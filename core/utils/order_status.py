"""
    Utilization functions support to handle order's status
"""

from django.core.exceptions import FieldError

from core.constants.order_status import (
    RECEIVED, REJECTED, ACCEPTED, CHECKED_OUT,
    COOKING, COOKED, READY_TO_SEND, FAILED,
    PENDING_REJECTION, ON_THE_WAY, COMPLETED
)

_STATUS_ORDER = {
    CHECKED_OUT: {
        "next_status": []  # In this case, status is handled internally
    },
    FAILED: {
        "next_status": []
    },
    RECEIVED: {
        "next_status": [ACCEPTED, PENDING_REJECTION, REJECTED]
    },
    PENDING_REJECTION: {
        "next_status": [REJECTED, RECEIVED]
    },
    REJECTED: {
        "next_status": []
    },
    ACCEPTED: {
        "next_status": [COOKING, PENDING_REJECTION, REJECTED]
    },
    COOKING: {
        "next_status": [COOKED]
    },
    COOKED: {
        "next_status": [READY_TO_SEND]
    },
    READY_TO_SEND: {
        "next_status": [ON_THE_WAY]
    },
    ON_THE_WAY: {
        "next_status": [COMPLETED]
    },
    COMPLETED: {
        "next_status": []
    },
}


def validate_order_status(old_status, new_status):
    """ Function to validate the order of status if correct """
    if old_status == new_status:
        return

    if not _STATUS_ORDER.get(old_status, None):
        raise FieldError('Previous status is invalid')

    if not _STATUS_ORDER.get(new_status, None):
        raise FieldError('New status is invalid')

    if len(_STATUS_ORDER[old_status]['next_status']) == 0:
        raise FieldError('Status is invalid')

    if (_STATUS_ORDER[old_status]['next_status']) != 0 and \
            new_status not in _STATUS_ORDER[old_status]['next_status']:
        raise FieldError('Status is invalid')

    return
