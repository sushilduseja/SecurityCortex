from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from agents.monitoring_agent import MonitoringAgent
from database.db_utils import get_all_compliance_monitors, get_compliance_monitor, create_compliance_monitor, update_compliance_monitor
from database.models import ComplianceMonitor

# Create router
router = APIRouter()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

# Models for request and response
class ComplianceMonitorCreate(BaseModel):
    name: str
    description: str
    model_or_system: str
    threshold_value: float
    current_value: Optional[float] = None
    status: str = "Active"
    alert_level: Optional[str] = None

class ComplianceMonitorUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_or_system: Optional[str] = None
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    status: Optional[str] = None
    alert_level: Optional[str] = None

class ComplianceMonitorResponse(BaseModel):
    id: int
    name: str
    description: str
    model_or_system: str
    threshold_value: float
    current_value: float
    status: str
    last_checked: str
    alert_level: str

class ComplianceMonitorList(BaseModel):
    items: List[ComplianceMonitorResponse]
    count: int

class ComplianceSummary(BaseModel):
    overall_status: str
    compliance_rate: float
    critical_alerts: int
    warning_alerts: int
    normal_monitors: int
    good_monitors: int
    recommendations: List[str]

# Get all compliance monitors
@router.get("/monitors", response_model=ComplianceMonitorList)
def list_compliance_monitors(
    model: Optional[str] = Query(None, description="Filter by model or system"),
    status: Optional[str] = Query(None, description="Filter by status"),
    alert_level: Optional[str] = Query(None, description="Filter by alert level")
):
    """Get all compliance monitors with optional filtering."""
    try:
        monitors = get_all_compliance_monitors()
        
        # Apply filters if provided
        if model:
            monitors = [m for m in monitors if m.get("model_or_system") == model]
        if status:
            monitors = [m for m in monitors if m.get("status") == status]
        if alert_level:
            monitors = [m for m in monitors if m.get("alert_level") == alert_level]
        
        return {"items": monitors, "count": len(monitors)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve compliance monitors: {str(e)}")

# Get a specific compliance monitor
@router.get("/monitors/{monitor_id}", response_model=ComplianceMonitorResponse)
def get_monitor_by_id(monitor_id: int = Path(..., description="The ID of the compliance monitor to retrieve")):
    """Get a specific compliance monitor by ID."""
    try:
        monitor = get_compliance_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail=f"Compliance monitor with ID {monitor_id} not found")
        return monitor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve compliance monitor: {str(e)}")

# Create a new compliance monitor
@router.post("/monitors", response_model=ComplianceMonitorResponse)
def create_new_monitor(monitor_data: ComplianceMonitorCreate):
    """Create a new compliance monitor."""
    try:
        # Create monitor using agent
        monitor = monitoring_agent.create_monitor(
            name=monitor_data.name,
            description=monitor_data.description,
            model_or_system=monitor_data.model_or_system,
            threshold_value=monitor_data.threshold_value
        )
        
        # Override values if provided
        if monitor_data.current_value is not None:
            monitor.current_value = monitor_data.current_value
        if monitor_data.status:
            monitor.status = monitor_data.status
        if monitor_data.alert_level:
            monitor.alert_level = monitor_data.alert_level
        
        # Save monitor to database
        monitor_id = create_compliance_monitor(monitor)
        
        # Get the saved monitor
        created_monitor = get_compliance_monitor(monitor_id)
        if not created_monitor:
            raise HTTPException(status_code=500, detail="Failed to retrieve created monitor")
        
        return created_monitor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create compliance monitor: {str(e)}")

# Update a compliance monitor
@router.put("/monitors/{monitor_id}", response_model=ComplianceMonitorResponse)
def update_monitor_by_id(
    monitor_data: ComplianceMonitorUpdate,
    monitor_id: int = Path(..., description="The ID of the compliance monitor to update")
):
    """Update an existing compliance monitor."""
    try:
        # Get existing monitor
        existing_monitor = get_compliance_monitor(monitor_id)
        if not existing_monitor:
            raise HTTPException(status_code=404, detail=f"Compliance monitor with ID {monitor_id} not found")
        
        # Update monitor fields if provided
        monitor = ComplianceMonitor(
            id=monitor_id,
            name=monitor_data.name if monitor_data.name is not None else existing_monitor["name"],
            description=monitor_data.description if monitor_data.description is not None else existing_monitor["description"],
            model_or_system=monitor_data.model_or_system if monitor_data.model_or_system is not None else existing_monitor["model_or_system"],
            threshold_value=monitor_data.threshold_value if monitor_data.threshold_value is not None else existing_monitor["threshold_value"],
            current_value=monitor_data.current_value if monitor_data.current_value is not None else existing_monitor["current_value"],
            status=monitor_data.status if monitor_data.status is not None else existing_monitor["status"],
            alert_level=monitor_data.alert_level if monitor_data.alert_level is not None else existing_monitor["alert_level"],
            last_checked=datetime.now()
        )
        
        # Update monitor in database
        success = update_compliance_monitor(monitor)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update compliance monitor")
        
        # Get the updated monitor
        updated_monitor = get_compliance_monitor(monitor_id)
        return updated_monitor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update compliance monitor: {str(e)}")

# Create standard monitors for a model
@router.post("/standard-monitors", response_model=Dict[str, Any])
def create_standard_monitors(
    model_name: str = Body(..., embed=True, description="Name of the model or system"),
    model_type: str = Body("all", embed=True, description="Type of model (e.g., classification, prediction, all)")
):
    """Create a set of standard compliance monitors for a model or system."""
    try:
        # Create standard monitors using agent
        monitor_ids = monitoring_agent.create_standard_monitors(model_name, model_type)
        
        # Get the created monitors
        monitors = []
        for monitor_id in monitor_ids:
            monitor = get_compliance_monitor(monitor_id)
            if monitor:
                monitors.append(monitor)
        
        return {"created_monitors": monitors, "count": len(monitors)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create standard monitors: {str(e)}")

# Update monitor value
@router.put("/monitors/{monitor_id}/value", response_model=ComplianceMonitorResponse)
def update_monitor_value(
    monitor_id: int = Path(..., description="The ID of the compliance monitor to update"),
    value: Optional[float] = Query(None, description="New current value for the monitor")
):
    """Update a compliance monitor's current value and recalculate alert level."""
    try:
        # Update monitor value using agent
        updated_monitor = monitoring_agent.update_monitor_value(monitor_id, value)
        
        # Get the updated monitor from database
        monitor = get_compliance_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail=f"Compliance monitor with ID {monitor_id} not found")
        
        return monitor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update monitor value: {str(e)}")

# Simulate monitoring cycle
@router.post("/simulate-cycle", response_model=Dict[str, Any])
def simulate_monitoring_cycle():
    """Simulate a monitoring cycle by updating all monitors."""
    try:
        # Get all monitors
        monitors = get_all_compliance_monitors()
        
        # Simulate monitoring cycle
        updated_monitors = monitoring_agent.simulate_monitoring_cycle(monitors)
        
        return {"updated_monitors": updated_monitors, "count": len(updated_monitors)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to simulate monitoring cycle: {str(e)}")

# Get compliance summary
@router.get("/summary", response_model=ComplianceSummary)
def get_compliance_summary():
    """Get a summary of compliance status."""
    try:
        # Get all monitors
        monitors = get_all_compliance_monitors()
        
        # Generate summary
        summary = monitoring_agent.get_compliance_summary(monitors)
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate compliance summary: {str(e)}")
