from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import BookingCreateSerializer, BookingListSerializer, RoomSerializer


class RoomCreateView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        return Response({'room_id': room.id}, status=status.HTTP_201_CREATED)


class RoomListView(APIView):
    def get(self, request):
        """
        GET /rooms/list?sort_by=price|created_at&order=asc|desc
        sort_by:
          - price      > price_per_night
          - created_at > time_create
        """
        sort_by = request.query_params.get('sort_by', 'created_at')
        order = request.query_params.get('order', 'asc')

        if sort_by == 'price':
            field_name = 'price_per_night'
        else:
            field_name = 'time_create'

        if order == 'desc':
            field_name = f'-{field_name}'

        rooms = Room.objects.all().order_by(field_name)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDeleteView(APIView):
    def delete(self, request, room_id: int):
        """
        DELETE /rooms/delete/<room_id>
        Удаляет комнату и все её брони (через CASCADE).
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {'error': 'room not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        room.delete()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class BookingCreateView(APIView):
    def post(self, request):
        """
        POST /bookings/create
        body: { "room_id": <int>, "date_start": "YYYY-MM-DD", "date_end": "YYYY-MM-DD" }
        """
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)


class BookingListView(APIView):
    def get(self, request):
        """
        GET /bookings/list?room_id=<id>
        """
        room_id = request.query_params.get('room_id')

        if not room_id:
            return Response(
                {'error': 'room_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bookings = Booking.objects.filter(room_id=room_id).order_by('date_start')
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingDeleteView(APIView):
    def delete(self, request, booking_id: int):
        """
        DELETE /bookings/delete/<booking_id>
        """
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'booking not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        booking.delete()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
