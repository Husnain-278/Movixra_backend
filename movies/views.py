from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Cast
from .serializers import MovieDetailSerializer, MovieListSerializer, MovieCastSerializer
from .pagination import MoviePagination
# Create your views here.


class MovieListView(generics.ListAPIView):
    pagination_class = MoviePagination
    
    def get_queryset(self):
        return  Movie.objects.all().prefetch_related('genres')
    
    serializer_class = MovieListSerializer
        
        
class MovieDetailView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            Movie.objects
            .all()
            .prefetch_related(
                'genres',
                'casts__actor'
            )
        )
        
        


class MovieCastView(generics.ListAPIView):  
    serializer_class = MovieCastSerializer
    
    def get_queryset(self):
        movie_slug = self.kwargs['slug']
        return Cast.objects.filter(movie__slug=movie_slug).select_related('actor')