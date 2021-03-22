from django.db import models
from django.core.exceptions import ValidationError


class GeneralConfig(models.Model):
    """ Contain the config for the mobile application  """

    class Meta:
        verbose_name = 'General'
    # FK
    on_maintenance = models.BooleanField(default=False)
    maintenance_due_time = models.DateTimeField(blank=True, null=True)

    def clean(self, *args, **kwargs):
        if self.on_maintenance and not self.maintenance_due_time:
            raise ValidationError('maintenance_due_time is required')

    def save(self, *args, **kwargs):
        if not self.on_maintenance:
            self.maintenance_due_time = None
        super().save(*args, **kwargs)
