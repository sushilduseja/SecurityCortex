import os
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from transformers import pipeline
from database.models import Policy
from database.db_utils import create_policy, update_policy, get_policy

class GovernanceAgent:
    def __init__(self):
        """Initialize the Governance Agent with NLP capabilities."""
        # Initialize the text generation model for policy creation
        self.text_generator = pipeline(
            "text-generation",
            model="gpt2",
            max_length=500,
            num_return_sequences=1
        )
        
        # Initialize the text classification model for policy categorization
        self.text_classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        # Define policy templates and categories
        self.policy_categories = [
            "Data Privacy", 
            "Model Transparency", 
            "Ethical AI", 
            "Bias Mitigation",
            "Security", 
            "Compliance",
            "Accountability",
            "Human Oversight"
        ]
        
        self.policy_templates = {
            "Data Privacy": "This policy establishes guidelines for protecting personal data used in AI systems. It ensures compliance with privacy regulations and ethical standards.",
            "Model Transparency": "This policy defines requirements for making AI models explainable and transparent to stakeholders, ensuring decisions can be understood and audited.",
            "Ethical AI": "This policy outlines ethical principles that guide the development and deployment of AI systems, ensuring they align with organizational values.",
            "Bias Mitigation": "This policy establishes procedures for identifying, measuring, and mitigating bias in AI systems to ensure fair and equitable outcomes.",
            "Security": "This policy defines security requirements for AI systems, including data protection, model security, and vulnerability management.",
            "Compliance": "This policy ensures AI systems adhere to relevant laws, regulations, and industry standards throughout their lifecycle.",
            "Accountability": "This policy establishes clear roles, responsibilities, and accountability structures for AI governance within the organization.",
            "Human Oversight": "This policy defines requirements for human supervision and intervention in automated AI decision-making processes."
        }

    def generate_policy(self, category: Optional[str] = None) -> Policy:
        """Generate a new governance policy using NLP, with optional category specification."""
        # Select a category if not provided
        if not category:
            category = random.choice(self.policy_categories)
        
        # Create a title based on the category
        title = f"{category} Policy for AI Systems"
        
        # Get the template description for the category
        description = self.policy_templates.get(category, "")
        
        # Generate policy content using the text generation model
        prompt = f"Policy for {category} in AI systems:\n\n"
        try:
            generated_text = self.text_generator(prompt)[0]['generated_text']
            # Clean up the generated text, removing the prompt
            content = generated_text.replace(prompt, "").strip()
        except Exception as e:
            # Fallback if model fails
            content = f"""
            # {title}
            
            ## Purpose
            This policy establishes guidelines for {category.lower()} in AI systems.
            
            ## Scope
            This policy applies to all AI systems developed or used by the organization.
            
            ## Requirements
            1. All AI systems must be reviewed for {category.lower()} concerns.
            2. Documentation must include {category.lower()} considerations.
            3. Regular audits will be conducted to ensure compliance.
            
            ## Responsibilities
            - Data Scientists: Implement technical controls
            - AI Ethics Board: Review and approve AI systems
            - Management: Ensure resources for compliance
            
            ## Compliance Measurement
            Compliance will be measured through regular audits and assessments.
            """
        
        # Create the policy object
        policy = Policy(
            title=title,
            description=description,
            category=category,
            status="Draft",
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return policy
    
    def save_policy(self, policy: Policy) -> int:
        """Save a policy to the database."""
        return create_policy(policy)
    
    def update_policy(self, policy: Policy) -> bool:
        """Update an existing policy in the database."""
        return update_policy(policy)
    
    def analyze_policy_gaps(self, existing_policies: List[Dict[str, Any]]) -> List[str]:
        """Analyze existing policies to identify governance gaps."""
        # Extract categories from existing policies
        existing_categories = set([p.get('category', '') for p in existing_policies])
        
        # Identify missing policy categories
        missing_categories = [c for c in self.policy_categories if c not in existing_categories]
        
        return missing_categories
    
    def generate_policy_recommendations(self, existing_policies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate policy recommendations based on gap analysis."""
        missing_categories = self.analyze_policy_gaps(existing_policies)
        
        recommendations = []
        for category in missing_categories:
            recommendations.append({
                "category": category,
                "title": f"{category} Policy for AI Systems",
                "description": self.policy_templates.get(category, ""),
                "priority": "High" if category in ["Data Privacy", "Ethical AI", "Bias Mitigation"] else "Medium"
            })
        
        return recommendations

# Example usage
if __name__ == "__main__":
    agent = GovernanceAgent()
    policy = agent.generate_policy("Data Privacy")
    policy_id = agent.save_policy(policy)
    print(f"Generated and saved policy with ID: {policy_id}")
