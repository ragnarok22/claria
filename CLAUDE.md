# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clar IA is a Spanish-language Telegram bot that responds with a comedic, exaggerated persona of a "revolutionary Cuban bot." The bot uses OpenAI's GPT-4o-mini model to generate contextual responses in Cuban slang with satirical pro-revolutionary rhetoric for entertainment in group chat settings.

**Key behavior:**
- Only responds in Telegram groups/supergroups (not private chats)
- Only responds when mentioned by username or name
- Uses async/await pattern throughout

## Common Commands

### Development
```bash
make install    # Install dependencies with uv
make run        # Run bot locally (requires .env file)
make lint       # Check code with ruff
make format     # Format code with ruff
make clean      # Remove cache files
```

### Docker
```bash
make docker-build  # Build Docker image
make docker-run    # Run container with .env
make docker-stop   # Stop and remove container
make docker-logs   # Stream container logs
```

### Docker Compose (Recommended for Production)
```bash
make compose-up    # Start service with rebuild
make compose-down  # Stop service
make compose-logs  # Stream service logs
```

## Environment Setup

The bot requires a `.env` file in the project root with:
```env
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_api_key_here
```

Both variables are **required** and validated by `Config` class at startup.

## Architecture

### Core Components

**bot.py** - Main Telegram bot logic
- `ClarIABot` class manages bot lifecycle
- `initialize_bot_info()` fetches bot username/name from Telegram on startup
- `is_mentioned()` checks if message contains bot's username or name
- `handle_message()` validates group chat + mention, then gets AI response
- Uses `application.run_polling()` for long-polling updates
- All handlers are async functions

**ai.py** - OpenAI integration
- `AIAssistant` wraps OpenAI client
- Contains 40-line `system_prompt` defining bot's Cuban revolutionary persona
- `get_response()` sends messages to GPT-4o-mini with:
  - Model: `gpt-4o-mini`
  - Max tokens: 500
  - Temperature: 0.8 (for creative responses)
  - Optional conversation context support (not currently used)

**config.py** - Configuration management
- Loads `.env` file with `python-dotenv`
- `Config` class validates required environment variables
- `get_env()` utility handles optional defaults and required validation

**main.py** - Entry point
- Instantiates `Config` and `ClarIABot`
- Calls `bot.run()` to start polling

### Message Flow
1. Telegram sends update via polling
2. `MessageHandler` (filters.TEXT) triggers `handle_message()`
3. Validate: is group chat? is bot mentioned?
4. Send typing action
5. Call `AIAssistant.get_response()` with message text
6. Reply to message with AI response
7. Error handling with Spanish error messages

## Package Management

This project uses **uv** as the package manager (modern, fast alternative to pip):
- Dependencies defined in `pyproject.toml`
- Locked versions in `uv.lock`
- Install: `uv sync`
- Add dependency: `uv add package-name`
- Add dev dependency: `uv add --dev package-name`

**Python version:** 3.13+ (specified in `pyproject.toml` and `.python-version`)

## Testing

No testing infrastructure currently configured. The Makefile includes a placeholder `make test` target that suggests installing `pytest` and `pytest-asyncio` for async test support.

## Deployment Notes

**Dockerfile:**
- Uses `python:3.14-slim` base image
- Installs dependencies with `uv sync --frozen --no-dev` (production only)
- Runs bot with `uv run main.py`

**compose.yaml:**
- Single service: `clar-ia-bot`
- Auto-builds from Dockerfile
- Loads `.env` file for environment variables
- Restart policy: `unless-stopped`

## Code Style

- Uses `ruff` for linting and formatting
- All async functions use proper `async`/`await` patterns
- Logging configured with timestamps and log levels
- Spanish messages for user-facing text (error messages, replies)
