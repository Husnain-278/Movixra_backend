from rest_framework.views import APIView
from cinema.models import Show, Seat
from django.shortcuts import get_object_or_404
from .serializers import CreateBookingSerializer, BookingSerializer, ShowSeatSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import BookedSeat
# Create your views here.

class CreateBookingAPIView(APIView):
    def post(self, request, slug):
        show = get_object_or_404(Show, slug = slug, is_active = True)
        serializer = CreateBookingSerializer(data= request.data, context = {'show': show})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        response_serializer = BookingSerializer(booking)
        return Response(
            {
                "success": True,
                "message": "Booking created Successfully. Please do payment within 5 minutes.",
                "errors": None,
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
        

class ShowSeatsView(APIView):
    def get(self, request, slug):
        show = get_object_or_404(
            Show,
            slug= slug,
            is_active = True
        )
        seats = Seat.objects.select_related('seat_type').all().order_by('row', 'number')
        booked_seat_ids = BookedSeat.objects.filter(show= show).values_list('seat_id', flat=True)
        serializer = ShowSeatSerializer(
            seats,
            many= True,
            context = {'booked_seat_ids': booked_seat_ids}
        )
        return Response(
            {
                "success":True,
                "message": "Seat fetched Successfully.",
                "errors": None,
                "data": {
                    "show": show.slug,
                    "hall": show.screen.name,
                    "seats": serializer.data
                }
            },
            status=status.HTTP_200_OK
        )