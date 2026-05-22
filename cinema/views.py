from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Screen
from .serializers import ScreenListSerializer, ScreenDetailSerializer
# Create your views here.

class ScreenListView(ListAPIView):
    queryset = Screen.objects.select_related('cinema').all()
    serializer_class = ScreenListSerializer
    
    
class ScreenDetailView(RetrieveAPIView):
    queryset = Screen.objects.select_related('cinema').prefetch_related('seats').all()
    serializer_class  = ScreenDetailSerializer
    lookup_field = 'slug'