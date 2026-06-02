from django.contrib import admin
from .models import Cinema, Screen, Seat, SeatType, Show


class SeatInline(admin.TabularInline):
	model = Seat
	fields = ("row", "number", "seat_type", "is_active", "created_at")
	readonly_fields = ("created_at",)
	extra = 0
	ordering = ("row", "number")


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
	list_display = ("name", "city", "is_active", "created_at")
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "city")
	list_filter = ("city", "is_active")


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
	list_display = ("name", "cinema", "capacity", "slug", "created_at")
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "cinema__name")
	list_filter = ("cinema",)
	inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
	list_display = ("screen", "row", "number", "seat_type", "is_active", "created_at")
	list_filter = ("seat_type", "is_active", "screen__cinema")
	search_fields = ("screen__name", "row", "number")


@admin.register(SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "seat_count")
	search_fields = ("name",)

	def seat_count(self, obj):
		return obj.seats.count()
	seat_count.short_description = "Seats"


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
	list_display = ("movie", "screen", "format_type", "show_date", "start_time", "end_time", "is_active", "created_at")
	list_filter = ("format_type", "show_date", "is_active", "screen__cinema")
	search_fields = ("movie__title", "screen__name")
	readonly_fields = ("created_at",)

