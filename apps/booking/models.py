from django.db import models


# Create your models here.
class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    time_create = models.DateField(auto_now_add=True)
    time_update = models.DateField(auto_now=True)

    def __str__(self):
        return f'Room # {self.room_number}, Price: {self.price_per_night} /day'

    class Meta:
        ordering = ['price_per_night']
        indexes = [models.Index(fields=['price_per_night'])]


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking #{self.id} — Room {self.room.id} ({self.date_start} → {self.date_end})'

    class Meta:
        ordering = ['date_start']
