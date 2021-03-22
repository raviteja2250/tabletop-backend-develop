""" Decleare serializer class for OTP
"""
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import (
    Serializer, CharField, ValidationError)
from rest_framework.exceptions import NotFound

from utils.validation import phone_regex

from user_management.models import AuthSession
from user_management.constants.groups import CUSTOMER
from user_management.utils import OTPHandler, OTPNotificationService
from user_management.serializers import CustomTokenObtainPairSerializer


class RequestOTPSerializer(Serializer):
    """ RequestOTP seriazlier class """
    phone_number = CharField(validators=[phone_regex], max_length=20)

    def request_otp(self):
        """ Request the OTP from valid phone_number """

        phone_number = self.validated_data.get('phone_number', None)

        # If phone number is normal, process it properly
        if phone_number != settings.DEMO_USER['phone_number']:
            otp_handler = OTPHandler()
            secret_key = otp_handler.generate_key(phone_number)
            otp_code = otp_handler.generate_totp(secret_key)

            # Delete old session and create new session for this process
            AuthSession.objects.filter(phone_number=phone_number).delete()
            AuthSession.objects.create(
                phone_number=phone_number, otp=otp_code, key=secret_key)

            # Send SMS to customer
            OTPNotificationService().send_otp(phone_number,  otp_code)

    def to_representation(self, instance):
        # Check user is registered
        try:
            existing_user = get_user_model().objects.get(
                phone_number=instance['phone_number'])
            registered = existing_user.has_finished_onboarding
        except ObjectDoesNotExist:
            registered = False

        return {
            "message": "OTP sent as SMS",
            "phone_number": instance['phone_number'],
            "registered": registered
        }


class ConfirmOTPSerializer(Serializer):
    """ ConfirmOTP seriazlier class """
    phone_number = CharField(validators=[phone_regex], max_length=20)
    confirmation_code = CharField(max_length=4)

    def confirm_otp(self):
        """ Request the OTP from valid phone_number """

        phone_number = self.validated_data.get('phone_number', None)
        confirmation_code = self.validated_data.get('confirmation_code', None)

        # If phone number is normal, process it properly
        if phone_number != settings.DEMO_USER['phone_number']:

            # Finding existing session
            session = AuthSession.objects.filter(
                phone_number=phone_number).first()
            if not session or session.otp != confirmation_code:
                # If session is not created before or the otp is wrong.
                raise ValidationError({'detail': 'Invalid session'})

            # Verify the otp
            is_valid_otp = OTPHandler().verify_totp(confirmation_code, session.key)
            if not is_valid_otp:
                session.delete()
                raise ValidationError({'detail': 'Invalid session'})

            # Create/get the user
            try:
                user = get_user_model().objects.get(phone_number=phone_number)
            except get_user_model().DoesNotExist:
                # For new user, it will be inactive until finishing the onboarding
                user = get_user_model().objects.create(
                    phone_number=phone_number, username=uuid4())

                # Add new user to group
                group = Group.objects.filter(name=CUSTOMER).first()
                user.groups.add(group)
                user.save()

            # Delete the session to prevent user login many time.
            session.delete()
        else:
            # Validate the OTP
            if confirmation_code != settings.DEMO_USER['otp']:
                raise ValidationError({'detail': 'Invalid session'})

            user = get_user_model().objects.filter(
                phone_number=settings.DEMO_USER['phone_number']).first()
            if not user:
                raise NotFound({'user': ['User not found']})

        self.validated_data['user'] = user

    def to_representation(self, instance):
        token_serializer = CustomTokenObtainPairSerializer(data={
            'user': instance['user'],
        })
        token_serializer.is_valid(raise_exception=True)

        return token_serializer.data
