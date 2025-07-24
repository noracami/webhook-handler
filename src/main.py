import logging
import hashlib
import hmac
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from .models import StatusPageWebhook
from .discord import discord_webhook
from .config import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Statuspage to Discord Webhook",
    description="Forwards Statuspage webhook notifications to Discord",
    version="1.0.0"
)


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify Statuspage webhook signature"""
    if not secret:
        return True
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


async def process_webhook(webhook_data: StatusPageWebhook):
    """Process webhook data and send to Discord"""
    try:
        success = await discord_webhook.send_webhook(webhook_data)
        if success:
            logger.info("Webhook processed successfully")
        else:
            logger.error("Failed to send webhook to Discord")
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "statuspage-webhook-handler"}


@app.post("/webhook/statuspage")
async def statuspage_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Receive Statuspage webhook notifications"""
    try:
        body = await request.body()
        
        # Verify webhook signature if secret is configured
        if settings.statuspage_webhook_secret:
            signature = request.headers.get("X-Webhook-Signature", "")
            if not verify_webhook_signature(body, signature, settings.statuspage_webhook_secret):
                logger.warning("Invalid webhook signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse webhook data
        webhook_data = StatusPageWebhook.parse_raw(body)
        
        # Log received webhook
        webhook_type = "unknown"
        if webhook_data.incident:
            webhook_type = f"incident ({webhook_data.incident.status})"
        elif webhook_data.maintenance:
            webhook_type = f"maintenance ({webhook_data.maintenance.status})"
        elif webhook_data.component:
            webhook_type = f"component ({webhook_data.component.status})"
        
        logger.info(f"Received {webhook_type} webhook for page {webhook_data.page.id}")
        
        # Process webhook in background
        background_tasks.add_task(process_webhook, webhook_data)
        
        return JSONResponse(
            status_code=200,
            content={"message": "Webhook received", "type": webhook_type}
        )
        
    except ValueError as e:
        logger.error(f"Invalid webhook payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Statuspage to Discord Webhook Handler",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "/webhook/statuspage",
            "health": "/health"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )