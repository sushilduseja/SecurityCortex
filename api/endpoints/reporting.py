from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from agents.reporting_agent import ReportingAgent
from database.db_utils import get_all_reports, get_report, create_report
from database.models import Report

# Create router
router = APIRouter()

# Initialize reporting agent
reporting_agent = ReportingAgent()

# Models for request and response
class ReportResponse(BaseModel):
    id: int
    title: str
    description: str
    report_type: str
    created_at: str
    content: str
    insights: str
    status: str

class ReportList(BaseModel):
    items: List[ReportResponse]
    count: int

class ReportTypeInfo(BaseModel):
    type: str
    description: str

# Get all reports
@router.get("/reports", response_model=ReportList)
def list_reports(
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get all reports with optional filtering."""
    try:
        reports = get_all_reports()
        
        # Apply filters if provided
        if report_type:
            reports = [r for r in reports if r.get("report_type") == report_type]
        if status:
            reports = [r for r in reports if r.get("status") == status]
        
        return {"items": reports, "count": len(reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve reports: {str(e)}")

# Get a specific report
@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report_by_id(report_id: int = Path(..., description="The ID of the report to retrieve")):
    """Get a specific report by ID."""
    try:
        report = get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report: {str(e)}")

# Generate a report
@router.post("/generate", response_model=ReportResponse)
def generate_report(report_type: str = Query(..., description="Type of report to generate")):
    """Generate a new report of the specified type."""
    try:
        # Check if report type is valid
        available_types = [rt["type"] for rt in reporting_agent.get_available_report_types()]
        if report_type not in available_types:
            raise HTTPException(status_code=400, detail=f"Invalid report type. Available types: {', '.join(available_types)}")
        
        # Generate report using agent
        report_id = reporting_agent.generate_report(report_type)
        
        # Get the generated report
        report = get_report(report_id)
        if not report:
            raise HTTPException(status_code=500, detail="Failed to retrieve generated report")
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

# Get available report types
@router.get("/types", response_model=List[ReportTypeInfo])
def get_report_types():
    """Get available report types."""
    try:
        return reporting_agent.get_available_report_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report types: {str(e)}")

# Generate all report types
@router.post("/generate-all", response_model=Dict[str, Any])
def generate_all_reports():
    """Generate all available report types."""
    try:
        report_types = reporting_agent.get_available_report_types()
        generated_reports = []
        
        for report_type in report_types:
            report_id = reporting_agent.generate_report(report_type["type"])
            report = get_report(report_id)
            if report:
                generated_reports.append({
                    "id": report.get("id"),
                    "title": report.get("title"),
                    "report_type": report.get("report_type")
                })
        
        return {"generated_reports": generated_reports, "count": len(generated_reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reports: {str(e)}")
