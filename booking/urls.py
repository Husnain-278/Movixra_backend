from django.urls import path
from .views import CreateBookingAPIView, ShowSeatsView

urlpatterns = [
    path(
        "shows/<slug:slug>/book/",
        CreateBookingAPIView.as_view(),
        name="create-booking"
    ),
    path(
    'shows/<slug:slug>/seats/',
    ShowSeatsView.as_view(),
    name='show-seats'
),
]