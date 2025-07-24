# uv Project Setup Instructions

## Prerequisites
- Python 3.8+ installed
- uv package manager installed (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Project Setup Steps

### 1. Initialize the Project
```bash
cd /Users/kelonghe/Project/webhook-handler
uv init --name webhook-handler .
```

### 2. Add Dependencies
```bash
uv add fastapi uvicorn httpx pydantic python-dotenv
```

### 3. Add Development Dependencies
```bash
uv add --dev pytest ruff black
```

### 4. Create Project Structure
```bash
mkdir -p src tests
touch src/__init__.py
touch src/main.py
touch src/config.py
touch src/discord.py
touch src/models.py
touch tests/__init__.py
```

### 5. Create Environment File
```bash
cp .env.example .env
# Edit .env with your Discord webhook URL
```

### 6. Development Commands

#### Run Development Server
```bash
uv run fastapi dev src/main.py
```

#### Run Tests
```bash
uv run pytest
```

#### Code Formatting
```bash
uv run black src/
uv run ruff check src/
```

#### Production Run
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables Setup

Create `.env` file with:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook/url
STATUSPAGE_WEBHOOK_SECRET=your_optional_secret
PORT=8000
LOG_LEVEL=INFO
```

## Next Steps
1. Implement the FastAPI application in `src/main.py`
2. Define Statuspage webhook models in `src/models.py`
3. Create Discord integration in `src/discord.py`
4. Set up configuration management in `src/config.py`
5. Test the webhook endpoint with Statuspage