""" Decleare serializer class for restAPI base on User models"""

from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer, ValidationError, CharField)


class UserSerializer(ModelSerializer):
    """ User seriazlier class """
    username = CharField(required=False)

    class Meta:
        """ Meta subclass """
        model = get_user_model()
        fields = ('id', 'phone_number', 'username',
                  'first_name', 'last_name', 'email')
        read_only_fields = ['id', 'phone_number', 'is_username_changed']

    def validate_username(self, value):
        """ Validate `username` field """
        if self.instance and self.instance.is_username_changed and self.instance.username != value:
            raise ValidationError('Username has been changed before')

        if value != self.instance.username and get_user_model().objects.filter(username=value).exists():
            raise ValidationError('Username is already taken')

        return value

    def validate_email(self, value):
        """ Validate `email` field """
        if value == '':
            raise ValidationError('This field may not be blank.')

        if value != self.instance.email and get_user_model().objects.filter(email=value).exists():
            raise ValidationError('Email is already taken')

        return value

    def validate_first_name(self, value):
        """ Validate `first_name` field """
        if value == '':
            raise ValidationError('This field may not be blank.')

        return value

    def validate_last_name(self, value):
        """ Validate `last_name` field """
        if value == '':
            raise ValidationError('This field may not be blank.')

        return value

    def update(self, instance, validated_data):
        new_username = validated_data.get('username', instance.username)
        if new_username != instance.username:
            if instance.is_username_changed:
                # If username is changed before, let do nothing
                validated_data['username'] = instance.username
            else:
                validated_data['is_username_changed'] = True

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['username_set'] = instance.is_username_changed
        return result
