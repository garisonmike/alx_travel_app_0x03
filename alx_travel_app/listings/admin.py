from django.contrib import admin
from alx_travel_app.listings.models import Listing, Booking, Review, Payment


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_per_night', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('id', 'created_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'start_date', 'end_date', 'ip_address', 'created_at')
    list_filter = ('start_date', 'end_date', 'created_at')
    search_fields = ('user__username', 'listing__title', 'ip_address')
    readonly_fields = ('id', 'created_at', 'ip_address')
    date_hierarchy = 'start_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'comment')
    readonly_fields = ('id', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'amount', 'status', 'ip_address', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking_reference', 'chapa_tx_ref', 'ip_address')
    readonly_fields = ('id', 'created_at', 'ip_address')
