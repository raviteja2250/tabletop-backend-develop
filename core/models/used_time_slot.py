"""
    Purpose: Declare schema for time slot model.
"""
from django.db import models

from utils.models import TimeStampMixin

from core.models import Order, TimeSlot


class UsedTimeSlot(TimeStampMixin, models.Model):
    """
        ORM class that present the UsedTimeSlot table
        This model is mainly used internally for recording which order in the timeslot
    """

    # FK
    time_slot = models.ForeignKey(
        TimeSlot, on_delete=models.CASCADE, related_name='used_time_slots')
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='used_time_slot')

    date = models.DateField()

    # Fields below just for cloning the value of time-slot, in case time-slot is changed
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)

    class Meta:
        # they should be unique together as 3 primary keys
        unique_together = (('time_slot', 'order', 'date'),)
