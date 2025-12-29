.PHONY: help install run test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run the bot"
	@echo "  make test     - Run tests (when available)"
	@echo "  make lint     - Run linter (ruff)"
	@echo "  make format   - Format code (ruff)"
	@echo "  make clean    - Clean cache files"

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
