from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer
import logging

logger = logging.getLogger("bookmyshow_api")

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