""" time_slot.py """
import datetime

from django.db.models import Prefetch

from rest_framework import serializers

from utils.constants.date_format import DATE_FORMAT, TIME_FORMAT

from core.models import BrandTimeSlot
from core.serializers import BrandSerializer


class TimeSlotSerializer(serializers.Serializer):
    """ Serializer class for Timeslot per Brand """

    brand = BrandSerializer(read_only=True)
    date_list = serializers.ListField(
        child=serializers.DateField(read_only=True),
        read_only=True
    )

    def to_representation(self, instance):
        json_instance = super().to_representation(instance)
        time_slots_of_brand = BrandTimeSlot.objects.filter(
            brand=instance['brand']).prefetch_related('time_slots').prefetch_related(
            Prefetch('time_slots__time_range'),
            Prefetch('time_slots__used_time_slots'),
        )

        result = dict()
        now = datetime.datetime.now() + datetime.timedelta(
            minutes=(instance['brand'].cooking_time + instance['brand'].delivery_time))

        for _date in json_instance['date_list']:
            result_per_date = []
            _date_instance = datetime.datetime.strptime(_date, DATE_FORMAT)

            # Find timeslot of this day of week
            _day_of_week = _date_instance.weekday()
            _time_slot_per_day_list = list(
                filter(lambda x: x.day_of_week == _day_of_week, time_slots_of_brand))  # pylint: disable=cell-var-from-loop
            _time_slot_per_day = _time_slot_per_day_list[0] if len(
                _time_slot_per_day_list) > 0 else None

            if not _time_slot_per_day:
                result[_date] = result_per_date
                continue

            _time_slots = sorted(
                _time_slot_per_day.time_slots.all(), key=lambda x: x.time_range.start)

            for _time_slot_with_capacity in _time_slots:
                if _date_instance.replace(
                        hour=_time_slot_with_capacity.time_range.start.hour,
                        minute=_time_slot_with_capacity.time_range.start.minute) >= now:
                    result_per_date.append({
                        'id': _time_slot_with_capacity.id,
                        'start': _time_slot_with_capacity.time_range.start.strftime(TIME_FORMAT),
                        'day_of_week': _date_instance.strftime("%a"),
                        'end': _time_slot_with_capacity.time_range.end.strftime(TIME_FORMAT),
                        'available_slots': _time_slot_with_capacity.available_slots(date=_date)
                    })

            result[_date] = result_per_date

        return result
