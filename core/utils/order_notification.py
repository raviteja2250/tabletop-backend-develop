import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


from utils.ses_service import SESService, SESInternalException

logger = logging.getLogger(__name__)

CHANNEL_NAME = "#slack-bot-tutorial"

client = WebClient(token=os.environ['SLACK_TOKEN'])

_NEW_ORDER_MESSAGE = {
    'subject': '[TABLETOP] We have the new order #%s',
    'message': 'Hi, we have the new order with id #%s'
}

_SENDER = os.environ.get('ORDER_NOTIFICATION_SENDER', '')
_DESTINATION = os.environ.get('ORDER_NOTIFICATION_DESTINATION', '').split(',')


class OrderNotificationService():
    """ Class to handle the way to notify user when we have something happend with order """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OrderNotificationService, cls).__new__(cls)

        return cls.instance

    def send_new_paid_order_notification(
        self, order_id, sender=_SENDER,  destination=_DESTINATION,
        subject=_NEW_ORDER_MESSAGE['subject'], message=_NEW_ORDER_MESSAGE['message']
    ):
        """ Send notification to the admin when we have new order """
        try:
            SESService().send_text_email(
                sender, destination,
                subject % (order_id), message % (order_id))
            logger.info('Sent email to %s', str(destination))
        except SESInternalException as err:
            logger.error('Error when sending email %s', str(err))

        try:
            client.chat_postMessage(channel=CHANNEL_NAME, text=message)
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")