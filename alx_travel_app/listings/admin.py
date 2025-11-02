from django.contrib import admin
from alx_travel_app.listings.models import Listing, Booking, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_per_night', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('id', 'created_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date', 'created_at')
    search_fields = ('user__username', 'listing__title')
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'start_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'comment')
    readonly_fields = ('id', 'created_at')
