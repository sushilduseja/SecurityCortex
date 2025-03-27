from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from agents.governance_agent import GovernanceAgent
from database.db_utils import get_all_policies, get_policy, create_policy, update_policy
from database.models import Policy

# Create router
router = APIRouter()

# Initialize governance agent
governance_agent = GovernanceAgent()

# Models for request and response
class PolicyCreate(BaseModel):
    title: str
    description: str
    category: str
    content: str
    status: str = "Draft"

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None

class PolicyResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    created_at: str
    updated_at: str
    content: str

class PolicyList(BaseModel):
    items: List[PolicyResponse]
    count: int

# Get all policies
@router.get("/policies", response_model=PolicyList)
def list_policies(
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get all governance policies with optional filtering."""
    try:
        policies = get_all_policies()
        
        # Apply filters if provided
        if category:
            policies = [p for p in policies if p.get("category") == category]
        if status:
            policies = [p for p in policies if p.get("status") == status]
        
        return {"items": policies, "count": len(policies)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve policies: {str(e)}")

# Get a specific policy
@router.get("/policies/{policy_id}", response_model=PolicyResponse)
def get_policy_by_id(policy_id: int = Path(..., description="The ID of the policy to retrieve")):
    """Get a specific governance policy by ID."""
    try:
        policy = get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail=f"Policy with ID {policy_id} not found")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve policy: {str(e)}")

# Create a new policy
@router.post("/policies", response_model=PolicyResponse)
def create_new_policy(policy_data: PolicyCreate):
    """Create a new governance policy."""
    try:
        # Create Policy object
        policy = Policy(
            title=policy_data.title,
            description=policy_data.description,
            category=policy_data.category,
            content=policy_data.content,
            status=policy_data.status,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save policy to database
        policy_id = governance_agent.save_policy(policy)
        
        # Get the saved policy
        created_policy = get_policy(policy_id)
        if not created_policy:
            raise HTTPException(status_code=500, detail="Failed to retrieve created policy")
        
        return created_policy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create policy: {str(e)}")

# Update a policy
@router.put("/policies/{policy_id}", response_model=PolicyResponse)
def update_policy_by_id(
    policy_data: PolicyUpdate,
    policy_id: int = Path(..., description="The ID of the policy to update")
):
    """Update an existing governance policy."""
    try:
        # Get existing policy
        existing_policy = get_policy(policy_id)
        if not existing_policy:
            raise HTTPException(status_code=404, detail=f"Policy with ID {policy_id} not found")
        
        # Update policy fields if provided
        policy = Policy(
            id=policy_id,
            title=policy_data.title if policy_data.title is not None else existing_policy["title"],
            description=policy_data.description if policy_data.description is not None else existing_policy["description"],
            category=policy_data.category if policy_data.category is not None else existing_policy["category"],
            content=policy_data.content if policy_data.content is not None else existing_policy["content"],
            status=policy_data.status if policy_data.status is not None else existing_policy["status"],
            updated_at=datetime.now()
        )
        
        # Update policy in database
        success = governance_agent.update_policy(policy)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update policy")
        
        # Get the updated policy
        updated_policy = get_policy(policy_id)
        return updated_policy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update policy: {str(e)}")

# Generate a policy
@router.post("/generate", response_model=PolicyResponse)
def generate_policy(category: Optional[str] = Query(None, description="Policy category to generate")):
    """Generate a new policy using the Governance Agent."""
    try:
        # Generate policy using agent
        policy = governance_agent.generate_policy(category)
        
        # Save policy to database
        policy_id = governance_agent.save_policy(policy)
        
        # Get the saved policy
        created_policy = get_policy(policy_id)
        if not created_policy:
            raise HTTPException(status_code=500, detail="Failed to retrieve generated policy")
        
        return created_policy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate policy: {str(e)}")

# Get policy recommendations
@router.get("/recommendations")
def get_policy_recommendations():
    """Get policy recommendations based on gap analysis."""
    try:
        # Get all existing policies
        policies = get_all_policies()
        
        # Generate recommendations
        recommendations = governance_agent.generate_policy_recommendations(policies)
        
        return {"recommendations": recommendations, "count": len(recommendations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

# Get available policy categories
@router.get("/categories")
def get_policy_categories():
    """Get available policy categories."""
    try:
        return {"categories": governance_agent.policy_categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve categories: {str(e)}")
