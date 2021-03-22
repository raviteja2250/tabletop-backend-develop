""" ses_service.py """
from django.conf import settings

import boto3


class SESService():
    """
        Service to interact with the AWS SES
        It's simple now for text only, we can enhance later when we have more requirements
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SESService, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.client = boto3.client(
            "ses",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def send_text_email(self, sender='',  destination='', subject='', message='', **kwargs):
        """ Send simple email with text only """
        try:
            self.client.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': destination if isinstance(destination, list) else [destination],
                },
                Message={
                    'Subject': {
                        'Data': subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': message,
                        },
                    }
                },
                **kwargs,  # For override the configuration
            )
        except Exception as err:
            raise SESInternalException(err) from err


class SESInternalException(Exception):
    """
        The intenal exceptions are raised by SES
        Now we don't need to care more about detail
    """
