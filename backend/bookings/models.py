from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# PARKING LOT 
class ParkingLot(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=255)
    total_slots = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.location})"


# SLOT 
class Slot(models.Model):
    parking_lot = models.ForeignKey(
        ParkingLot,
        on_delete=models.CASCADE,
        related_name="slots"
    )

    slot_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        # prevents duplicate A1,A1 inside same parking
        unique_together = ('parking_lot', 'slot_number')

    def __str__(self):
        return f"{self.parking_lot.name} - {self.slot_number}"


# BOOKING 
# BOOKING 
class Booking(models.Model):

    STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="slot_bookings"
    )

    #  NEW FIELD
    vehicle_number = models.CharField(max_length=15)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='BOOKED'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # validation
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.user} | {self.slot.slot_number} | {self.vehicle_number} | {self.date}"