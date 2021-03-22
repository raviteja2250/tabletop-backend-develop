""" sns_service.py """
from django.conf import settings

import boto3


class SNSService():
    """ Service to interact with the AWS SNS"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SNSService, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.client = boto3.client(
            "sns",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def publish_message(self, phone_number, message):
        """ Send message to a phone number """
        try:
            self.client.publish(PhoneNumber=phone_number, Message=message)
        except Exception as err:
            raise SNSInternalException(err) from err


class SNSInternalException(Exception):
    """
        The intenal exceptions are raised by SNS
        Now we don't need to care more about detail
    """
