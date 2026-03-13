from django.urls import path
from .views import AvailableSlotsView, CreateBookingView
from .views import AvailableSlotsView, CreateBookingView, CancelBookingView, MyBookingsView


urlpatterns = [
    path('available-slots/<int:lot_id>/', AvailableSlotsView.as_view()),
    path('create-booking/', CreateBookingView.as_view()),
    path('cancel/<int:booking_id>/', CancelBookingView.as_view()),
    path('my-bookings/', MyBookingsView.as_view()),
]