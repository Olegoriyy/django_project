from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['is_active', 'created_at', 'id']
        extra_kwargs = {
            'title': {'allow_blank': False},
            'price_per_night': {'max_value': 10000},
        }


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, attrs):
        pk = attrs.get('pk') or getattr(self.instance, 'pk', None)
        room = attrs.get('room') or getattr(self.instance, 'room', None)
        start = attrs.get('start_date') or getattr(self.instance, 'start_date', None)
        end = attrs.get('end_date') or getattr(self.instance, 'end_date', None)
        if start >= end:
            raise serializers.ValidationError({
                'end_date': 'Дата выезда должна быть позже даты заезда.'
            })
        # Проверяем бронирования на пересечения
        qs = Booking.objects.filter(
            room=room,
            start_date__lt=end,
            end_date__gt=start,
        )
        # при обновлении бронирования, исключаем саму себя
        if pk:
            qs = qs.exclude(pk=pk)

        if qs.exists():
            raise serializers.ValidationError('Номер уже забронирован на эти даты.')

        return attrs
