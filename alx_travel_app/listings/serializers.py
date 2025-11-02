#!/usr/bin/env python3
"""
Serializers for travel app models.
They transform Django model instances into JSON responses for APIs.
"""

from rest_framework import serializers
from alx_travel_app.listings.models import Listing, Booking, Review


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model.
    Converts a Listing object → JSON.
    """
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price_per_night', 'location', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    Converts a Booking object → JSON.
    """
    class Meta:
        model = Booking
        fields = ['id', 'user', 'listing', 'start_date', 'end_date', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    Converts a Review object → JSON.
    """
    class Meta:
        model = Review
        fields = ['id', 'user', 'listing', 'rating', 'comment', 'created_at']
