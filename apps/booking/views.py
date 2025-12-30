from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class HealthCheck(APIView):
    def get(self, request):
        return Response({'status': 'OK'}, status=200)


class RoomApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            r_object = get_object_or_404(Room, id=pk)
            return Response(RoomSerializer(r_object).data)

        all_objects = RoomSerializer(Room.objects.all(), many=True).data
        return Response({'all_rooms': all_objects}, status=200)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Room created | id': serializer.data['id']}, status=201)

    def put(self, request, pk=None):
        if not pk:
            return Response({'Need room id'})

        n_object = get_object_or_404(Room, id=pk)

        serializer = RoomSerializer(instance=n_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Room updated | id': serializer.data['id']})

    def delete(self, request, pk=None):
        if not pk:
            return Response({'Need room id'})

        d_object = get_object_or_404(Room, id=pk)

        d_object.delete()

        return Response({'Room deleted | id': pk}, status=204)


class BookingApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            r_object = get_object_or_404(Booking, id=pk)
            serializer = BookingSerializer(r_object)

            return Response({'Room {id}': serializer.data})

        all_objects = Booking.objects.all()
        serializer = BookingSerializer(all_objects, many=True)

        return Response({'All bookings:': serializer.data}, status=200)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Booking created | id': serializer.data['id']}, status=201)

    def put(self, request, pk=None):
        if not pk:
            return Response({'Need id for PUT Method'})

        o_object = get_object_or_404(Booking, id=pk)

        serializer = BookingSerializer(instance=o_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Booking updated | id': serializer.data['id']})

    def delete(self, request, pk=None):
        if not pk:
            return Response({'Need booking id'})

        d_object = get_object_or_404(Booking, id=pk)

        d_object.delete()

        return Response({'Booking deleted | id': pk}, status=204)
