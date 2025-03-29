from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import uvicorn

from database.db_init_sqlite import init_db
from database.db_utils_sqlite import (
    get_all_policies, get_policy, create_policy, update_policy,
    get_all_risk_assessments, get_risk_assessment, create_risk_assessment,
    get_all_compliance_monitors, get_compliance_monitor,
    create_compliance_monitor, update_compliance_monitor, get_all_reports,
    get_report, create_report, get_recent_activities, log_activity
)
from database.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity

# Pydantic models for request/response validation
from app.api.models import (
    PolicyResponse, PolicyRequest, 
    RiskAssessmentResponse, RiskAssessmentRequest,
    ComplianceMonitorResponse, ComplianceMonitorRequest,
    ReportResponse, ReportRequest,
    DashboardMetricsResponse, ChartDataResponse, ActivityResponse
)

# Create the FastAPI application
app = FastAPI(
    title="AI Governance Dashboard",
    description="API for AI Governance Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify the domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()

# Do not mount static files at root since we need to handle API routes
# We'll mount specific folders and use catch-all for SPA routing

# API Routes

# API routes will be handled by specific endpoints
# All frontend routes should be handled by serving index.html

# Mount static files with index.html as the default
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/css", StaticFiles(directory="static/css"), name="css")

# Dashboard metrics
@app.get("/api/dashboard/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics():
    """Get summary metrics for the dashboard"""
    try:
        # Get all data for calculating metrics
        policies = get_all_policies()
        risk_assessments = get_all_risk_assessments()
        compliance_monitors = get_all_compliance_monitors()
        
        # Calculate metrics
        policy_count = len(policies)
        
        # Average risk score calculation
        risk_scores = [ra['risk_score'] for ra in risk_assessments if ra['risk_score'] is not None]
        avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        # Compliance rate calculation
        compliant_monitors = [m for m in compliance_monitors 
                             if m['alert_level'] == 'Normal' and m['status'] == 'Active']
        active_monitors = [m for m in compliance_monitors if m['status'] == 'Active']
        compliance_rate = len(compliant_monitors) / len(active_monitors) if active_monitors else 1
        
        # Calculate changes over time (dummy values for now)
        delta_policy = 2  # Increase of 2 policies
        delta_risk = -0.05  # Decrease in risk score (good)
        delta_compliance = 0.03  # Increase in compliance rate (good)
        delta_monitors = 1  # Added 1 new monitor
        
        return {
            "policy_count": policy_count,
            "avg_risk_score": round(avg_risk_score, 2),
            "compliance_rate": round(compliance_rate, 2),
            "active_monitors": len(active_monitors),
            "deltas": {
                "policy_count": delta_policy,
                "avg_risk_score": delta_risk,
                "compliance_rate": delta_compliance,
                "active_monitors": delta_monitors
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Compliance Status Chart data
@app.get("/api/dashboard/compliance-status-chart", response_model=ChartDataResponse)
async def get_compliance_status_chart():
    """Get data for the compliance status chart"""
    try:
        monitors = get_all_compliance_monitors()
        
        # Group monitors by alert level
        alert_levels = {}
        for monitor in monitors:
            level = monitor['alert_level']
            if level not in alert_levels:
                alert_levels[level] = 0
            alert_levels[level] += 1
        
        # Prepare data for chart
        labels = list(alert_levels.keys())
        data = list(alert_levels.values())
        
        # Colors for each status
        colors = {
            'Normal': '#4caf50',
            'Warning': '#ff9800',
            'Critical': '#f44336'
        }
        
        background_colors = [colors.get(label, '#999') for label in labels]
        
        return {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": background_colors
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alias for backward compatibility with legacy frontend code
@app.get("/api/charts/compliance-status", response_model=ChartDataResponse)
async def get_compliance_status_chart_legacy():
    """Legacy endpoint for compliance status chart"""
    return await get_compliance_status_chart()

# Risk Distribution Chart data
@app.get("/api/dashboard/risk-distribution-chart", response_model=ChartDataResponse)
async def get_risk_distribution_chart():
    """Get data for the risk distribution chart"""
    try:
        assessments = get_all_risk_assessments()
        
        # Define risk categories
        risk_categories = [
            'Security', 'Privacy', 'Fairness', 'Transparency',
            'Safety', 'Accountability'
        ]
        
        # Simulate risk values for each category
        # (in a real app, these would come from detailed assessments)
        data = []
        for i, assessment in enumerate(assessments[:5]):  # Take up to 5 assessments
            # Generate pseudo-random values based on the assessment risk score
            risk_score = assessment['risk_score']
            assessment_data = [
                min(1.0, max(0.1, risk_score * (1 + (((i + category_idx) % 3) - 1) * 0.2)))
                for category_idx, _ in enumerate(risk_categories)
            ]
            data.append({
                "label": assessment['model_name'] or f"Assessment {assessment['id']}",
                "data": assessment_data,
                "backgroundColor": f"rgba(54, 162, 235, {0.2 + i * 0.15})",
                "borderColor": f"rgb(54, 162, 235)",
                "pointBackgroundColor": f"rgb(54, 162, 235)",
                "pointBorderColor": "#fff",
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": f"rgb(54, 162, 235)"
            })
        
        return {
            "labels": risk_categories,
            "datasets": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alias for backward compatibility with legacy frontend code
@app.get("/api/charts/risk-distribution", response_model=ChartDataResponse)
async def get_risk_distribution_chart_legacy():
    """Legacy endpoint for risk distribution chart"""
    return await get_risk_distribution_chart()

# Recent Activities
@app.get("/api/dashboard/activities", response_model=List[ActivityResponse])
async def get_activities():
    """Get recent activities"""
    try:
        activities = get_recent_activities(limit=10)
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alias for backward compatibility with legacy frontend code
@app.get("/api/activities/recent", response_model=List[ActivityResponse])
async def get_activities_legacy():
    """Legacy endpoint for recent activities"""
    return await get_activities()

# Policies endpoints
@app.get("/api/policies", response_model=List[PolicyResponse])
async def api_get_policies():
    """Get all governance policies"""
    try:
        policies = get_all_policies()
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/policies/{policy_id}", response_model=PolicyResponse)
async def api_get_policy(policy_id: int):
    """Get a specific policy by ID"""
    try:
        policy = get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail=f"Policy with ID {policy_id} not found")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/policies", response_model=Dict[str, Any])
async def api_create_policy(policy_request: PolicyRequest):
    """Create a new policy"""
    try:
        # Convert from Pydantic model to our domain model
        policy = Policy(
            title=policy_request.title,
            description=policy_request.description,
            category=policy_request.category,
            status=policy_request.status,
            content=policy_request.content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        policy_id = create_policy(policy)
        
        # Log the activity
        activity = Activity(
            activity_type="create",
            description=f"Created policy: {policy.title}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=policy_id,
            related_entity_type="policy"
        )
        log_activity(activity)
        
        return {"success": True, "policy_id": policy_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/policies/{policy_id}", response_model=Dict[str, Any])
async def api_update_policy(policy_id: int, policy_request: PolicyRequest):
    """Update an existing policy"""
    try:
        existing_policy = get_policy(policy_id)
        if not existing_policy:
            raise HTTPException(status_code=404, detail=f"Policy with ID {policy_id} not found")
        
        # Convert from Pydantic model to our domain model
        updated_policy = Policy(
            id=policy_id,
            title=policy_request.title,
            description=policy_request.description,
            category=policy_request.category,
            status=policy_request.status,
            content=policy_request.content,
            created_at=existing_policy.get('created_at'),
            updated_at=datetime.now()
        )
        
        success = update_policy(updated_policy)
        
        # Log the activity
        activity = Activity(
            activity_type="update",
            description=f"Updated policy: {updated_policy.title}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=policy_id,
            related_entity_type="policy"
        )
        log_activity(activity)
        
        return {"success": success}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Risk Assessments endpoints
@app.get("/api/risk-assessments", response_model=List[RiskAssessmentResponse])
async def api_get_risk_assessments():
    """Get all risk assessments"""
    try:
        assessments = get_all_risk_assessments()
        return assessments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/risk-assessments/{assessment_id}", response_model=RiskAssessmentResponse)
async def api_get_risk_assessment(assessment_id: int):
    """Get a specific risk assessment by ID"""
    try:
        assessment = get_risk_assessment(assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail=f"Risk assessment with ID {assessment_id} not found")
        return assessment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/risk-assessments", response_model=Dict[str, Any])
async def api_create_risk_assessment(assessment_request: RiskAssessmentRequest):
    """Create a new risk assessment"""
    try:
        # Convert from Pydantic model to our domain model
        assessment = RiskAssessment(
            title=assessment_request.title,
            model_name=assessment_request.model_name,
            risk_score=assessment_request.risk_score,
            findings=assessment_request.findings,
            recommendations=assessment_request.recommendations,
            status=assessment_request.status,
            created_at=datetime.now()
        )
        
        assessment_id = create_risk_assessment(assessment)
        
        # Log the activity
        activity = Activity(
            activity_type="create",
            description=f"Created risk assessment: {assessment.title}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=assessment_id,
            related_entity_type="risk_assessment"
        )
        log_activity(activity)
        
        return {"success": True, "assessment_id": assessment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Compliance Monitors endpoints
@app.get("/api/compliance-monitors", response_model=List[ComplianceMonitorResponse])
async def api_get_compliance_monitors():
    """Get all compliance monitors"""
    try:
        monitors = get_all_compliance_monitors()
        return monitors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compliance-monitors/{monitor_id}", response_model=ComplianceMonitorResponse)
async def api_get_compliance_monitor(monitor_id: int):
    """Get a specific compliance monitor by ID"""
    try:
        monitor = get_compliance_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail=f"Compliance monitor with ID {monitor_id} not found")
        return monitor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compliance-monitors", response_model=Dict[str, Any])
async def api_create_compliance_monitor(monitor_request: ComplianceMonitorRequest):
    """Create a new compliance monitor"""
    try:
        # Convert from Pydantic model to our domain model
        monitor = ComplianceMonitor(
            name=monitor_request.name,
            description=monitor_request.description,
            model_or_system=monitor_request.model_or_system,
            threshold_value=monitor_request.threshold_value,
            current_value=monitor_request.current_value,
            status=monitor_request.status,
            last_checked=datetime.now(),
            alert_level=monitor_request.alert_level
        )
        
        monitor_id = create_compliance_monitor(monitor)
        
        # Log the activity
        activity = Activity(
            activity_type="create",
            description=f"Created compliance monitor: {monitor.name}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=monitor_id,
            related_entity_type="compliance_monitor"
        )
        log_activity(activity)
        
        return {"success": True, "monitor_id": monitor_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/compliance-monitors/{monitor_id}", response_model=Dict[str, Any])
async def api_update_compliance_monitor(monitor_id: int, monitor_request: ComplianceMonitorRequest):
    """Update an existing compliance monitor"""
    try:
        existing_monitor = get_compliance_monitor(monitor_id)
        if not existing_monitor:
            raise HTTPException(status_code=404, detail=f"Compliance monitor with ID {monitor_id} not found")
        
        # Convert from Pydantic model to our domain model
        updated_monitor = ComplianceMonitor(
            id=monitor_id,
            name=monitor_request.name,
            description=monitor_request.description,
            model_or_system=monitor_request.model_or_system,
            threshold_value=monitor_request.threshold_value,
            current_value=monitor_request.current_value,
            status=monitor_request.status,
            last_checked=datetime.now(),
            alert_level=monitor_request.alert_level
        )
        
        success = update_compliance_monitor(updated_monitor)
        
        # Log the activity
        activity = Activity(
            activity_type="update",
            description=f"Updated compliance monitor: {updated_monitor.name}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=monitor_id,
            related_entity_type="compliance_monitor"
        )
        log_activity(activity)
        
        return {"success": success}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reports endpoints
@app.get("/api/reports", response_model=List[ReportResponse])
async def api_get_reports():
    """Get all reports"""
    try:
        reports = get_all_reports()
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
async def api_get_report(report_id: int):
    """Get a specific report by ID"""
    try:
        report = get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reports", response_model=Dict[str, Any])
async def api_create_report(report_request: ReportRequest):
    """Create a new report"""
    try:
        # Convert from Pydantic model to our domain model
        report = Report(
            title=report_request.title,
            description=report_request.description,
            report_type=report_request.report_type,
            content=report_request.content,
            insights=report_request.insights,
            status=report_request.status,
            created_at=datetime.now()
        )
        
        report_id = create_report(report)
        
        # Log the activity
        activity = Activity(
            activity_type="create",
            description=f"Created report: {report.title}",
            created_at=datetime.now(),
            actor="admin",
            related_entity_id=report_id,
            related_entity_type="report"
        )
        log_activity(activity)
        
        return {"success": True, "report_id": report_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
# Catch-all route to serve index.html for all non-API routes (SPA client-side routing)
# This MUST be the last route to ensure API routes are checked first
@app.get("/{path:path}")
async def serve_spa(path: str, request: Request):
    # For all non-API routes, serve the SPA's index.html
    if not request.url.path.startswith("/api/"):
        return FileResponse("static/index.html")
    
    # API routes that aren't handled by specific endpoints will return a 404
    raise HTTPException(status_code=404, detail="API endpoint not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)