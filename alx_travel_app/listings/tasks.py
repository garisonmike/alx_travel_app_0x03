from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    """
    Background task to send booking confirmation emails asynchronously.
    """
    subject = "Booking Confirmation - ALX Travel App"
    message = f"Your booking (ID: {booking_id}) was successfully created. Thank you for choosing us!"
    sender = "no-reply@alxtravelapp.com"

    send_mail(subject, message, sender, [user_email], fail_silently=False)
    return f"Confirmation email sent to {user_email}"
