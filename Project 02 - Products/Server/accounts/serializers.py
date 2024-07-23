from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """

    """
    email = serializers.CharField(max_length=120)
    username = serializers.CharField(max_length=80)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:

        model = User
        fields = [
            'email',
            'username',
            'password'
        ]

    def validate(self, attrs):

        # Custom validation checks
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('Email has already been used')

        # Ensures that default validations checks
        return super().validate(attrs)

    def create(self, validated_data):

        # From the validated_data removing the password
        password = validated_data.pop("password")
        # Using create method creating new instance of user without password
        user = super().create(validated_data)
        # Setting up the password for the user
        user.set_password(password)
        # Saving the data into DB
        user.save()

        # Creating a token for the current user for authentication
        Token.objects.create(user=user)

        return user

