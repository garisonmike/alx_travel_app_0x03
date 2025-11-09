from django.test import RequestFactory, SimpleTestCase
from alx_travel_app.middleware import get_client_ip, IPTrackingMiddleware


class TestIPTracking(SimpleTestCase):
    """Test IP address tracking middleware and utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
    
    def test_get_client_ip_from_x_forwarded_for(self):
        """Test IP extraction from X-Forwarded-For header (proxy scenario)."""
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.195, 70.41.3.18, 150.172.238.178'
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.195'  # Should get the first IP (client)
    
    def test_get_client_ip_from_x_real_ip(self):
        """Test IP extraction from X-Real-IP header."""
        request = self.factory.get('/')
        request.META['HTTP_X_REAL_IP'] = '198.51.100.42'
        
        ip = get_client_ip(request)
        assert ip == '198.51.100.42'
    
    def test_get_client_ip_from_remote_addr(self):
        """Test IP extraction from REMOTE_ADDR (direct connection)."""
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.0.2.1'
        
        ip = get_client_ip(request)
        assert ip == '192.0.2.1'
    
    def test_get_client_ip_priority(self):
        """Test that X-Forwarded-For takes priority over other headers."""
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.1'
        request.META['HTTP_X_REAL_IP'] = '198.51.100.1'
        request.META['REMOTE_ADDR'] = '192.0.2.1'
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.1'
    
    def test_middleware_attaches_ip_to_request(self):
        """Test that middleware attaches client_ip attribute to request."""
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.0.2.100'
        
        # Simple get_response mock
        def get_response(req):
            from django.http import HttpResponse
            return HttpResponse()
        
        middleware = IPTrackingMiddleware(get_response)
        middleware(request)
        
        assert hasattr(request, 'client_ip')
        assert getattr(request, 'client_ip', None) == '192.0.2.100'
