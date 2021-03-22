"""
    Contains everything related to payment
"""
import os
import logging
import json as json_lib

import Adyen

logger = logging.getLogger(__name__)


class CustomAdyenClient(Adyen.AdyenClient):
    """ Class as the custom version for Adyen's client """

    # pylint:disable=inconsistent-return-statements
    def _handle_response(self, url, raw_response, raw_request,
                         status_code, headers, request_dict):
        """
            - Override the _handle_response result
              due to the sdk haven't supported to create payment link
            - This function is copied from lib, so let ignore pylint and keep it as it is
        """
        if status_code != 200 and status_code != 201:  # pylint: disable=consider-using-in
            response = {}
            # If the result can't be parsed into json, most likely is raw html.
            # Some response are neither json or raw html, handle them here:
            if raw_response:
                response = json_lib.loads(raw_response)
            # Pass raised error to error handler.
            self._handle_http_error(url, response, status_code,
                                    headers.get('pspReference'),
                                    raw_request, raw_response,
                                    headers, request_dict)

            try:
                if response['errorCode']:
                    raise Adyen.exceptions.AdyenAPICommunicationError(
                        "Unexpected error while communicating with Adyen."
                        " Received the response data:'{}', HTTP Code:'{}'. "
                        "Please reach out to support@adyen.com if the "
                        "problem persists with the psp:{}".format(
                            raw_response,
                            status_code,
                            headers.get('pspReference')),
                        status_code=status_code,
                        raw_request=raw_request,
                        raw_response=raw_response,
                        url=url,
                        psp=headers.get('pspReference'),
                        headers=headers,
                        error_code=response['errorCode'])
            except KeyError:
                erstr = 'KeyError: errorCode'
                raise Adyen.exceptions.AdyenAPICommunicationError(
                    erstr) from KeyError
        else:
            try:
                response = json_lib.loads(raw_response)
                psp = headers.get('pspReference', response.get('pspReference'))
                return Adyen.client.AdyenResult(message=response, status_code=status_code,
                                                psp=psp, raw_request=raw_request,
                                                raw_response=raw_response)
            except ValueError:
                # Couldn't parse json so try to pull error from html.

                error = self._error_from_hpp(raw_response)

                message = request_dict

                reference = message.get("reference",
                                        message.get("merchantReference"))

                errorstring = """Unable to retrieve payment "
                list. Received the error: {}. Please verify your request "
                and try again. If the issue persists, please reach out to "
                support@adyen.com including the "
                merchantReference: {}""".format(error, reference),  # pylint: disable=trailing-comma-tuple

                raise Adyen.exceptions.AdyenInvalidRequestError(
                    errorstring) from ValueError


class PaymentRequest:
    """ The request's body for payment """

    def __init__(self, amount=None, reference=None, shopper_reference=None, psp_reference=None):
        if not isinstance(amount, float) and not isinstance(amount, int):
            raise TypeError('amount should be float')

        if amount <= 0:
            raise ValueError('amount should greater than zero')

        # For now let hard-code the Localisation as SG
        self.amount = amount
        self.shopper_reference = shopper_reference
        self.reference = reference
        self.psp_reference = psp_reference
        self.currency = "SGD"
        self.country_code = "SG"

    def to_create_payement_request(self):
        """ Convert to JSON for create payment """
        if not isinstance(self.reference, str):
            raise ValueError(
                'reference should be string. This field is required')

        result = {
            'amount': {
                # docs:https://docs.adyen.com/development-resources/currency-codes
                'value': self.amount * 100,
                'currency': self.currency
            },
            'reference': self.reference,
            'countryCode': self.country_code,
        }

        if self.shopper_reference and isinstance(self.shopper_reference, str):
            result['shopperReference'] = self.shopper_reference
            result['recurringProcessingModel'] = 'CardOnFile'
            result['storePaymentMethod'] = True

        return result

    def to_refund_request(self):
        """ Convert to JSON for refund """
        if not isinstance(self.psp_reference, str):
            raise ValueError('pspReference should be string')

        return {
            'originalReference': self.psp_reference,
        }


class PaymentService:
    """ PaymentService handle logic of payment flow """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PaymentService, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        # Initialize the adyen client
        kwargs = {
            'xapikey': os.environ.get('AO_ADYEN_API_KEY', ''),
            'platform': os.environ.get('AO_ADYEN_PLATFORM', 'test'),
            'merchant_account': os.environ.get('AO_ADYEN_MERCHANT_ACCOUNT', ''),
            'live_endpoint_prefix': os.environ.get(
                'AO_ADYEN_LIVE_ENDPOINT_PREFIX', ''),
        }

        self._ayden_instance = Adyen.Adyen(**kwargs)
        self._ayden_instance.client = CustomAdyenClient(**kwargs)

    def create_payment_link(self, payment_request):
        """ Create a payment with payment lnk"""

        if not isinstance(payment_request, PaymentRequest):
            raise TypeError('payment_request is not PaymentRequest')

        logger.info('Starting to create payment link.')

        # Send request to the Adyen
        response = self._ayden_instance.client.call_checkout_api(
            payment_request.to_create_payement_request(), 'paymentLinks')

        logger.info('Created payment link with response: %s', str(response))

        return response  # AdyenResult

    def refund(self, payment_request):
        """ Refund the payment """

        if not isinstance(payment_request, PaymentRequest):
            raise TypeError('payment_request is not PaymentRequest')

        logger.info('Starting to cancel/refund a payment.')

        # Send request to the Adyen
        response = self._ayden_instance.payment.cancel_or_refund(
            payment_request.to_refund_request())

        logger.info(
            'Processed to cancel/refund a payment with response %s', str(response))

        return response  # AdyenResult
