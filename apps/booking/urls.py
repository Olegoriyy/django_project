from django.urls import path

from .views import BookingApiView, HealthCheck, RoomApiView

urlpatterns = [
    # Rooms endpoints
    path('rooms/api/', RoomApiView.as_view()),
    path('rooms/api/<int:pk>/', RoomApiView.as_view()),
    # Bookings endpoints
    path('booking/api/', BookingApiView.as_view()),
    path('booking/api/<int:pk>/', BookingApiView.as_view()),
    # Health check
    path('health_check/', HealthCheck.as_view()),
]
