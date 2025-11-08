"""
IP-based rate limiting utilities for Django views.
Prevents abuse by limiting requests from the same IP address.
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from datetime import timedelta


def rate_limit_by_ip(max_requests=10, window_seconds=60):
    """
    Decorator to rate limit views based on IP address.
    
    Args:
        max_requests: Maximum number of requests allowed in the time window
        window_seconds: Time window in seconds
        
    Usage:
        @rate_limit_by_ip(max_requests=5, window_seconds=60)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Get client IP
            client_ip = getattr(request, 'client_ip', request.META.get('REMOTE_ADDR', ''))
            
            # Create cache key
            cache_key = f'rate_limit:{client_ip}:{view_func.__name__}'
            
            # Get current request count
            request_count = cache.get(cache_key, 0)
            
            if request_count >= max_requests:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please try again later.',
                    'retry_after': window_seconds
                }, status=429)
            
            # Increment counter
            if request_count == 0:
                # First request - set with expiry
                cache.set(cache_key, 1, window_seconds)
            else:
                # Increment existing counter
                cache.incr(cache_key)
            
            # Call the view
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


# Simple in-memory rate limiter (no cache backend required)
class SimpleRateLimiter:
    """
    Simple in-memory rate limiter using a dictionary.
    Note: This won't work across multiple processes/servers.
    For production, use Django cache with Redis backend.
    """
    _storage = {}
    
    @classmethod
    def is_rate_limited(cls, ip_address, max_requests=10, window_seconds=60):
        """
        Check if an IP address has exceeded the rate limit.
        
        Returns:
            bool: True if rate limited, False otherwise
        """
        from time import time
        
        current_time = time()
        key = f"{ip_address}:{window_seconds}"
        
        if key not in cls._storage:
            cls._storage[key] = {'count': 1, 'reset_at': current_time + window_seconds}
            return False
        
        entry = cls._storage[key]
        
        # Check if window has expired
        if current_time > entry['reset_at']:
            entry['count'] = 1
            entry['reset_at'] = current_time + window_seconds
            return False
        
        # Increment counter
        entry['count'] += 1
        
        # Check limit
        return entry['count'] > max_requests
