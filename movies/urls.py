from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCastView


urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('<slug:slug>/cast/', MovieCastView.as_view(), name='movie-cast'),
]
