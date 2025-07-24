#!/usr/bin/env python3
"""
Statuspage to Discord Webhook Handler
Main entrypoint for CI/CD deployment
"""

import uvicorn
from src.config import settings


def main():
    """Main entrypoint for the webhook handler application"""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()
