from rest_framework import serializers

from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    RegistrationSerializer is a serializer for user registration with password hashing

    password
        A write-only field for the user's password

    Meta
        model
            Specifies that the serializer is for the User model
        fields
            Lists the fields included in the serialization: 'username', 'email', 'password'

    create(validated_data)
        Creates a new user instance
        Arguments:
            validated_data: The validated data from the serializer containing 'username', 'email', and 'password'
        Returns:
            The created user instance with the password hashed
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    """
    AccountSerializer is a ModelSerializer for the User model.
    It serializes the 'username' and 'email' fields from the User model.

    Inner class Meta:
        The Meta class holds configuration for the AccountSerializer.
        - model: Specifies the model to serialize.
        - fields: A list of the fields to include in the serialization.
    """

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
