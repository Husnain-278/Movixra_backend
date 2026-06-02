from django.urls import path
from .views import CreatePaymentAPIView


urlpatterns = [
    path(
        'create/<uuid:booking_id>/',
        CreatePaymentAPIView.as_view(),
        name='create-payment'
    ),
]