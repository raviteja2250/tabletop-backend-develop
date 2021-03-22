""" Decleare serializer class for restAPI base on Order models"""
from django.core.exceptions import FieldError

from rest_framework.serializers import ValidationError


from core.models import Order, CookingItem, OrderComment

from core.constants import order_status, cooking_status
from core.utils import order_status as utils
from core.serializers import OrderCommentInlineSerializer
from core.serializers.order import OrderSerializer


class UpdateOrderSerializer(OrderSerializer):
    """ Order seriazlier class """
    order_comments = OrderCommentInlineSerializer(
        many=True, required=False, write_only=True)

    class Meta:
        """ Meta subclass """
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'paid', 'refunded', 'refunded_psp_reference',
            'payment_psp_reference', 'payment_link', 'completed_time', 'received_time', 'due_time',
            'discounts', 'fees', 'brand', 'order_items',

        ]

    def validate(self, attrs):
        request = self.context.get("request", None)
        new_status = attrs.get('status', None)
        order_comments = attrs.get('order_comments', None)

        # NOTE: This way should be use later.
        # if self.instance.status == order_status.PENDING_REJECTION and \
        #         new_status == order_status.RECEIVED and request and not request.user.is_front_desk_staff:
        #     raise ValidationError(
        #         {'status': 'Only frontdesk staff can handle rejected order'})

        if order_comments and len(order_comments) > 0:
            if not(self.instance.status == order_status.PENDING_REJECTION and new_status == order_status.RECEIVED) and \
                    not(self.instance.status == order_status.PENDING_REJECTION and new_status == order_status.REJECTED) and \
                    not((self.instance.status != order_status.PENDING_REJECTION and self.instance.status != order_status.REJECTED) and
                        (new_status in (order_status.REJECTED, order_status.PENDING_REJECTION))):
                raise ValidationError(
                    {'status': 'Should give comment for only rejected order'})
        else:
            if self.instance.status != new_status and (new_status in (order_status.REJECTED, order_status.PENDING_REJECTION)):
                raise ValidationError(
                    {'order_comments': 'Should give the reason to reject order'})

            if self.instance.status == order_status.PENDING_REJECTION and new_status == order_status.RECEIVED:
                raise ValidationError(
                    {'order_comments': 'Should give the reason to renew order'})

        return attrs

    def validate_status(self, value):
        """ Validator for te status field """

        # Validate the order of status.
        try:
            utils.validate_order_status(self.instance.status, value)
        except FieldError as field_error:
            raise ValidationError('Status is invalid') from field_error

        # Validate cooking items
        cooking_items = CookingItem.objects.filter(order=self.instance)
        if value == order_status.COOKED:
            # When order's status is changed from cooking to cooked,
            # ensure all items are cooked
            cooked_items = cooking_items.filter(
                status__in=[cooking_status.COOKED, cooking_status.PICKEDUP])
            if len(cooked_items) != len(cooking_items):
                raise ValidationError(
                    'All items should be cooked before changing order status')

        if value == order_status.READY_TO_SEND:
            # When order's status is changed from cookied to ready_to_send,
            # ensure all items are picked up
            picked_up_item = cooking_items.filter(
                status=cooking_status.PICKEDUP)

            if len(picked_up_item) != len(cooking_items):
                raise ValidationError(
                    'All items should be picked up before changing order status')

        return value

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        order_comment_data = validated_data.get('order_comments', None)

        if not request or not request.user:
            return super().update(instance, validated_data)

        # NOTE: This way should be use later.
        # new_status = validated_data.get('status')
        # if instance.status != new_status and \
        #         new_status == order_status.REJECTED and \
        #         request.user.is_kitchen_staff:
        #     # Kitchen can't reject order
        #     validated_data['status'] = order_status.PENDING_REJECTION

        if order_comment_data:
            order_comments = [OrderComment(
                order=self.instance,
                user=request.user,
                **order_comment_datom) for order_comment_datom in order_comment_data]
            OrderComment.objects.bulk_create(order_comments)

        return super().update(instance, validated_data)
