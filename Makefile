# Makefile for the Opti-Campaign project

# Define phony targets to avoid conflicts with file names
.PHONY: build run stop logs test-backend test-frontend ci

# Build the Docker containers
build:
	docker-compose build

# Run the Docker containers in detached mode
run:
	docker-compose up -d

# Stop and remove the Docker containers
stop:
	docker-compose down

# Follow the logs of the Docker containers
logs:
	docker-compose logs -f

# Run backend tests
test-backend:
	cd backend && pytest

# Run frontend tests
test-frontend:
	cd frontend && npm run test

# Run all tests (continuous integration)
ci: test-backend test-frontend

