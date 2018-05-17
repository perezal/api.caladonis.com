from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CharField, empty
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError


class PasswordField(CharField):

    def run_validators(self, value):
        password_validation.validate_password(value)
        super(PasswordField, self).run_validators(value)

class UserSerializer(serializers.ModelSerializer):

    password = PasswordField(
        max_length=128,
        write_only=True,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        # the serializer will call create() instead of create_user(),
        # so we stomp on the create method
        User.objects.create = User.objects.create_user
        model = User
        fields = ('username', 'email', 'password')
