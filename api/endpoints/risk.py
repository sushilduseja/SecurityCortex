from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from agents.risk_assessment_agent import RiskAssessmentAgent
from database.db_utils import get_all_risk_assessments, get_risk_assessment, create_risk_assessment
from database.models import RiskAssessment

# Create router
router = APIRouter()

# Initialize risk assessment agent
risk_agent = RiskAssessmentAgent()

# Models for request and response
class RiskAssessmentCreate(BaseModel):
    title: str
    model_name: str
    documentation: str

class RiskAssessmentMetadata(BaseModel):
    model_name: str
    model_type: str
    description: str
    purpose: Optional[str] = None
    training_data: Optional[str] = None
    limitations: Optional[str] = None
    ethical_considerations: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None

class RiskAssessmentResponse(BaseModel):
    id: int
    title: str
    model_name: str
    risk_score: float
    findings: str
    recommendations: str
    created_at: str
    status: str

class RiskAssessmentList(BaseModel):
    items: List[RiskAssessmentResponse]
    count: int

# Get all risk assessments
@router.get("/assessments", response_model=RiskAssessmentList)
def list_risk_assessments(
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    min_risk: Optional[float] = Query(None, description="Filter by minimum risk score"),
    max_risk: Optional[float] = Query(None, description="Filter by maximum risk score")
):
    """Get all risk assessments with optional filtering."""
    try:
        assessments = get_all_risk_assessments()
        
        # Apply filters if provided
        if model_name:
            assessments = [a for a in assessments if a.get("model_name") == model_name]
        if min_risk is not None:
            assessments = [a for a in assessments if a.get("risk_score", 0) >= min_risk]
        if max_risk is not None:
            assessments = [a for a in assessments if a.get("risk_score", 100) <= max_risk]
        
        return {"items": assessments, "count": len(assessments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve risk assessments: {str(e)}")

# Get a specific risk assessment
@router.get("/assessments/{assessment_id}", response_model=RiskAssessmentResponse)
def get_assessment_by_id(assessment_id: int = Path(..., description="The ID of the risk assessment to retrieve")):
    """Get a specific risk assessment by ID."""
    try:
        assessment = get_risk_assessment(assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail=f"Risk assessment with ID {assessment_id} not found")
        return assessment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve risk assessment: {str(e)}")

# Create a risk assessment from documentation
@router.post("/assess-from-documentation", response_model=RiskAssessmentResponse)
def assess_from_documentation(assessment_data: RiskAssessmentCreate):
    """Create a risk assessment from model documentation."""
    try:
        # Use the agent to assess risk from documentation
        assessment = risk_agent.assess_risk_from_text(
            assessment_data.model_name,
            assessment_data.documentation
        )
        
        # Override title if provided
        if assessment_data.title:
            assessment.title = assessment_data.title
        
        # Save the assessment
        assessment_id = risk_agent.save_assessment(assessment)
        
        # Get the saved assessment
        created_assessment = get_risk_assessment(assessment_id)
        if not created_assessment:
            raise HTTPException(status_code=500, detail="Failed to retrieve created assessment")
        
        return created_assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create risk assessment: {str(e)}")

# Create a risk assessment from metadata
@router.post("/assess-from-metadata", response_model=RiskAssessmentResponse)
def assess_from_metadata(metadata: RiskAssessmentMetadata):
    """Create a risk assessment from model metadata."""
    try:
        # Convert metadata to dictionary
        metadata_dict = metadata.dict()
        
        # Use the agent to assess risk from metadata
        assessment = risk_agent.assess_from_metadata(
            metadata.model_name,
            metadata_dict
        )
        
        # Save the assessment
        assessment_id = risk_agent.save_assessment(assessment)
        
        # Get the saved assessment
        created_assessment = get_risk_assessment(assessment_id)
        if not created_assessment:
            raise HTTPException(status_code=500, detail="Failed to retrieve created assessment")
        
        return created_assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create risk assessment: {str(e)}")

# Get risk categories
@router.get("/categories")
def get_risk_categories():
    """Get available risk categories and descriptions."""
    try:
        return {
            "categories": risk_agent.risk_categories,
            "descriptions": risk_agent.category_descriptions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve risk categories: {str(e)}")

# Get high-risk assessments
@router.get("/high-risk", response_model=RiskAssessmentList)
def get_high_risk_assessments(threshold: float = Query(75, description="Risk score threshold for high-risk classification")):
    """Get all high-risk assessments above the specified threshold."""
    try:
        assessments = get_all_risk_assessments()
        high_risk = [a for a in assessments if a.get("risk_score", 0) >= threshold]
        
        return {"items": high_risk, "count": len(high_risk)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve high-risk assessments: {str(e)}")
