"""
    Utilization functions support to handle cooking item's status
"""

from django.core.exceptions import FieldError

from core.constants.cooking_status import (
    COOKING, COOKED, PICKEDUP
)

_COOKING_ITEM_STATUS = {
    COOKING: {
        "previous_status": [],
        "next_status": [COOKED]
    },
    COOKED: {
        "previous_status": [COOKING],
        "next_status": [PICKEDUP]
    },
    PICKEDUP: {
        "previous_status": [COOKED],
        "next_status": []
    },
}


def validate_cooking_item_status(old_status, new_status):
    """ Function to validate the status of cooking item """
    if old_status == new_status:
        return

    if not _COOKING_ITEM_STATUS.get(old_status, None):
        raise FieldError('Previous status is invalid')

    if not _COOKING_ITEM_STATUS.get(new_status, None):
        raise FieldError('New status is invalid')

    if new_status not in _COOKING_ITEM_STATUS[old_status]['next_status'] and new_status not in _COOKING_ITEM_STATUS[old_status]['previous_status']:
        raise FieldError('Status is invalid')

    return
