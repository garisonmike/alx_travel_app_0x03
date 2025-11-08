# IP Tracking Documentation

## Overview

The ALX Travel App includes comprehensive IP address tracking to monitor user activity, prevent abuse, and provide security analytics.

## Features

### 1. IP Capture Middleware

**Location:** `alx_travel_app/middleware.py`

The `IPTrackingMiddleware` automatically captures client IP addresses from every request, handling:
- Direct connections (`REMOTE_ADDR`)
- Proxy/load balancer scenarios (`X-Forwarded-For`, `X-Real-IP`)

**Usage:**
```python
# In views or anywhere with request object
client_ip = request.client_ip
```

### 2. Database Storage

IP addresses are stored in:
- **Booking model**: Tracks which IP created each booking
- **Payment model**: Tracks which IP initiated each payment

**Fields:**
```python
ip_address = models.GenericIPAddressField(blank=True, null=True)
```

### 3. Admin Interface

IP addresses are visible in Django admin:
- Booking list: Shows IP address column
- Payment list: Shows IP address column
- Searchable by IP address
- Read-only field (automatically captured)

### 4. Rate Limiting (Optional)

**Location:** `alx_travel_app/ratelimit.py`

Provides IP-based rate limiting to prevent abuse:

```python
from alx_travel_app.ratelimit import rate_limit_by_ip

@rate_limit_by_ip(max_requests=10, window_seconds=60)
def my_view(request):
    # This view is rate limited to 10 requests per minute per IP
    ...
```

## Setup

### 1. Run Migration

```bash
python manage.py migrate
```

This creates the `ip_address` fields in the database.

### 2. Middleware Configuration

The middleware is already configured in `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'alx_travel_app.middleware.IPTrackingMiddleware',
]
```

### 3. Docker/Kubernetes

When deploying behind a proxy/load balancer, ensure the proxy forwards the real client IP:

**Nginx example:**
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

**Kubernetes Ingress:**
```yaml
nginx.ingress.kubernetes.io/use-forwarded-headers: "true"
```

## Testing

Run IP tracking tests:

```bash
pytest tests/test_ip_tracking.py -v
```

Tests verify:
- IP extraction from X-Forwarded-For
- IP extraction from X-Real-IP
- IP extraction from REMOTE_ADDR
- Header priority order
- Middleware attachment to request

## Security Considerations

### Privacy

IP addresses are personal data under GDPR. Ensure:
1. Privacy policy discloses IP tracking
2. Data retention policies are followed
3. User consent is obtained where required

### Anonymization

For analytics, consider anonymizing IPs:

```python
def anonymize_ip(ip):
    """Anonymize IP by zeroing last octet."""
    parts = ip.split('.')
    if len(parts) == 4:
        parts[-1] = '0'
        return '.'.join(parts)
    return ip
```

### Rate Limiting Best Practices

- Set reasonable limits to prevent false positives
- Whitelist known IPs (APIs, monitoring services)
- Use Redis cache backend for distributed systems
- Log rate limit events for security monitoring

## API Response

Booking creation response includes IP (read-only):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user": 1,
  "listing": "456e7890-e12b-34d5-b678-901234567890",
  "start_date": "2025-12-01",
  "end_date": "2025-12-05",
  "ip_address": "203.0.113.195",
  "created_at": "2025-11-08T16:30:00Z"
}
```

## Monitoring & Analytics

### Query Examples

**Find bookings from specific IP:**
```python
Booking.objects.filter(ip_address='203.0.113.195')
```

**Count bookings per IP:**
```python
from django.db.models import Count
Booking.objects.values('ip_address').annotate(count=Count('id')).order_by('-count')
```

**Detect suspicious activity (many bookings from one IP):**
```python
suspicious = Booking.objects.values('ip_address').annotate(
    count=Count('id')
).filter(count__gte=10)
```

## Troubleshooting

### IP shows as 127.0.0.1

**Problem:** All IPs are localhost.

**Solutions:**
1. Check if running behind proxy and headers are forwarded
2. Verify middleware is enabled
3. Check proxy configuration

### Empty IP addresses

**Problem:** `ip_address` field is NULL.

**Solutions:**
1. Ensure middleware is loaded before views
2. Check middleware order in settings
3. Verify views are using `request.client_ip`

## Future Enhancements

Potential additions:
- GeoIP location tracking (country, city)
- IP reputation checking (VPN/proxy detection)
- Automated fraud detection
- Real-time blocking of malicious IPs
- IP whitelisting/blacklisting admin interface
