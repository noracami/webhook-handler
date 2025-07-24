import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .models import StatusPageWebhook, Incident, Maintenance, Component
from .config import settings

logger = logging.getLogger(__name__)


class DiscordWebhook:
    def __init__(self):
        self.webhook_url = settings.discord_webhook_url

    def get_status_color(self, status: str, impact: Optional[str] = None) -> int:
        """Get Discord embed color based on status and impact"""
        if status in ["resolved", "completed", "operational"]:
            return 0x00FF00  # Green
        elif status in ["investigating", "identified", "monitoring"]:
            return 0xFFFF00  # Yellow
        elif status in ["major_outage", "partial_outage"] or impact == "major":
            return 0xFF0000  # Red
        elif status in ["performance_issues", "degraded_performance"] or impact == "minor":
            return 0xFF8C00  # Orange
        elif status in ["scheduled", "in_progress"]:
            return 0x0099FF  # Blue
        else:
            return 0x808080  # Gray

    def format_incident_embed(self, incident: Incident, page_url: str) -> Dict[str, Any]:
        """Format incident data into Discord embed"""
        embed = {
            "title": f"🚨 {incident.name}",
            "description": incident.body or "No description provided",
            "color": self.get_status_color(incident.status, incident.impact),
            "url": incident.shortlink,
            "timestamp": incident.updated_at.isoformat(),
            "fields": [
                {
                    "name": "Status",
                    "value": incident.status.replace("_", " ").title(),
                    "inline": True
                },
                {
                    "name": "Impact",
                    "value": incident.impact.replace("_", " ").title(),
                    "inline": True
                },
                {
                    "name": "Started",
                    "value": incident.started_at.strftime("%Y-%m-%d %H:%M UTC") if incident.started_at else "Unknown",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Statuspage Notification",
                "icon_url": "https://dka575ofm4ao0.cloudfront.net/assets/base/logo-6d88bcb6c99a.png"
            }
        }

        if incident.components:
            component_names = [comp.name for comp in incident.components]
            embed["fields"].append({
                "name": "Affected Components",
                "value": ", ".join(component_names),
                "inline": False
            })

        if incident.resolved_at:
            embed["fields"].append({
                "name": "Resolved",
                "value": incident.resolved_at.strftime("%Y-%m-%d %H:%M UTC"),
                "inline": True
            })

        return embed

    def format_maintenance_embed(self, maintenance: Maintenance) -> Dict[str, Any]:
        """Format maintenance data into Discord embed"""
        embed = {
            "title": f"🔧 {maintenance.name}",
            "description": maintenance.body or "Scheduled maintenance",
            "color": self.get_status_color(maintenance.status),
            "url": maintenance.shortlink,
            "timestamp": maintenance.updated_at.isoformat(),
            "fields": [
                {
                    "name": "Status",
                    "value": maintenance.status.replace("_", " ").title(),
                    "inline": True
                },
                {
                    "name": "Scheduled Start",
                    "value": maintenance.scheduled_for.strftime("%Y-%m-%d %H:%M UTC"),
                    "inline": True
                },
                {
                    "name": "Scheduled End",
                    "value": maintenance.scheduled_until.strftime("%Y-%m-%d %H:%M UTC"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Statuspage Notification",
                "icon_url": "https://dka575ofm4ao0.cloudfront.net/assets/base/logo-6d88bcb6c99a.png"
            }
        }

        if maintenance.components:
            component_names = [comp.name for comp in maintenance.components]
            embed["fields"].append({
                "name": "Affected Components",
                "value": ", ".join(component_names),
                "inline": False
            })

        return embed

    def format_component_embed(self, component: Component) -> Dict[str, Any]:
        """Format component status change into Discord embed"""
        embed = {
            "title": f"📊 Component Status Update",
            "description": f"**{component.name}** status changed to **{component.status.replace('_', ' ').title()}**",
            "color": self.get_status_color(component.status),
            "timestamp": component.updated_at.isoformat(),
            "fields": [
                {
                    "name": "Component",
                    "value": component.name,
                    "inline": True
                },
                {
                    "name": "Status",
                    "value": component.status.replace("_", " ").title(),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Statuspage Notification",
                "icon_url": "https://dka575ofm4ao0.cloudfront.net/assets/base/logo-6d88bcb6c99a.png"
            }
        }

        if component.description:
            embed["fields"].append({
                "name": "Description",
                "value": component.description,
                "inline": False
            })

        return embed

    async def send_webhook(self, webhook_data: StatusPageWebhook) -> bool:
        """Send webhook data to Discord"""
        try:
            embed = None
            
            if webhook_data.incident:
                embed = self.format_incident_embed(
                    webhook_data.incident, 
                    f"https://{webhook_data.page.id}.statuspage.io"
                )
            elif webhook_data.maintenance:
                embed = self.format_maintenance_embed(webhook_data.maintenance)
            elif webhook_data.component:
                embed = self.format_component_embed(webhook_data.component)
            
            if not embed:
                logger.warning("No supported webhook type found")
                return False

            payload = {
                "embeds": [embed],
                "username": "Statuspage",
                "avatar_url": "https://dka575ofm4ao0.cloudfront.net/assets/base/logo-6d88bcb6c99a.png"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
            logger.info(f"Successfully sent Discord message for {type(webhook_data).__name__}")
            return True
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error sending Discord webhook: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Discord webhook: {e}")
            return False


discord_webhook = DiscordWebhook()