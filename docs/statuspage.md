# Statuspage Webhook Integration

## Overview
This service receives webhook notifications from Atlassian Statuspage and forwards them to Discord as formatted messages.

## Statuspage Webhook Configuration
1. Go to your Statuspage dashboard
2. Navigate to Settings → Webhook notifications
3. Add a new webhook with URL: `https://your-domain.com/webhook/statuspage`
4. Select the events you want to receive (incidents, maintenance, components)

## Supported Webhook Events

### Incident Events
- `incident.created` - New incident reported
- `incident.updated` - Incident status or details updated
- `incident.resolved` - Incident marked as resolved

### Component Events
- `component.status_changed` - Service component status changed

### Maintenance Events
- `maintenance.scheduled` - Planned maintenance scheduled
- `maintenance.started` - Maintenance window started
- `maintenance.completed` - Maintenance completed

## Webhook Payload Structure

### Incident Payload Example
```json
{
  "meta": {
    "unsubscribe": "https://...",
    "documentation": "https://..."
  },
  "page": {
    "id": "kctbh9vrtdwd",
    "status_indicator": "none",
    "status_description": "All Systems Operational"
  },
  "incident": {
    "id": "rclfxz2g21ly",
    "name": "Server Issues",
    "status": "investigating",
    "created_at": "2014-05-14T14:22:34.441-06:00",
    "updated_at": "2014-05-14T14:22:34.441-06:00",
    "monitoring_at": null,
    "resolved_at": null,
    "impact": "minor",
    "shortlink": "http://stspg.io/pkvpcwjwqd5b",
    "postmortem_ignored": false,
    "postmortem_body": null,
    "postmortem_body_last_updated_at": null,
    "postmortem_published_at": null,
    "postmortem_notified_subscribers": false,
    "postmortem_notified_twitter": false,
    "backfilled": false,
    "scheduled_for": null,
    "scheduled_until": null,
    "scheduled_remind_prior": false,
    "scheduled_reminded_at": null,
    "impact_override": null,
    "scheduled_auto_in_progress": false,
    "scheduled_auto_completed": false,
    "started_at": "2014-05-14T14:22:34.441-06:00",
    "body": "We are investigating server issues.",
    "components": [],
    "updates": []
  }
}
```

## Discord Message Format

### Incident Messages
- **Title**: Incident name
- **Color**: 
  - 🔴 Red (0xFF0000) for major/critical incidents
  - 🟠 Orange (0xFF8C00) for minor incidents
  - 🟡 Yellow (0xFFFF00) for investigating
  - 🟢 Green (0x00FF00) for resolved
- **Fields**:
  - Status
  - Impact level
  - Created/Updated time
  - Affected components (if any)
- **Footer**: Link to status page

### Component Messages
- **Title**: Component name status change
- **Color**: Based on component status
- **Description**: Status change details

### Maintenance Messages
- **Title**: Maintenance event
- **Color**: 🔵 Blue (0x0099FF)
- **Fields**:
  - Scheduled time
  - Affected components
  - Duration

## Security
- Optional webhook secret verification using `STATUSPAGE_WEBHOOK_SECRET`
- Validates webhook signature if secret is provided
- Logs all webhook attempts for monitoring