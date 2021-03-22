""" Decleare serializer class for restAPI base on Order models"""

import datetime
import logging

from django.db import transaction

from rest_framework.serializers import (
    ValidationError, DictField, ChoiceField,
    PrimaryKeyRelatedField)

from utils.constants.date_format import DATE_FORMAT

from core.models import (
    Order, OrderItem, TimeSlot, Discount,
    UsedTimeSlot, OrderFee, Brand,  Fee)
from core.constants import order_status
from core.utils.payments import PaymentService, PaymentRequest
from core.utils.date import minutes_between
from core.constants import order_type
from core.constants.time_slot import COOKING_TIME_AS_MINUTES, DELIVERY_TIME_AS_MINUTES
from core.utils.pusher_service import PusherService
from core.constants.channels import KITCHEN_CHANNEL, APP_CHANNEL
from core.constants.events import UPDATED_ORDER
from core.serializers import OrderItemSerializer
from core.serializers.order import OrderSerializer
from core.constants.order_type import (
    DINE_IN, DELIVERY, TAKE_AWAY
)
from core.constants.monetary import PERCENT

logger = logging.getLogger(__name__)


class CreateOrderSerializer(OrderSerializer):
    """ Order seriazlier class """
    order_items = OrderItemSerializer(many=True)
    type = ChoiceField(required=True, choices=(
        (DINE_IN, 'Dine In'),
        (DELIVERY, 'Delivery'),
        (TAKE_AWAY, 'Take away'),
    ))
    brand = PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=True)
    discount = PrimaryKeyRelatedField(
        queryset=Discount.objects.all(), required=False)
    time_slot = DictField(allow_empty=True, write_only=True,
                          required=False)  # {"id": ..., "date"}

    class Meta:
        """ Meta subclass """
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'paid', 'refunded', 'refunded_psp_reference',
            'payment_psp_reference', 'payment_link', 'completed_time',
            'received_time', 'due_time', 'discounts', 'fees'
        ]

    def __init__(self, *args, **kwargs):
        self._time_slot_instance = None
        super().__init__(*args, **kwargs)

    @staticmethod
    def update_order_discount(instance, discount, order_items):
        """ Utilization function to add discount into order """
        if not discount:
            return

        order_discount = discount.clone_to_order_discount(instance)
        order_discount.save()

        if discount.type == PERCENT:
            for order_item in order_items:
                if not order_item.no_discount:
                    order_item.calculate_discounted_price([discount])

            OrderItem.objects.bulk_update(order_items, ['discounted_price'])

    @staticmethod
    def update_order_fee(instance):
        """ Utilization function to add fee into order """

        # Automatic fee
        fees = Fee.objects.filter(
            brand=instance.brand, order_type__contains=instance.type)

        order_fee_list = [fee.clone_to_order_fee(instance) for fee in fees]
        OrderFee.objects.bulk_create(order_fee_list)

    @staticmethod
    def create_payment(order):
        try:
            # Create payment's request
            shopper_reference = order.user.phone_number if order.user is not None else None

            payment_request = PaymentRequest(
                amount=order.total_price, reference=str(order.pk), shopper_reference=shopper_reference)

            # Check out the order
            payment_service = PaymentService()
            payment_result = payment_service.create_payment_link(
                payment_request)
        except Exception as err:
            logger.error('Create payment error %s', str(err))
            order.status = order_status.FAILED
            return

        # If there is no err, means payment link is created,
        # let change the status to checked_out and update the link
        order.status = order_status.CHECKED_OUT
        order.payment_link = payment_result.message['url']

    @transaction.atomic
    def create(self, validated_data):
        discount = validated_data.pop('discount', None)
        time_slot = validated_data.pop('time_slot', None)
        validated_order_items = validated_data.pop('order_items')
        order = super().create(validated_data)

        # Create order item. 8
        order_item_list = [OrderItem(order=order, **validated_order_item)
                           for validated_order_item in validated_order_items]
        OrderItem.objects.bulk_create(order_item_list)

        # Assign current user into the Order
        request = self.context.get('request')
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            order.user = request.user

        # Create the used time slot
        if time_slot:
            used_time_slot = UsedTimeSlot(
                order=order,
                time_slot=self._time_slot_instance,
                start=self._time_slot_instance.time_range.start,
                end=self._time_slot_instance.time_range.end,
                date=datetime.datetime.strptime(
                    time_slot['date'], DATE_FORMAT))
            used_time_slot.save()

        # # Apply the discount_code
        self.update_order_discount(order, discount, order_item_list)
        self.update_order_fee(order)

        self.create_payment(order)

        # Save all changes
        order.save()

        # Send signal to the client, because there are many-to-many fields,
        # So, the save() will be called many time => Send signal manually
        PusherService().push(KITCHEN_CHANNEL,
                             UPDATED_ORDER, {'id': order.id, 'isNew': True})
        PusherService().push(
            APP_CHANNEL, UPDATED_ORDER, {'id': order.pk})

        logger.info('Created new order: %s', str(order.id))

        return order

    def validate_order_items(self, value):
        """ Validator for the order_items field """

        if not isinstance(value, list) or len(value) == 0:
            raise ValidationError(
                'Order\'s items can not be empty')

        return value

    def validate_status(self, value):
        """ Validator for the status field """
        # For creating new order, always checked out
        return order_status.CHECKED_OUT

    def validate(self, attrs):
        """ Validator for the time_slot field """
        #
        # Validate table_no
        #
        table_no = attrs.get('table_no', None)
        if not table_no and attrs['type'] == order_type.DINE_IN:
            raise ValidationError({'table_no': 'Dine in order needs table no'})

        #
        # Validate location
        #
        if attrs['type'] == order_type.DELIVERY and not attrs.get('location', None):
            raise ValidationError(
                {'location': 'Delivery order should have location'})

        #
        # Validate order's items should be in the same brand
        #

        for order_item in attrs['order_items']:
            if order_item['menu_item'].brand.id != attrs['brand'].id:
                raise ValidationError(
                    {'order_items': 'Can\'t order item in multiple brands'})

        #
        # Validate discount belongs to the brand
        #
        discount = attrs.get('discount', None)
        if discount:
            if discount.brand.id != attrs['brand'].id:
                raise ValidationError(
                    {'discount': 'Discount doesn\'t belong to this brand'})

            if attrs['type'] not in discount.order_type:
                raise ValidationError(
                    {'discount': 'Discount can\'t be applied for this order_type'})
        #
        # Validate time_slot
        #
        time_slot_data = attrs.get('time_slot', {})

        cooking_time = attrs['brand'].cooking_time
        delivery_time = attrs['brand'].delivery_time
        if not cooking_time:
            lead_time = COOKING_TIME_AS_MINUTES
        if not delivery_time:
            lead_time = DELIVERY_TIME_AS_MINUTES

        lead_time = cooking_time + delivery_time

        if attrs['type'] != order_type.DELIVERY and attrs['type'] != order_type.TAKE_AWAY:
            if bool(time_slot_data):
                raise ValidationError(
                    {'time_slot': 'Only delivery and take away order need time slot'})
            return attrs  # TODO: Need refactor here, if return here, validation after this line can't be run

        if not bool(time_slot_data) and attrs['type'] == order_type.DELIVERY:
            raise ValidationError(
                {'time_slot': 'Delivery order needs time slot'})

        if not bool(time_slot_data) and attrs['type'] == order_type.TAKE_AWAY:
            raise ValidationError(
                {'time_slot': 'Take away order needs time slot'})

        if not time_slot_data.get('id', None) or not time_slot_data.get('date', None):
            raise ValidationError(
                {'time_slot': 'Time slot needs `id` and `date`'})

        now = datetime.datetime.now()
        time_slot = TimeSlot.objects.filter(
            pk=time_slot_data['id']).first()
        time_slot_date = datetime.datetime.strptime(
            time_slot_data['date'], DATE_FORMAT)

        if not time_slot:
            raise ValidationError({'time_slot': 'Time slot not found'})

        if time_slot_date.weekday() != time_slot.brand_time_slot.day_of_week:
            raise ValidationError({'time_slot': 'Day of week is invalid'})

        if time_slot.available_slots(date=time_slot_data['date']) <= 0:
            raise ValidationError({'time_slot': 'Time slot is not available'})

        if time_slot_date.replace(hour=time_slot.time_range.start.hour,
                                  minute=time_slot.time_range.start.minute) < now:
            raise ValidationError(
                {'time_slot': 'Order\'s date can not be in the past'})

        if minutes_between(
                time_slot_date.replace(hour=time_slot.time_range.start.hour,
                                       minute=time_slot.time_range.start.minute),
                now) < lead_time:
            raise ValidationError({'time_slot': 'Order should be place before ' +
                                   str(lead_time) + ' minutes for the preparation'})

        self._time_slot_instance = time_slot

        return attrs
