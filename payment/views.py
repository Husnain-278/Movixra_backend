from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from booking.models import Booking
from .models import Payment

from .services.paypal import create_paypal_order


class CreatePaymentAPIView(APIView):

    def post(self, request, booking_id):

        try:
            booking = Booking.objects.get(
                booking_id=booking_id
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.status != 'pending':

            return Response(
                {
                    "success": False,
                    "message": "Booking is not pending."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        paypal_response = create_paypal_order(booking)

        paypal_order_id = paypal_response.get('id')

        approval_url = None

        for link in paypal_response.get('links', []):

            if link['rel'] == 'approve':
                approval_url = link['href']
                break

        payment = Payment.objects.create(
            booking=booking,
            paypal_order_id=paypal_order_id,
            amount=booking.total_amount,
        )

        return Response(
            {
                "success": True,
                "approval_url": approval_url,
                "paypal_order_id": paypal_order_id,
            },
            status=status.HTTP_201_CREATED
        )