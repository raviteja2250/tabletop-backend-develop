""" core/signals.py """
import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from core.utils.pusher_service import PusherService
from core.utils.payments import PaymentService, PaymentRequest
from core.models import Location, Order, CookingItem, OrderComment
from core.constants.channels import KITCHEN_CHANNEL, APP_CHANNEL
from core.constants.events import UPDATED_COOKING_ITEM, UPDATED_ORDER, NEW_ORDER_COMMENT
from core.constants import order_status
from core.utils.order_notification import OrderNotificationService

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Location)
def save_location(sender, instance, **kwargs):
    """ Function is ran before save Location """
    # Get the old instance
    old_instance = None
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)

    if not old_instance:
        # In case create new
        locations = Location.objects.filter(user=instance.user)
        instance.is_default = False
        if len(locations) == 0:
            instance.is_default = True
    else:
        # In case update
        if instance.is_default and old_instance.is_default != instance.is_default:
            Location.objects.filter(
                user=instance.user, is_default=True).update(is_default=False)


@receiver(pre_save, sender=Order)
def save_order(sender, instance, **kwargs):
    """ Function is ran before save Order """
    # Get the old instance
    old_instance = None
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)

    if old_instance:  # Update order
        # Do something when status change
        if old_instance.status != instance.status:
            if instance.status == order_status.REJECTED and instance.payment_psp_reference:
                try:
                    payment_service = PaymentService()
                    payment_request = PaymentRequest(
                        amount=instance.total_price, psp_reference=instance.payment_psp_reference)
                    response = payment_service.refund(payment_request)
                    instance.refund_psp_reference = response.message['pspReference']
                except Exception as err:
                    logger.error('Refund order failed. %s', str(err))

            # Should send message after refund the payment
            PusherService().push(KITCHEN_CHANNEL,
                                 UPDATED_ORDER, {'id': instance.pk})
            PusherService().push(
                APP_CHANNEL, UPDATED_ORDER, {'id': instance.pk, 'isNew': False})

        # In case the payment is paid
        if not old_instance.paid and instance.paid:
            # Sending notification to admin
            OrderNotificationService().send_new_paid_order_notification(instance.id)

            # Breaking down the cooking item.
            for ordered_item in instance.order_items.all():
                for _i in range(ordered_item.quantity):
                    CookingItem.objects.create(
                        menu_item=ordered_item.menu_item, order=instance
                    )


@receiver(pre_save, sender=CookingItem)
def save_cooking_item(sender, instance, **kwargs):
    """ Function is ran before save CookingItem """
    if not instance.pk:
        return

    old_instance = sender.objects.get(pk=instance.pk)

    if old_instance.status != instance.status:
        # For now, just push message when status change.
        PusherService().push(KITCHEN_CHANNEL,
                             UPDATED_COOKING_ITEM, {'id': instance.pk, 'order_id': instance.order.id})


@receiver(post_save, sender=OrderComment)
def save_order_comment(sender, instance, created, **kwargs):
    """ Function is ran before save OrderComment """
    if created:
        PusherService().push(
            KITCHEN_CHANNEL, NEW_ORDER_COMMENT,
            {'id': instance.id, 'order_id': instance.order.id}
        )
