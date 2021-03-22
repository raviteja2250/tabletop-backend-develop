""" adyen_response """
from django.db import models

import jsonfield

from utils.models import TimeStampMixin

from core.models import Order


class AdyenResponse(TimeStampMixin, models.Model):
    """ ORM class that present the AdyenResponse table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)

    content = jsonfield.JSONField()
