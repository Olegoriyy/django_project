from django.urls import path

from .views import *

urlpatterns = [
    # rooms
    path('rooms/create', RoomCreateView.as_view(), name='room-create'),
    path('rooms/list', RoomListView.as_view(), name='room-list'),
    path('rooms/delete/<int:room_id>', RoomDeleteView.as_view(), name='room-delete'),
    # books
    path('bookings/create', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/list', BookingListView.as_view(), name='booking-list'),
    path(
        'bookings/delete/<int:booking_id>',
        BookingDeleteView.as_view(),
        name='booking-delete',
    ),
]
