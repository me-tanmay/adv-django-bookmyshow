from django.urls import path
from .views import LoginView, RegisterView, LogoutView, EventView, BookingView, PaymentView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventView.as_view(), name='event-detail'),
    path('bookings/', BookingView.as_view(), name='bookings'),
    path('payments/', PaymentView.as_view(), name='payments'),
]