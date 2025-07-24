# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python FastAPI service that receives webhook notifications from Atlassian Statuspage and forwards them to Discord as formatted messages. The service handles incidents, maintenance events, and component status changes.

## Architecture
- **FastAPI Application** (`src/main.py`) - Main webhook endpoint and request handling
- **Pydantic Models** (`src/models.py`) - Data models for Statuspage webhook payloads
- **Discord Integration** (`src/discord.py`) - Message formatting and Discord webhook sending
- **Configuration** (`src/config.py`) - Environment variable management with validation

## Development Commands

### Setup and Installation
```bash
uv add <package>  # Add new dependency
```

### Running the Application
```bash
uv run fastapi dev src/main.py      # Development server with auto-reload
uv run uvicorn src.main:app --reload # Alternative dev command
uv run python src/main.py           # Production server
```

### Code Quality
```bash
uv run ruff check src/              # Linting (if ruff is added)
uv run black src/                   # Code formatting (if black is added)
```

### Configuration
- Copy `.env.example` to `.env` and configure:
  - `DISCORD_WEBHOOK_URL` - Required Discord webhook URL
  - `STATUSPAGE_WEBHOOK_SECRET` - Optional webhook signature verification
  - `PORT` - Server port (default: 8000)
  - `LOG_LEVEL` - Logging level (default: INFO)

## Key Endpoints
- `POST /webhook/statuspage` - Main webhook receiver
- `GET /health` - Health check
- `GET /` - Service information
- `GET /docs` - FastAPI auto-generated documentation

## Webhook Processing Flow
1. Receive Statuspage webhook at `/webhook/statuspage`
2. Verify signature if `STATUSPAGE_WEBHOOK_SECRET` is configured
3. Parse webhook payload using Pydantic models
4. Format message based on event type (incident/maintenance/component)
5. Send to Discord as background task
6. Return success response immediately

## Discord Message Types
- **Incidents**: Red/Orange/Yellow/Green embeds based on status and impact
- **Maintenance**: Blue embeds with scheduled times
- **Components**: Status-based colored embeds

## Error Handling
- Invalid payloads return 400 Bad Request
- Invalid signatures return 401 Unauthorized
- Discord send failures are logged but don't fail the webhook response
- All webhook processing happens in background tasks