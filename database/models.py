from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class Policy:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    category: str = ""
    status: str = "Draft"
    created_at: datetime = None
    updated_at: datetime = None
    content: str = ""

@dataclass
class RiskAssessment:
    id: Optional[int] = None
    title: str = ""
    model_name: str = ""
    risk_score: float = 0.0
    findings: str = ""
    recommendations: str = ""
    created_at: datetime = None
    status: str = "Pending"

@dataclass
class ComplianceMonitor:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    model_or_system: str = ""
    threshold_value: float = 0.0
    current_value: float = 0.0
    status: str = "Active"
    last_checked: datetime = None
    alert_level: str = "Normal"

@dataclass
class Report:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    report_type: str = ""
    created_at: datetime = None
    content: str = ""
    insights: str = ""
    status: str = "Draft"

@dataclass
class Activity:
    id: Optional[int] = None
    activity_type: str = ""
    description: str = ""
    created_at: datetime = None
    actor: str = ""
    related_entity_id: Optional[int] = None
    related_entity_type: Optional[str] = None
