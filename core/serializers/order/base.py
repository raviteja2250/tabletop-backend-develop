""" Decleare serializer class for restAPI base on Order models"""

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import ModelSerializer

from user_management.serializers import UserSerializer

from utils.constants.date_format import TIME_FORMAT, DATE_FORMAT

from core.serializers import (
    DiscountSerializer, FeeSerializer, BrandSerializer, LocationSerializer
)


class OrderSerializer(ModelSerializer):
    fees = FeeSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)

        # Transform data manually here because we may extend those field in another class.
        result['total_price'] = str(instance.total_price)
        result['sub_total_price'] = str(instance.base_price)
        result['user'] = UserSerializer(instance.user).data
        result['brand'] = BrandSerializer(instance.brand).data
        result['location'] = LocationSerializer(instance.location).data

        result['discount'] = None
        if hasattr(instance, 'discount'):
            result['discount'] = DiscountSerializer(instance.discount).data

        try:
            used_time_slot = instance.used_time_slot
            result['time_slot'] = {
                'start': used_time_slot.start.strftime(TIME_FORMAT),
                'end': used_time_slot.end.strftime(TIME_FORMAT),
                'date': used_time_slot.date.strftime(DATE_FORMAT)
            }
        except (ObjectDoesNotExist, AttributeError):
            result['time_slot'] = None

        return result
