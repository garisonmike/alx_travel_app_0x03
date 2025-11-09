from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Listing, Booking
from unittest.mock import patch, MagicMock

User = get_user_model()

class BookingIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass')
        self.listing = Listing.objects.create(
            title='Test listing', 
            description='desc', 
            price_per_night=100,
            location='Test Location'
        )

    @patch('alx_travel_app.listings.views.send_booking_confirmation_email')
    def test_create_booking_triggers_task(self, mock_send_email):
        """Test that creating a booking through the API triggers the email task"""
        # Mock the task to return immediately (not delay)
        mock_send_email.return_value = MagicMock()
        
        # Log in the user
        self.client.force_login(self.user)

        response = self.client.post('/api/bookings/', {
            'listing': str(self.listing.pk),
            'user': self.user.pk,
            'start_date': '2025-12-01',
            'end_date': '2025-12-05'
        })
        
        # We expect 201 Created for the viewset
        self.assertIn(response.status_code, (200, 201), f"Got status {response.status_code}: {response.content}")

        # Ensure a booking exists
        booking = Booking.objects.filter(user=self.user, listing=self.listing).first()
        self.assertIsNotNone(booking, "Booking was not created")
        assert booking is not None

        # Ensure the task was called
        self.assertTrue(mock_send_email.called, "Email task was not called")
        # Verify it was called with the correct arguments
        mock_send_email.assert_called_once_with(self.user.email, booking.id)
