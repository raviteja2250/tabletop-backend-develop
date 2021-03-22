""" Declare utilization services """
import base64
import datetime
import logging

import pyotp

from django.conf import settings

from utils.sns_service import SNSService, SNSInternalException


logger = logging.getLogger(__name__)


# OTP Handler section
_expiry_time = settings.OTP_EXPIRY_TIME
_digits = settings.OTP_DIGITS


class OTPHandler():
    """ Class to handle logic to generate/verify OTP code """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OTPHandler, cls).__new__(cls)

        return cls.instance

    def generate_key(self, input_str):
        """ Function to generate the key from input string """
        return base64.b32encode((input_str + str(datetime.datetime.now()) + settings.SECRET_KEY).encode())

    def generate_totp(self, key, expiry_time=_expiry_time, digits=_digits):
        """ Function to generate the TOTP code """
        otp = pyotp.totp.TOTP(key, interval=expiry_time, digits=digits)
        return otp.now()

    def verify_totp(self, otp_code, key, expiry_time=_expiry_time, digits=_digits):
        otp = pyotp.totp.TOTP(key, interval=expiry_time, digits=digits)
        return otp.verify(otp_code)


# OTP Notification section
_OTP_SMS_CONTENT = 'Your authentication code is %s'


class OTPNotificationService():
    """ Class to handle the way to notify user when they reuqest OTP """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OTPNotificationService, cls).__new__(cls)

        return cls.instance

    def send_otp(self, phone_number, otp_code):
        """ Send OTP to the customer """
        try:
            SNSService().publish_message(phone_number, (_OTP_SMS_CONTENT % otp_code))
            logger.info('New OTP request for %s', phone_number)
        except SNSInternalException as err:
            logger.error('Error when sending OTP %s', str(err))
