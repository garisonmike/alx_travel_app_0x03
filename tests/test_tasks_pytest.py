from alx_travel_app.listings.tasks import send_booking_confirmation_email

def test_task_is_registered():
    # basic smoke test that the task function is present and has delay
    assert hasattr(send_booking_confirmation_email, 'delay')
    assert callable(send_booking_confirmation_email)
