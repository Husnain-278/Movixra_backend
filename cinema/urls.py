from django.urls import path
from .views import AvailableMoviesView, AvailableShowsView

urlpatterns = [
   path('movies/', AvailableMoviesView.as_view()),
   path('movies/<slug:movie_slug>/available-shows/', AvailableShowsView.as_view()),
]
