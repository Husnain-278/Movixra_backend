from django.urls import path
from .views import ScreenListView, ScreenDetailView

urlpatterns = [
    path('',ScreenListView.as_view()),
    path('<slug:slug>/', ScreenDetailView.as_view()),
]
