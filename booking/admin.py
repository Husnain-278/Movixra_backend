from django.contrib import admin
from .models import Booking, BookedSeat


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ("booking_id", "customer_email", "show", "status", "total_amount", "created_at")
	search_fields = ("booking_id", "customer_email")
	list_filter = ("status", "created_at")
	readonly_fields = ("created_at", "updated_at")


@admin.register(BookedSeat)
class BookedSeatAdmin(admin.ModelAdmin):
	list_display = ("booking", "show", "seat", "price", "booked_at")
	search_fields = ("booking__booking_id", "show__slug", "seat__row", "seat__number")
	list_filter = ("show", "booked_at")
	readonly_fields = ("booked_at",)
