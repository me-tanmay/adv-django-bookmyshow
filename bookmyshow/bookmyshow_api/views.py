from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer, EventSerializer, BookingSerializer, PaymentSerializer
from .models import Event, Booking, Payment
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger("bookmyshow_api")

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"User {user.email} registered successfully.")
                return Response({
                    'message': 'User registered successfully',
                    'user_id': user.pk
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Unexpected error occurred during registration: {str(e)}")
                return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Registration attempt failed with data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {user.email} logged in successfully.")
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Login attempt failed with data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                logger.warning("Logout attempt failed: No refresh token provided.")
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.email} logged out successfully.")
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error occurred during logout: {str(e)}")
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            try:
                event = serializer.save(created_by=request.user)
                logger.info(f"Event {event.name} created successfully by {request.user.email}.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Unexpected error occurred during event creation: {str(e)}")
                return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Event creation attempt failed with data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BookingView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                booking = serializer.save(user=request.user)
                logger.info(f"Booking for event {booking.event.name} created successfully by {request.user.email}.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Unexpected error occurred during booking creation: {str(e)}")
                return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Booking creation attempt failed with data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        payments = Payment.objects.filter(booking__user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payment = serializer.save()
                logger.info(f"Payment for booking {payment.booking.event.name} created successfully by {payment.booking.user.email}.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Unexpected error occurred during payment creation: {str(e)}")
                return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Payment creation attempt failed with data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        