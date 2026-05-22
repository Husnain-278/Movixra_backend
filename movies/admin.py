from django.contrib import admin
from .models import Movie, Genre, Actor, Cast
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating')
    search_fields = ('title',)
    list_filter = ('release_date', 'rating')
    ordering = ('-release_date',)
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)   
    
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    list_filter = ('birth_date',)
    ordering = ('name',)
    
@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie', 'actor', 'role_name')
    search_fields = ('movie__title', 'actor__name', 'role_name')
    list_filter = ('movie', 'actor')