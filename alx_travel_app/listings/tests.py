from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from alx_travel_app.listings.models import Listing, Booking, Review


class ListingModelTest(TestCase):
    def setUp(self):
        # Use Decimal to mirror the model field and avoid float rounding errors.
        self.listing = Listing.objects.create(
            title="Test Beach House",
            description="A beautiful test property",
            price_per_night=Decimal("100.00"),
            location="Test City"
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.title, "Test Beach House")
        self.assertEqual(self.listing.price_per_night, Decimal("100.00"))
        self.assertIsNotNone(self.listing.id)

    def test_listing_str(self):
        self.assertEqual(str(self.listing), "Test Beach House")


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(
            title="Test Property",
            description="Test description",
            price_per_night=Decimal("150.00"),
            location="Test Location"
        )
        self.booking = Booking.objects.create(
            user=self.user,
            listing=self.listing,
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 5)
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.user.username, 'testuser')
        self.assertEqual(self.booking.listing.title, 'Test Property')
        self.assertIsNotNone(self.booking.id)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reviewer', password='testpass')
        self.listing = Listing.objects.create(
            title="Review Test Property",
            description="Test description",
            price_per_night=Decimal("200.00"),
            location="Test City"
        )
        self.review = Review.objects.create(
            user=self.user,
            listing=self.listing,
            rating=5,
            comment="Excellent stay!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Excellent stay!")
        self.assertIsNotNone(self.review.id)
