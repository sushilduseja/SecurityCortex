from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Response Models
class BaseResponse(BaseModel):
    id: int
    created_at: datetime

# Policy Models
class PolicyRequest(BaseModel):
    title: str
    description: str
    category: str
    status: str = "Draft"
    content: str

class PolicyResponse(BaseResponse):
    title: str
    description: str
    category: str
    status: str
    content: str
    updated_at: Optional[datetime] = None

# Risk Assessment Models
class RiskAssessmentRequest(BaseModel):
    title: str
    model_name: str
    risk_score: float
    findings: str
    recommendations: str
    status: str = "Pending"

class RiskAssessmentResponse(BaseResponse):
    title: str
    model_name: str
    risk_score: float
    findings: str
    recommendations: str
    status: str

# Compliance Monitor Models
class ComplianceMonitorRequest(BaseModel):
    name: str
    description: str
    model_or_system: str
    threshold_value: float
    current_value: float = 0.0
    status: str = "Active"
    alert_level: str = "Normal"

# Special compliance monitor response that doesn't require created_at
class ComplianceMonitorResponse(BaseModel):
    id: int
    name: str
    description: str
    model_or_system: str
    threshold_value: float
    current_value: float
    status: str
    last_checked: datetime
    alert_level: str
    created_at: Optional[datetime] = None

# Report Models
class ReportRequest(BaseModel):
    title: str
    description: str
    report_type: str
    content: str
    insights: str = ""
    status: str = "Draft"

class ReportResponse(BaseResponse):
    title: str
    description: str
    report_type: str
    content: str
    insights: str
    status: str

# Activity Model
class ActivityResponse(BaseResponse):
    activity_type: str
    description: str
    actor: str
    related_entity_id: Optional[int] = None
    related_entity_type: Optional[str] = None

# Dashboard Models
class DeltaResponse(BaseModel):
    policy_count: int
    avg_risk_score: float
    compliance_rate: float
    active_monitors: int

class DashboardMetricsResponse(BaseModel):
    policy_count: int
    avg_risk_score: float
    compliance_rate: float
    active_monitors: int
    deltas: DeltaResponse

# Chart Data Models
class DatasetResponse(BaseModel):
    label: Optional[str] = None
    data: List[float]
    backgroundColor: str
    borderColor: Optional[str] = None
    pointBackgroundColor: Optional[str] = None
    pointBorderColor: Optional[str] = None
    pointHoverBackgroundColor: Optional[str] = None
    pointHoverBorderColor: Optional[str] = None

class ChartDataResponse(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]