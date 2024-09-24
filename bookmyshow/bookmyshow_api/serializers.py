import logging
from rest_framework import serializers
from django.contrib.auth import authenticate

from.models import CustomUser, Event, Booking, Payment

logger = logging.getLogger("bookmyshow_api")

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLES, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password', 'role')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            logger.warning(f"Registration attempt failed: Email {value} already exists.")
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                role=validated_data['role']
            )
            logger.info(f"User {user.email} registered successfully.")
            return user
        except Exception as e:
            logger.error(f"Unexpected error occurred during user creation: {str(e)}")
            raise serializers.ValidationError("An unexpected error occurred. Please try again later.")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
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


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Event
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'