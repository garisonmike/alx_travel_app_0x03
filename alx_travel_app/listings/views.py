from rest_framework import viewsets
from alx_travel_app.listings.models import Listing, Booking, Review
from alx_travel_app.listings.serializers import ListingSerializer, BookingSerializer, ReviewSerializer
import os
import requests
from django.http import JsonResponse
from .models import Payment
from django.views.decorators.csrf import csrf_exempt

class ListingViewSet(viewsets.ModelViewSet):
    """CRUD API for Listings"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """CRUD API for Bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD API for Reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify"

@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        booking_reference = request.POST.get("booking_reference")
        amount = request.POST.get("amount")

        if not booking_reference or not amount:
            return JsonResponse({"error": "Missing booking_reference or amount"}, status=400)

        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
        payload = {
            "amount": amount,
            "currency": "ETB",
            "tx_ref": f"txn_{booking_reference}",
            "callback_url": "http://localhost:8000/verify-payment/",
            "return_url": "http://localhost:8000/payment-success/",
            "customization": {"title": "Travel Booking Payment"},
        }

        response = requests.post(chapa_url, headers=headers, json=payload)
        data = response.json()

        if data.get("status") == "success":
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=data["data"]["tx_ref"],
                status="Pending",
            )
            return JsonResponse({
                "checkout_url": data["data"]["checkout_url"],
                "transaction_id": data["data"]["tx_ref"]
            })

        return JsonResponse({"error": "Payment initiation failed", "details": data}, status=400)

    # If it's not POST, just return a message
    return JsonResponse({"message": "Send a POST request to initiate payment."})


@csrf_exempt
def verify_payment(request):
    """Verify payment status with Chapa"""
    if request.method == "GET":
        tx_ref = request.GET.get("tx_ref")
        
        if not tx_ref:
            return JsonResponse({"error": "Missing transaction reference"}, status=400)
        
        headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
        verify_url = f"{CHAPA_VERIFY_URL}/{tx_ref}"
        
        response = requests.get(verify_url, headers=headers)
        data = response.json()
        
        if data.get("status") == "success":
            # Update payment status in database
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                payment.status = "Completed"
                payment.save()
                
                return JsonResponse({
                    "message": "Payment verified successfully",
                    "transaction_id": tx_ref,
                    "status": "Completed"
                })
            except Payment.DoesNotExist:
                return JsonResponse({
                    "error": "Payment record not found",
                    "transaction_id": tx_ref
                }, status=404)
        
        return JsonResponse({
            "error": "Payment verification failed",
            "details": data
        }, status=400)
    
    return JsonResponse({"message": "Send a GET request with tx_ref to verify payment."})