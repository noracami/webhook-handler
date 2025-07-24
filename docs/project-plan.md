# Statuspage to Discord Webhook Service

## Project Structure
```
webhook-handler/
├── src/
│   ├── main.py          # FastAPI app with Statuspage webhook endpoint
│   ├── config.py        # Environment configuration
│   ├── discord.py       # Discord message sending
│   └── models.py        # Statuspage webhook payload models
├── docs/
│   ├── setup.md         # uv project setup instructions
│   └── statuspage.md    # Statuspage webhook documentation
├── pyproject.toml       # uv dependencies
├── .env.example         # Environment template
├── .gitignore
├── README.md
└── CLAUDE.md
```

## Core Components

### 1. FastAPI App (main.py)
- Endpoint: `POST /webhook/statuspage`
- Statuspage payload validation using Pydantic models
- Event filtering (incident updates, maintenance, etc.)
- Health check endpoint

### 2. Statuspage Models (models.py)
- Pydantic models for Statuspage webhook payloads
- Support for incident, component, and maintenance events
- Proper typing for all webhook fields

### 3. Discord Integration (discord.py)
- Format Statuspage events into Discord embeds
- Different formatting for incidents vs maintenance
- Status-based color coding (red for incidents, yellow for maintenance)

### 4. Configuration (config.py)
- Environment variable management
- Statuspage webhook verification (if needed)

## Environment Variables
- `DISCORD_WEBHOOK_URL`: Discord webhook URL
- `STATUSPAGE_WEBHOOK_SECRET`: Optional Statuspage webhook secret
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level

## Discord Message Features
- Rich embeds with incident details
- Status-based color coding
- Component status updates
- Maintenance notifications
- Clickable links to status page