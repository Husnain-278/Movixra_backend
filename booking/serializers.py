from rest_framework import serializers
from .models import BookedSeat, Booking
from cinema.models import Seat
from django.db import transaction

class BookedSeatSerializer(serializers.ModelSerializer):
    seat_number = serializers.SerializerMethodField()
    def get_seat_number(self, obj):
        return f"{obj.seat.row}{obj.seat.number}"
    class Meta:
        model = BookedSeat
        fields= [
            'id',
            'seat',
            'seat_number',
            'price'
        ]
        read_only_fields = fields
        
        
class BookingSerializer(serializers.ModelSerializer):
    
    booked_seats = BookedSeatSerializer(many=True, read_only = True)
    show_slug = serializers.CharField( source="show.slug",read_only=True)
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'customer_email',
            'total_amount',
            'status',
            'show_slug',
            'created_at',
            'booked_seats'
        ]
        
        
    
class CreateBookingSerializer(serializers.Serializer):
    customer_email = serializers.EmailField()
    seat_ids = serializers.ListField(child= serializers.IntegerField(),allow_empty= False)

    def validate_seat_ids(self, value):
        unique_seats = set(value)
        if len(unique_seats) != len(value):
            raise serializers.ValidationError("Duplicate seats are not allowed.")
        return value
    
    def validate(self, attrs):
        show = self.context.get('show')
        seat_ids = attrs.get('seat_ids')
        
        #Checks seats are unique
        seats = Seat.objects.filter(id__in= seat_ids)
        if seats.count() != len(seat_ids):
            raise serializers.ValidationError("one or more seats are invalid.")
        
        #Checkts seats are available
        already_booked = BookedSeat.objects.filter(show = show, seat_id__in= seat_ids).exists()
        if already_booked:
            raise serializers.ValidationError("One or more seats are already booked.")
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        show = self.context.get('show')
        seat_ids = validated_data.get('seat_ids')
        seats = Seat.objects.filter(id__in = seat_ids)
        total_amount = sum(seat.seat_type.price for seat in seats)
        
        booking = Booking.objects.create(
            show = show,
            customer_email = validated_data.get('customer_email'),
            total_amount = total_amount,
            status = 'pending'
        )
        
        booked_seats = []
        for seat in seats:
            booked_seats.append(
                BookedSeat(
                booking = booking, 
                show = show,
                seat = seat,
                price = seat.seat_type.price
                )
            )
        BookedSeat.objects.bulk_create(booked_seats)
        return booking
    
    

class ShowSeatSerializer(serializers.ModelSerializer):
     
    seat_number = serializers.SerializerMethodField()
    seat_type = serializers.CharField(source='seat_type.name')
    price = serializers.DecimalField(source = 'seat_type.price', max_digits=10,decimal_places=2)
    is_booked = serializers.SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = [
            'id',
            'seat_number', 
            'seat_type',
            'price',
            'is_booked'
        ]
    
    def get_seat_number(self, obj):
        return f"{obj.row}{obj.number}"
    
    def get_is_booked(self, obj):
        booked_seat_ids = self.context.get('booked_seat_ids', [])
        return obj.id in booked_seat_ids