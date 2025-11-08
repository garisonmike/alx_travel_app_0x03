# 🐳 Docker Quick Start Guide

Get the ALX Travel App running in **under 5 minutes** with Docker!

## Prerequisites

- Docker & Docker Compose installed
- 4GB RAM available
- Internet connection

## 🚀 Quick Commands

### 1️⃣ Start Everything

```bash
# Using Make (recommended)
make dev

# Or using docker-compose directly
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 2️⃣ Access Your App

- **Web App:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Swagger API:** http://localhost:8000/swagger/
- **RabbitMQ Dashboard:** http://localhost:15672 (guest/guest)

### 3️⃣ Stop Everything

```bash
make down
# Or: docker-compose down
```

## 📦 What Gets Installed?

- ✅ Django web application
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ RabbitMQ message broker
- ✅ Celery worker (background tasks)
- ✅ Celery beat (scheduled tasks)

## 🔧 Common Commands

```bash
# View logs
make logs
# Or: docker-compose logs -f

# Run tests
make test
# Or: docker-compose exec web pytest

# Django shell
make shell
# Or: docker-compose exec web python manage.py shell

# Database shell
make dbshell
# Or: docker-compose exec db psql -U alx_user -d alx_travel_db

# Restart services
make restart
# Or: docker-compose restart

# Clean everything
make clean
# Or: docker-compose down -v --rmi all
```

## 🏭 Production Deployment

```bash
# 1. Create .env from template
cp .env.production .env
# Edit .env with your production values

# 2. Start production stack
make prod
# Or: docker-compose -f docker-compose.prod.yml up -d

# 3. Initialize
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## 🐛 Troubleshooting

### Port Already in Use?

```bash
# Change port in docker-compose.yml
ports:
  - "8080:8000"  # Use 8080 instead
```

### Database Connection Error?

```bash
# Wait for services to start (30 seconds)
docker-compose ps  # Check all services are "Up"
```

### Permission Errors?

```bash
sudo chown -R $USER:$USER .
```

### Start Fresh?

```bash
make clean  # Remove everything
make dev    # Start again
```

## 📚 Full Documentation

See [docs/DOCKER_DEPLOYMENT.md](docs/DOCKER_DEPLOYMENT.md) for:
- Detailed architecture
- Configuration options
- Production setup
- Monitoring
- Security best practices

## 🆘 Need Help?

- Check logs: `make logs`
- View status: `make ps`
- Test health: `make health`
- GitHub Issues: [Report a bug](https://github.com/garisonmike/alx_travel_app_0x03/issues)

---

**That's it! 🎉 Your app is containerized and running!**
