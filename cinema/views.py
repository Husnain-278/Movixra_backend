from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from movies.models import Movie
from cinema.models import Show
from movies.serializers import MovieListSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import AvailableShowsSerializer


class AvailableMoviesView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


class AvailableShowsView(APIView):

    def get(self, request, movie_slug):

        try:
            movie = Movie.objects.get(slug=movie_slug)

        except Movie.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Movie not found.",
                    "errors": None,
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        shows = Show.objects.filter(
            movie__slug=movie_slug,
            is_active=True
        )

        serializer = AvailableShowsSerializer(
            shows,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Available shows fetched successfully.",
                "errors": None,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )