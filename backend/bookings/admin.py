from django.contrib import admin
from .models import ParkingLot, Slot, Booking


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'total_slots']


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'slot_number', 'parking_lot', 'is_active']
    list_filter = ['parking_lot']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'slot', 'date', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'date']