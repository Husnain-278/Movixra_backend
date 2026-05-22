from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCastView


urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('movies/<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<slug:slug>/cast/', MovieCastView.as_view(), name='movie-cast'),
]
