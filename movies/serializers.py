from .models import Movie, Genre, Actor, Cast
from rest_framework import serializers

class GenreSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
        

class ActorSerializer(serializers.ModelSerializer): 
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Actor
        fields = ['id', 'name', 'slug', 'bio', 'birth_date', 'photo']
        
    #Function to get the full URL of the photo
    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
    
    
class MovieListSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'poster', 'rating', 'duration_minutes', 'genres', 'language']
        
    def get_poster(self, obj):
        if obj.poster:
            return obj.poster.url
        return None
    
    
class CastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    
    class Meta:
        model = Cast
        fields = ['id', 'actor', 'role_name']
        
        
class MovieDetailSerializer(serializers.ModelSerializer):       
    poster = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, read_only=True)    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'description', 'poster', 'trailer_url', 'rating', 'release_date', 'duration_minutes', 'genres', 'language']
        
    def get_poster(self, obj):
        if obj.poster:
            return obj.poster.url
        return None
    

class MovieCastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    
    class Meta:
        model = Cast
        fields = ['id', 'actor', 'role_name']