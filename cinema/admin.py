from django.contrib import admin
from .models import Cinema, Screen, Seat


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

