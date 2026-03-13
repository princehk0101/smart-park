from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ParkingLot
from .serializers import ParkingLotSerializer


class ParkingListCreateView(generics.ListCreateAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer


# PARKING DETAIL 
class ParkingDetailView(generics.RetrieveAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer


# SLOT SUMMARY (TOTAL / ACTIVE) 
class ParkingStatsView(APIView):

    def get(self, request, pk):
        parking = ParkingLot.objects.get(pk=pk)

        total = parking.slots.count()
        active = parking.slots.filter(is_active=True).count()

        return Response({
            "parking_id": parking.id,
            "parking_name": parking.name,
            "total_slots": total,
            "active_slots": active
        })