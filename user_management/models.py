""" models.py """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from utils.validation import phone_regex
from utils.models import TimeStampMixin

from user_management.constants.groups import CUSTOMER, KITCHEN_STAFF, FRONT_DESK_STAFF


class User(TimeStampMixin, AbstractUser, models.Model):
    """ Class to customize the user's info """

    phone_number = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True, unique=True)
    first_name = models.CharField(
        _('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(
        _('last name'), max_length=150, blank=True,  null=True)
    email = models.EmailField(_('email address'), blank=True, null=True)

    # The flag for the first time user change the username
    is_username_changed = models.BooleanField(default=False)
    has_finished_onboarding = models.BooleanField(default=False)

    def __str__(self):
        return 'UserID {}'.format(str(self.id))

    @property
    def is_customer(self):
        """ Check user is customer """
        return self.groups.filter(name=CUSTOMER).exists()

    @property
    def is_kitchen_staff(self):
        """ Check user is staff """
        return self.groups.filter(name=KITCHEN_STAFF).exists()

    @property
    def is_front_desk_staff(self):
        """ Check user is staff """
        return self.groups.filter(name=FRONT_DESK_STAFF).exists()

    @property
    def onboarding_session(self):
        return {
            'username': self.username is not None and self.username != '' and self.has_finished_onboarding is not None,
            'first_name': self.first_name is not None and self.first_name != '',
            'last_name': self.last_name is not None and self.last_name != '',
            'email': self.email is not None and self.email != '',
        }

    def save(self, *args, **kwargs):
        self.has_finished_onboarding = self.first_name is not None and self.last_name is not None and \
            self.username is not None and self.email is not None and self.first_name != '' and \
            self.last_name != '' and self.email != '' and self.username != '' and self.has_finished_onboarding is not None

        super().save(*args, **kwargs)


class ProxyUser(User):
    """ Use Proxy User to group the user models in auth app """

    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = 'user'


class AuthSession(models.Model):
    """ The session for an OTP code """

    phone_number = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True)

    otp = models.CharField(max_length=10)
    key = models.BinaryField(max_length=200)
