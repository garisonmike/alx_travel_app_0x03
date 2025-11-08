from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Listing, Booking
from unittest.mock import patch

User = get_user_model()

class BookingIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass')
        self.listing = Listing.objects.create(title='Test listing', description='desc', price=100)

    @patch('alx_travel_app.listings.tasks.send_booking_confirmation_email')
    def test_create_booking_triggers_task(self, mock_send_email):
        # Log in the user
        self.client.force_login(self.user)

        response = self.client.post('/api/bookings/', {
            'listing': self.listing.pk,
            'user': self.user.pk,
            'start_date': '2025-12-01',
            'end_date': '2025-12-05'
        })
        # We expect 201 Created for the viewset
        self.assertIn(response.status_code, (200, 201))

        # Ensure a booking exists
        booking = Booking.objects.filter(user=self.user, listing=self.listing).first()
        self.assertIsNotNone(booking)

        # The task should be referenced (mocked) and not actually send an email
        self.assertTrue(mock_send_email.called)
