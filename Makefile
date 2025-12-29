.PHONY: help install run test lint format clean docker-build docker-run docker-stop docker-logs compose-up compose-down compose-logs

IMAGE_NAME = clar-ia
CONTAINER_NAME = clar-ia-bot

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run the bot locally"
	@echo "  make test          - Run tests (when available)"
	@echo "  make lint          - Run linter (ruff)"
	@echo "  make format        - Format code (ruff)"
	@echo "  make clean         - Clean cache files"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run bot in Docker container"
	@echo "  make docker-stop   - Stop Docker container"
	@echo "  make docker-logs   - Show Docker container logs"
	@echo ""
	@echo "Docker Compose commands:"
	@echo "  make compose-up    - Start bot with docker-compose"
	@echo "  make compose-down  - Stop bot with docker-compose"
	@echo "  make compose-logs  - Show docker-compose logs"

install:
	uv sync

run:
	python main.py

test:
	@echo "No tests configured yet"
	@echo "Install pytest: uv add --dev pytest pytest-asyncio"

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		--restart unless-stopped \
		$(IMAGE_NAME)

docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

docker-logs:
	docker logs -f $(CONTAINER_NAME)

compose-up:
	docker-compose up -d --build

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f
