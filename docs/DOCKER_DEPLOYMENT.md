# 🐳 Docker Deployment Guide

## Complete Containerization for ALX Travel App

This guide covers deploying the ALX Travel App using Docker and Docker Compose with a full production-ready stack.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Development Setup](#development-setup)
5. [Production Deployment](#production-deployment)
6. [Service Details](#service-details)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Monitoring](#monitoring)

---

## 🏗️ Architecture Overview

The containerized application consists of 6 services:

```
┌─────────────────────────────────────────────────┐
│                   NGINX (Port 80)               │
│              Reverse Proxy & Static             │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│          Django Web App (Port 8000)             │
│         Gunicorn + WhiteNoise                   │
└──┬──────────┬──────────┬──────────┬────────────┘
   │          │          │          │
   │     ┌────▼────┐ ┌───▼────┐ ┌──▼─────┐
   │     │PostgreSQL│ │ Redis  │ │RabbitMQ│
   │     │(Port 5432│ │(Port   │ │(Port   │
   │     │)         │ │6379)   │ │5672)   │
   │     └──────────┘ └────────┘ └────────┘
   │
┌──▼──────────────────┐  ┌──────────────────────┐
│  Celery Worker      │  │   Celery Beat        │
│  (Background Tasks) │  │   (Scheduler)        │
└─────────────────────┘  └──────────────────────┘
```

### Services:

1. **web** - Django application (Gunicorn)
2. **db** - PostgreSQL database
3. **redis** - Redis cache & Celery results
4. **rabbitmq** - Message broker for Celery
5. **worker** - Celery worker processes
6. **beat** - Celery beat scheduler
7. **nginx** (production only) - Reverse proxy

---

## ✅ Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 10GB disk space

### Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install --cask docker
```

**Windows:**
Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

### Verify Installation

```bash
docker --version
docker-compose --version
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/garisonmike/alx_travel_app_0x03.git
cd alx_travel_app_0x03
```

### 2. Create Environment File

```bash
cp .env.example .env
# Edit .env with your values
nano .env
```

### 3. Build and Run

```bash
# Development (with hot reload)
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

### 4. Access Application

- **Web App:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Swagger API:** http://localhost:8000/swagger/
- **RabbitMQ Management:** http://localhost:15672 (guest/guest)

---

## 💻 Development Setup

### Using docker-compose.yml

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (reset database)
docker-compose down -v
```

### Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Run Migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Run Tests

```bash
# All tests
docker-compose exec web pytest

# Specific test
docker-compose exec web pytest tests/test_ip_tracking.py

# Django tests
docker-compose exec web python manage.py test
```

### Access Django Shell

```bash
docker-compose exec web python manage.py shell
```

### Access Database

```bash
docker-compose exec db psql -U alx_user -d alx_travel_db
```

---

## 🏭 Production Deployment

### Using docker-compose.prod.yml

### 1. Configure Environment

Create `.env` file with production values:

```bash
SECRET_KEY=your_production_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/dbname
CHAPA_SECRET_KEY=your_production_chapa_key
POSTGRES_PASSWORD=strong_password_here
REDIS_PASSWORD=strong_redis_password
RABBITMQ_PASS=strong_rabbitmq_password
```

### 2. Build and Deploy

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### 3. Initialize Production

```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 4. Enable HTTPS (Optional)

Add SSL certificates to `nginx/certs/` and update `nginx/conf.d/default.conf`:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    # ... rest of config
}
```

---

## 🔧 Service Details

### Web Service (Django)

- **Image:** Custom (built from Dockerfile)
- **Port:** 8000
- **Command:** `gunicorn alx_travel_app.wsgi:application`
- **Workers:** 3-4 (adjust based on CPU)
- **Health Check:** `/admin/login/`

### Database Service (PostgreSQL)

- **Image:** `postgres:15-alpine`
- **Port:** 5432
- **Volume:** `postgres_data`
- **Credentials:** From `.env`

### Redis Service

- **Image:** `redis:7-alpine`
- **Port:** 6379
- **Volume:** `redis_data`
- **Purpose:** Cache + Celery results

### RabbitMQ Service

- **Image:** `rabbitmq:3-management-alpine`
- **Ports:** 5672 (AMQP), 15672 (Management UI)
- **Volume:** `rabbitmq_data`
- **Purpose:** Celery message broker

### Celery Worker

- **Image:** Custom (same as web)
- **Command:** `celery -A alx_travel_app worker`
- **Concurrency:** 2-4 workers

### Celery Beat

- **Image:** Custom (same as web)
- **Command:** `celery -A alx_travel_app beat`
- **Purpose:** Scheduled periodic tasks

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | ✅ |
| `DEBUG` | Debug mode | `True` | ✅ |
| `ALLOWED_HOSTS` | Allowed hostnames | `*` | ✅ |
| `DATABASE_URL` | PostgreSQL connection | SQLite | ❌ |
| `REDIS_URL` | Redis connection | - | ❌ |
| `CELERY_BROKER_URL` | RabbitMQ URL | - | ✅ |
| `CELERY_RESULT_BACKEND` | Results backend | - | ❌ |
| `CHAPA_SECRET_KEY` | Payment gateway key | - | ✅ |

### Docker Compose Overrides

Create `docker-compose.override.yml` for local customizations:

```yaml
version: '3.8'
services:
  web:
    ports:
      - "8080:8000"
    environment:
      - DEBUG=True
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# View logs
docker-compose logs web

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart web
```

### Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Verify connection
docker-compose exec db pg_isready
```

### Port Already in Use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Or change port in docker-compose.yml
ports:
  - "8080:8000"
```

### Celery Tasks Not Running

```bash
# Check worker logs
docker-compose logs worker

# Check RabbitMQ
docker-compose logs rabbitmq

# Restart worker
docker-compose restart worker
```

### Permission Denied Errors

```bash
# Fix permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up
```

### Reset Everything

```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```

---

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

### Resource Usage

```bash
# View container stats
docker stats

# Disk usage
docker system df
```

### Health Checks

```bash
# Check all services
docker-compose ps

# Web health
curl http://localhost:8000/admin/login/

# RabbitMQ health
curl http://localhost:15672/api/health/checks/alarms
```

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U alx_user alx_travel_db > backup.sql

# Restore
docker-compose exec -T db psql -U alx_user alx_travel_db < backup.sql
```

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set strong database passwords
- [ ] Configure Redis password
- [ ] Enable HTTPS/SSL
- [ ] Set up regular backups
- [ ] Configure monitoring/logging
- [ ] Set up firewall rules
- [ ] Review security settings
- [ ] Test all endpoints
- [ ] Verify Celery tasks work
- [ ] Check email notifications
- [ ] Test payment integration

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Celery Documentation](https://docs.celeryq.dev/)

---

## 🆘 Getting Help

- Check logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- GitHub Issues: [Report a bug](https://github.com/garisonmike/alx_travel_app_0x03/issues)
- ALX Support: Contact your mentor

---

**Happy Containerizing! 🐳**
