from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alx_travel_app.listings.views import ListingViewSet, BookingViewSet, ReviewViewSet
from . import views

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("initiate-payment/", views.initiate_payment, name="initiate-payment"),  # type: ignore
    path("verify-payment/", views.verify_payment, name="verify-payment"),  # type: ignore
]