from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException

from utils.constants.status_code import HTTP_450_HAS_NOT_FISNIHED_ONBOARDING


class HasNotFinishedOnboarding(APIException):
    status_code = HTTP_450_HAS_NOT_FISNIHED_ONBOARDING
    default_detail = _('User hasn\'t finished the onboarding.')
    default_code = 'hasn\'t_finished_onboarding'

    def __init__(self, detail=None, code=None):
        """ Override the __init__ to avoid transform data to ErrorDetail """
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = detail
