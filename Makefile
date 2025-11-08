.PHONY: help build up down restart logs shell test migrate superuser clean ps

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Commands
build: ## Build all Docker images
	docker-compose build

up: ## Start all services in foreground
	docker-compose up

up-d: ## Start all services in background
	docker-compose up -d

down: ## Stop and remove all containers
	docker-compose down

down-v: ## Stop and remove all containers and volumes
	docker-compose down -v

restart: ## Restart all services
	docker-compose restart

logs: ## View logs from all services
	docker-compose logs -f

logs-web: ## View logs from web service
	docker-compose logs -f web

logs-worker: ## View logs from Celery worker
	docker-compose logs -f worker

shell: ## Access Django shell
	docker-compose exec web python manage.py shell

bash: ## Access bash in web container
	docker-compose exec web bash

dbshell: ## Access PostgreSQL shell
	docker-compose exec db psql -U alx_user -d alx_travel_db

test: ## Run all tests
	docker-compose exec web pytest -v

test-coverage: ## Run tests with coverage
	docker-compose exec web pytest --cov=alx_travel_app --cov-report=html

migrate: ## Run database migrations
	docker-compose exec web python manage.py migrate

makemigrations: ## Create new migrations
	docker-compose exec web python manage.py makemigrations

superuser: ## Create Django superuser
	docker-compose exec web python manage.py createsuperuser

collectstatic: ## Collect static files
	docker-compose exec web python manage.py collectstatic --noinput

ps: ## Show running containers
	docker-compose ps

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all

# Production Commands
prod-build: ## Build production images
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production services
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## View production logs
	docker-compose -f docker-compose.prod.yml logs -f

prod-restart: ## Restart production services
	docker-compose -f docker-compose.prod.yml restart

prod-ps: ## Show production containers
	docker-compose -f docker-compose.prod.yml ps

# Database Commands
backup-db: ## Backup database
	docker-compose exec db pg_dump -U alx_user alx_travel_db > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backup_$$(date +%Y%m%d_%H%M%S).sql"

restore-db: ## Restore database from backup (usage: make restore-db FILE=backup.sql)
	docker-compose exec -T db psql -U alx_user alx_travel_db < $(FILE)

# Utility Commands
prune: ## Remove unused Docker resources
	docker system prune -af

stats: ## Show Docker container stats
	docker stats

health: ## Check health of all services
	@echo "Checking service health..."
	@docker-compose ps
	@echo "\nTesting web service..."
	@curl -f http://localhost:8000/admin/login/ && echo "✓ Web service is healthy" || echo "✗ Web service is down"
	@echo "\nTesting RabbitMQ..."
	@curl -f http://localhost:15672/ && echo "✓ RabbitMQ is healthy" || echo "✗ RabbitMQ is down"

# Development Quick Start
dev: build up-d migrate superuser ## Quick start for development (build, up, migrate, create superuser)
	@echo "\n✓ Development environment is ready!"
	@echo "  Web: http://localhost:8000"
	@echo "  Admin: http://localhost:8000/admin"
	@echo "  Swagger: http://localhost:8000/swagger/"
	@echo "  RabbitMQ: http://localhost:15672 (guest/guest)"

# Production Quick Start
prod: prod-build prod-up ## Quick start for production
	@echo "\n✓ Production environment is starting..."
	@echo "  Check status: make prod-ps"
	@echo "  View logs: make prod-logs"
