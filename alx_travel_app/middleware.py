"""
IP tracking middleware and utility for Django.
Captures client IP addresses from requests, handling proxy/load balancer headers.
"""


def get_client_ip(request):
    """
    Extract the client's real IP address from the request.
    Handles X-Forwarded-For and X-Real-IP headers for proxy/load balancer scenarios.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        str: Client IP address
    """
    # Check for X-Forwarded-For header (comma-separated list, first is client)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take the first IP in the chain (client IP)
        ip = x_forwarded_for.split(',')[0].strip()
        return ip
    
    # Check for X-Real-IP header (single IP)
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        return x_real_ip.strip()
    
    # Fallback to REMOTE_ADDR (direct connection)
    return request.META.get('REMOTE_ADDR', '')


class IPTrackingMiddleware:
    """
    Middleware to attach client IP address to every request object.
    Usage: request.client_ip will contain the client's IP address.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Attach client IP to the request object
        request.client_ip = get_client_ip(request)
        response = self.get_response(request)
        return response
