from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class Page(BaseModel):
    id: str
    status_indicator: str
    status_description: str


class Component(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    position: Optional[int] = None
    description: Optional[str] = None
    showcase: Optional[bool] = None
    start_date: Optional[datetime] = None
    group_id: Optional[str] = None
    page_id: str
    group: Optional[bool] = None
    only_show_if_degraded: Optional[bool] = None


class IncidentUpdate(BaseModel):
    id: str
    status: str
    body: str
    incident_id: str
    created_at: datetime
    updated_at: datetime
    display_at: datetime
    affected_components: Optional[List[Component]] = None
    deliver_notifications: Optional[bool] = None
    custom_tweet: Optional[str] = None
    tweet_id: Optional[str] = None


class Incident(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    monitoring_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    impact: str
    shortlink: str
    started_at: Optional[datetime] = None
    page_id: str
    incident_updates: Optional[List[IncidentUpdate]] = None
    components: Optional[List[Component]] = None
    body: Optional[str] = None
    postmortem_ignored: Optional[bool] = None
    postmortem_body: Optional[str] = None
    postmortem_body_last_updated_at: Optional[datetime] = None
    postmortem_published_at: Optional[datetime] = None
    postmortem_notified_subscribers: Optional[bool] = None
    postmortem_notified_twitter: Optional[bool] = None
    backfilled: Optional[bool] = None
    scheduled_for: Optional[datetime] = None
    scheduled_until: Optional[datetime] = None
    scheduled_remind_prior: Optional[bool] = None
    scheduled_reminded_at: Optional[datetime] = None
    impact_override: Optional[str] = None
    scheduled_auto_in_progress: Optional[bool] = None
    scheduled_auto_completed: Optional[bool] = None


class MaintenanceUpdate(BaseModel):
    id: str
    status: str
    body: str
    created_at: datetime
    updated_at: datetime
    display_at: datetime
    affected_components: Optional[List[Component]] = None
    deliver_notifications: Optional[bool] = None
    custom_tweet: Optional[str] = None
    tweet_id: Optional[str] = None


class Maintenance(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    monitoring_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    shortlink: str
    started_at: Optional[datetime] = None
    page_id: str
    incident_updates: Optional[List[MaintenanceUpdate]] = None
    components: Optional[List[Component]] = None
    scheduled_for: datetime
    scheduled_until: datetime
    body: Optional[str] = None


class ComponentUpdate(BaseModel):
    id: str
    status: str
    body: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class Meta(BaseModel):
    unsubscribe: Optional[str] = None
    documentation: Optional[str] = None


class StatusPageWebhook(BaseModel):
    meta: Optional[Meta] = None
    page: Page
    incident: Optional[Incident] = None
    maintenance: Optional[Maintenance] = None
    component: Optional[Component] = None
    component_update: Optional[ComponentUpdate] = None