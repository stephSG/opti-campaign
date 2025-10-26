# Makefile for Opti-Campaign Project Management

.PHONY: build up down logs test-backend test-frontend

# Build or rebuild services
build:
	docker-compose build

# Start services in detached mode
up:
	docker-compose up -d

# Stop and remove services
down:
	docker-compose down

# Follow logs for specified services
logs:
	docker-compose logs -f backend frontend

# Run backend tests
test-backend:
	docker-compose exec backend pytest

# Run frontend tests
test-frontend:
	docker-compose exec frontend npm run test

