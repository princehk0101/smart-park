from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Slot, Booking
from .serializers import SlotSerializer, BookingSerializer



#  AVAILABLE SLOT CHECK 
class AvailableSlotsView(APIView):

    def get(self, request, lot_id):

        date = request.GET.get('date')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        # all active slots
        slots = Slot.objects.filter(parking_lot_id=lot_id, is_active=True)

        # overlapping booking logic 
        booked_slots = Booking.objects.filter(
            slot__parking_lot_id=lot_id,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='BOOKED'
        ).values_list('slot_id', flat=True)

        available_slots = slots.exclude(id__in=booked_slots)

        return Response(SlotSerializer(available_slots, many=True).data)



class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        slot_id = request.data.get('slot')
        vehicle_number = request.data.get('vehicle_number')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # 1️⃣ required field validation
        if not slot_id:
            return Response({"error": "slot is required"}, status=400)

        if not vehicle_number:
            return Response({"error": "vehicle number is required"}, status=400)

        if not date or not start_time or not end_time:
            return Response({"error": "date, start_time and end_time required"}, status=400)

        # 2️⃣ slot existence check
        try:
            slot = Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            return Response({"error": "Invalid slot id"}, status=404)

        # 3️⃣ slot already booked?
        conflict = Booking.objects.filter(
            slot=slot,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='BOOKED'
        ).exists()

        if conflict:
            return Response(
                {"error": "This slot is already booked for selected time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🚗 same vehicle double booking check
        vehicle_conflict = Booking.objects.filter(
            vehicle_number=vehicle_number,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='BOOKED'
        ).exists()

        if vehicle_conflict:
            return Response(
                {"error": "This vehicle already has an active booking in that time"},
                status=400
            )

        # 4️⃣ create booking
        booking = Booking.objects.create(
            user=request.user,
            slot=slot,
            vehicle_number=vehicle_number,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        return Response({
            "message": "Booking successful",
            "booking_id": booking.id,
            "slot_number": slot.slot_number,
            "vehicle_number": booking.vehicle_number
        }, status=201)



# CANCEL BOOKING
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        if booking.status != "BOOKED":
            return Response({"error": "Booking already closed"}, status=400)

        booking.status = "CANCELLED"
        booking.save()

        return Response({"message": "Booking cancelled successfully"})


# USER BOOKING HISTORY
class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        return Response(BookingSerializer(bookings, many=True).data)