from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Event, Booking, Payment
from rest_framework_simplejwt.tokens import RefreshToken

class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testpassword',
            'role': 'user'
        }
        self.event_manager_data = {
            'email': 'eventmanager@example.com',
            'name': 'Event Manager',
            'username': 'eventmanager',
            'password': 'testpassword',
            'role': 'event_manager'
        }

    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'testuser@example.com')

    def test_login_user(self):
        self.client.post(reverse('register'), self.user_data, format='json')
        url = reverse('login')
        response = self.client.post(url, {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_logout_user(self):
        self.client.post(reverse('register'), self.user_data, format='json')
        login_response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        refresh_token = login_response.data['refresh_token']
        url = reverse('logout')
        response = self.client.post(url, {'refresh_token': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EventTests(APITestCase):

    def setUp(self):
        self.event_manager = CustomUser.objects.create_user(
            email='eventmanager@example.com',
            name='Event Manager',
            username='eventmanager',
            password='testpassword',
            role='event_manager'
        )
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            username='testuser',
            password='testpassword',
            role='user'
        )
        self.event_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date': '2023-12-31T23:59:59Z',
            'location': 'Test Location',
            'category': 'music'
        }
        self.client.force_authenticate(user=self.event_manager)

    def test_create_event(self):
        url = reverse('events')
        response = self.client.post(url, self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().name, 'Test Event')

    def test_filter_events(self):
        Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date='2023-12-31T23:59:59Z',
            location='Test Location',
            category='music',
            created_by=self.event_manager
        )
        url = reverse('events')
        response = self.client.get(url, {'location': 'Test Location'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class BookingTests(APITestCase):

    def setUp(self):
        self.event_manager = CustomUser.objects.create_user(
            email='eventmanager@example.com',
            name='Event Manager',
            username='eventmanager',
            password='testpassword',
            role='event_manager'
        )
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            username='testuser',
            password='testpassword',
            role='user'
        )
        self.event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date='2023-12-31T23:59:59Z',
            location='Test Location',
            category='music',
            created_by=self.event_manager
        )
        self.booking_data = {
            'event': self.event.id,
            'number_of_tickets': 2
        }
        self.client.force_authenticate(user=self.user)

    def test_create_booking(self):
        url = reverse('bookings')
        response = self.client.post(url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().event.name, 'Test Event')

class PaymentTests(APITestCase):

    def setUp(self):
        self.event_manager = CustomUser.objects.create_user(
            email='eventmanager@example.com',
            name='Event Manager',
            username='eventmanager',
            password='testpassword',
            role='event_manager'
        )
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            username='testuser',
            password='testpassword',
            role='user'
        )
        self.event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date='2023-12-31T23:59:59Z',
            location='Test Location',
            category='music',
            created_by=self.event_manager
        )
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            number_of_tickets=2
        )
        self.payment_data = {
            'booking': self.booking.id,
            'amount': 100.00,
            'status': 'completed'
        }
        self.client.force_authenticate(user=self.user)

    def test_create_payment(self):
        url = reverse('payments')
        response = self.client.post(url, self.payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().booking.event.name, 'Test Event')