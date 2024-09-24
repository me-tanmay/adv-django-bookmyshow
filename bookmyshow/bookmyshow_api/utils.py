from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(user):
    subject = 'Welcome to BookMyShow'
    message = f'Hi {user.first_name},\n\nThank you for registering at BookMyShow.'
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_booking_confirmation_email(booking):
    subject = 'Booking Confirmation'
    message = f'Hi {booking.user.first_name},\n\nYour booking for {booking.event.name} has been confirmed.'
    recipient_list = [booking.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_event_update_email(event, user):
    subject = 'Event Update'
    message = f'Hi {user.first_name},\n\nThe event {event.name} has been updated.'
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)