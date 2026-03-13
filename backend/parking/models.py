from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        unique_together = ('parking_lot', 'slot_number')

    def __str__(self):
        return f"{self.parking_lot.name} - {self.slot_number}"


# AUTO SLOT CREATION
@receiver(post_save, sender=ParkingLot)
def create_slots(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.total_slots + 1):
            Slot.objects.create(
                parking_lot=instance,
                slot_number=f"S{i}"
            )