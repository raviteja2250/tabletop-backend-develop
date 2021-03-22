""" Declare validator for model fields """
import re

from django.core.validators import RegexValidator

_REGEX_TEXT = r'^\+(?:[0-9]●?){6,14}[0-9]$'

phone_regex = RegexValidator(
    regex=_REGEX_TEXT, message="Phone is invalid")


def is_valid_phone_number(phone_number):
    """ Validate if a phone number is valid """
    return re.search(_REGEX_TEXT, phone_number)
