from rest_framework import serializers
from .models import Screen, Seat, Show

class ScreenListSerializer(serializers.ModelSerializer):
    cinema = serializers.CharField(source = 'cinema.name', read_only=True)
    capacity = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Screen
        fields = ['id', 'name', 'cinema', 'image','slug','capacity','created_at']
    
    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        return None
    
    
class SeatSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField(read_only= True)
    
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number','label', 'seat_type', 'is_active']
        
    def get_label(self, obj):
        return f"{obj.row}{obj.number}"

class ScreenDetailSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)
    cinema = serializers.CharField(source = 'cinema.name', read_only=True)
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    class Meta:
        model = Screen
        fields = [
            'id',
            'cinema',
            'name',
            'image',
            'slug', 
            'seats',
            'created_at'
        ]
        
        
        
class AvailableShowsSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source = 'movie.title', read_only=True)
    screen = serializers.CharField(source='screen.name')
    class Meta:
        model = Show
        fields = [
            'movie',
            'screen',
            'slug',
            'format_type', 
            'show_date',
            'start_time', 
            'end_time',
            'is_active'
        ]