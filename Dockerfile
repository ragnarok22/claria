# Dockerfile for Clar IA Telegram Bot
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (production only, no dev dependencies)
RUN uv sync --frozen --no-dev

# Copy application code
COPY config.py ai.py bot.py main.py ./

# Run the bot
CMD ["uv", "run", "main.py"]
