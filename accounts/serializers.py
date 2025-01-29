from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accounts.models import User

READ_FIELDS = (
    'id',
    'name',
    'email',
    'is_owner',
)

WRITE_FIELDS = (
    'name',
    'email',
    'password',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = READ_FIELDS


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = WRITE_FIELDS

    def validate(self, data):
        password = data.get('password')
        if not self.instance and password:
            try:
                user_data = data.copy()
                password_validation.validate_password(
                    password, user=User(**user_data)
                )
            except DjangoValidationError as error:
                raise serializers.ValidationError({
                    'password': list(error.messages)
                })
        return super(User, self).validate(data)
