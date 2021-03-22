"""
    Contains everything related to pusher
"""
import os
import logging

import pusher

logger = logging.getLogger(__name__)


class PusherService:
    """ PusherService handle logic of Pusher """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        try:
            self.client = pusher.Pusher(
                app_id=os.environ.get('AO_PUSHER_APP_ID', ''),
                key=os.environ.get('AO_PUSHER_KEY', ''),
                secret=os.environ.get('AO_PUSHER_SECRET', ''),
                cluster=os.environ.get('AO_PUSHER_CLUSTER', ''),
                ssl=True
            )
        except Exception as err:
            logger.error('Pusher error: %s', str(err))

    def push(self, channel, event, content):
        """ Function to push the message to the channel """
        try:
            self.client.trigger(channel, event, content)
        except Exception as err:
            logger.error('Pusher error: %s', str(err))
