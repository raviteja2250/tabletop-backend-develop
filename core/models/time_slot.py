"""
    Purpose: Declare schema for time slot model.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from core.models import Brand
from core.constants.day_of_week import (
    MONDAY, TUESDAY, WEDNESDAY,
    THURSDAY, FRIDAY, SATURDAY, SUNDAY
)
from utils.constants.date_format import TIME_FORMAT


class TimeRange(models.Model):
    """ Timeslot with capacity """
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return self.start.strftime(TIME_FORMAT) + ' - ' + self.end.strftime(TIME_FORMAT)

    def clean(self):
        if self.end < self.start:
            raise ValidationError("End time should after start time")

        start_str = self.start.strftime(TIME_FORMAT)
        end_str = self.end.strftime(TIME_FORMAT)
        existing_time_range = TimeRange.objects.filter(
            start__contains=start_str, end__contains=end_str).first()

        if existing_time_range and (self.pk is None or existing_time_range.pk != self.pk):
            raise ValidationError(
                "The time range exists. Please use it instead of creating the new one")


class BrandTimeSlot(models.Model):
    """ ORM class that present the TimeSlot table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='time_slots', null=True)

    day_of_week = models.IntegerField(choices=(
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ))

    def clean(self):
        existing_brand_time_slot = BrandTimeSlot.objects.filter(
            day_of_week=self.day_of_week, brand=self.brand).first()
        if existing_brand_time_slot and (self.pk is None or existing_brand_time_slot.pk != self.pk):
            raise ValidationError(
                "The time slot for this day of week is created.")


class TimeSlot(models.Model):
    """ Timeslot with capacity """
    capacity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ],
    )

    brand_time_slot = models.ForeignKey(
        BrandTimeSlot, on_delete=models.CASCADE, related_name='time_slots', null=True)
    time_range = models.ForeignKey(
        TimeRange, on_delete=models.CASCADE, related_name='time_slots', null=True)

    def available_slots(self, date):
        """ Check this timeslot is available in that date """
        used_time_slots = []

        for _used_time_slots in self.used_time_slots.all():  # Used prefetch here
            if str(_used_time_slots.date) == date:
                used_time_slots.append(_used_time_slots)

        if len(used_time_slots) < self.capacity:
            return self.capacity - len(used_time_slots)

        return 0
