from django.db import models
from cinema.models import Show,Seat
import uuid
from django.utils import timezone
from datetime import timedelta

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    booking_id = models.UUIDField(default=uuid.uuid4)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="bookings")
    customer_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', db_index=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.customer_email} - {self.show}"
    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)

        super().save(*args, **kwargs)
    
    

class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booked_seats")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="booked_seats")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="booked_seats")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['show', 'seat']

    def __str__(self):
        return f"{self.seat} - {self.show}"