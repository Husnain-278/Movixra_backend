from django.db import models
from booking.models import Booking
# Create your models here.


class Payment(models.Model):
    STATUS_CHOICES =(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    )
    
    PAYMENT_METHOD_CHOICES=(
        ('paypal','Paypal'),
    )
    booking = models.OneToOneField(Booking, on_delete= models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=12, choices=PAYMENT_METHOD_CHOICES, default='paypal')
    paypal_order_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.status}"
