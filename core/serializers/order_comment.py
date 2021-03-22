""" Decleare serializer class for restAPI base on OrderComment models"""

from rest_framework.serializers import (
    ModelSerializer, PrimaryKeyRelatedField, ValidationError, ChoiceField
)

from core.models import OrderComment, Order
from core.constants.order_status import PENDING_REJECTION
from core.constants.order_comment_type import (
    KITCHEN, SERVICE
)


class OrderCommentSerializer(ModelSerializer):
    """ OrderComment seriazlier class """
    type = ChoiceField(required=False, choices=(
        (KITCHEN, 'Kitchen'),
        (SERVICE, 'Service'),
    ), default=KITCHEN)

    class Meta:
        """ Meta subclass """
        model = OrderComment
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            user = request.user

        order_comment = OrderComment.objects.create(
            user=user, **validated_data)

        return order_comment

    def validate(self, attrs):
        order = attrs.get('order', None)

        if order and order.status != PENDING_REJECTION:
            raise ValidationError(
                {'order': 'Comment is created for pending_rejection order only'})

        return attrs


class OrderCommentInlineSerializer(OrderCommentSerializer):
    """ OrderComment seriazlier class """
    type = ChoiceField(required=False, choices=(
        (KITCHEN, 'Kitchen'),
        (SERVICE, 'Service'),
    ), default=KITCHEN)

    order = PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=False)
