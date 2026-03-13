from rest_framework import serializers
from .models import ParkingLot, Slot


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class ParkingLotSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta:
        model = ParkingLot
        fields = '__all__'