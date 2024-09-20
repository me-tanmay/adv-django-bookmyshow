import logging
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

logger = logging.getLogger("bookmyshow_api")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                logger.warning(f"Login attempt failed: User with email {email} does not exist.")
                raise serializers.ValidationError("Unable to log in with provided credentials.")
            except Exception as e:
                logger.error(f"Unexpected error occurred while fetching user: {str(e)}")
                raise serializers.ValidationError("An unexpected error occurred. Please try again later.")

            try:
                user = authenticate(username=user.username, password=password)
                if user:
                    if not user.is_active:
                        logger.warning(f"Login attempt failed: User account {email} is disabled.")
                        raise serializers.ValidationError("User account is disabled.")
                else:
                    logger.warning(f"Login attempt failed: Incorrect password for email {email}.")
                    raise serializers.ValidationError("Unable to log in with provided credentials.")
            except Exception as e:
                logger.error(f"Unexpected error occurred during authentication: {str(e)}")
                raise serializers.ValidationError("An unexpected error occurred. Please try again later.")
        else:
            logger.warning("Login attempt failed: Email and password must be provided.")
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        logger.info(f"User {email} authenticated successfully.")
        data['user'] = user
        return data