#
# Makefile for the Opti-Campaign project
#

.PHONY: help run-backend test-backend init-db

# Ensures that "make" without arguments shows the help
default: help

help:
	@echo "Available commands:"
	@echo ""
	@echo "  make run-backend    - Run the FastAPI backend server (dev mode)"
	@echo "  make test-backend   - Run the backend unit tests (requires pytest)"
	@echo "  make init-db        - Initialize the database with tables and seed data"
	@echo ""

run-backend:
	@echo "Starting backend server on http://127.0.0.1:8000"
	@echo "Access docs at http://127.0.0.1:8000/docs"
	@uvicorn app.main:app --reload

test-backend:
	@echo "Running backend tests..."
	@pytest

init-db:
	@echo "Installing dependencies to ensure compatibility..."
	@pip install --quiet -r requirements.txt
	@echo "Initializing database..."
	@python init_db.py
	@echo "Database initialized."
