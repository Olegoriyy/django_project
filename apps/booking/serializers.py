from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Room
        fields = (
            'room_id',
            'room_number',
            'description',
            'price_per_night',
            'time_create',
        )
        read_only_fields = ('room_id', 'time_create')


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',  # важно: связка с полем модели "room"
        write_only=True,
    )

    class Meta:
        model = Booking
        fields = ('room_id', 'date_start', 'date_end')

    def validate(self, attrs):
        """
        Общая валидация: проверяем, что date_start <= date_end.
        """
        date_start = attrs.get('date_start')
        date_end = attrs.get('date_end')

        if date_start and date_end and date_start > date_end:
            raise serializers.ValidationError('date_start Должна быть <= date_end')

        return attrs


class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Booking
        fields = ('booking_id', 'date_start', 'date_end')
