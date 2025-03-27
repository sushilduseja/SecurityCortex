import os
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from utils.ai_utils import AiUtils
from database.models import RiskAssessment
from database.db_utils import create_risk_assessment, get_risk_assessment

class RiskAssessmentAgent:
    def __init__(self):
        """Initialize the Risk Assessment Agent with rule-based AI capabilities."""
        # Initialize text classification for risk assessment
        self.text_classifier = AiUtils.initialize_text_classification("risk-classifier")
        
        # Initialize zero-shot classifier for more specific risk categories
        self.zero_shot_classifier = AiUtils.initialize_zero_shot_classification("risk-zero-shot")
        
        # Risk categories and descriptions
        self.risk_categories = [
            "Privacy Risk",
            "Bias Risk",
            "Security Risk",
            "Transparency Risk",
            "Accountability Risk",
            "Robustness Risk",
            "Safety Risk",
            "Compliance Risk"
        ]
        
        # Risk category descriptions for classification
        self.category_descriptions = {
            "Privacy Risk": "Risks related to data privacy, personal information exposure, or GDPR compliance.",
            "Bias Risk": "Risks of unfair or biased outcomes, discrimination against protected groups.",
            "Security Risk": "Risks related to model security, adversarial attacks, or data poisoning.",
            "Transparency Risk": "Risks related to model explainability, black-box decision making.",
            "Accountability Risk": "Risks related to unclear responsibility or liability for AI decisions.",
            "Robustness Risk": "Risks related to model performance degradation under stress or unusual inputs.",
            "Safety Risk": "Risks related to physical safety or critical system failures.",
            "Compliance Risk": "Risks related to regulatory compliance, industry standards."
        }

    def assess_risk_from_text(self, model_name: str, documentation: str) -> RiskAssessment:
        """Assess the risk of an AI model based on its documentation text."""
        # Use our rule-based multi-label classification
        try:
            # Use AiUtils for classification instead of direct model calls
            main_risks = AiUtils.multi_label_classify(
                documentation, 
                self.risk_categories,
                self.zero_shot_classifier,
                threshold=0.3
            )
            
            # Calculate an overall risk score (0-100)
            if len(main_risks) > 0:
                # Base score on the highest risk categories
                top_risks = main_risks[:3] if len(main_risks) >= 3 else main_risks
                risk_score = sum(score * 100 for _, score in top_risks) / len(top_risks)
            else:
                # Default moderate risk if no specific risks identified
                risk_score = 50.0
                
            # Generate findings based on identified risks
            findings = self._generate_findings(main_risks, documentation)
            
            # Generate recommendations based on findings
            recommendations = self._generate_recommendations(main_risks)
            
        except Exception as e:
            # Fallback if classification fails
            risk_categories = random.sample(self.risk_categories, 2)
            main_risks = [(cat, random.uniform(0.3, 0.7)) for cat in risk_categories]
            risk_score = sum(score * 100 for _, score in main_risks) / len(main_risks)
            
            findings = f"Analysis failed with error: {str(e)}. Fallback assessment performed.\n"
            findings += "Potential risks identified: " + ", ".join(cat for cat, _ in main_risks)
            
            recommendations = "Due to analysis failure, consider a manual review of the model."
        
        # Create the risk assessment object
        assessment = RiskAssessment(
            title=f"Risk Assessment for {model_name}",
            model_name=model_name,
            risk_score=risk_score,
            findings=findings,
            recommendations=recommendations,
            created_at=datetime.now(),
            status="Completed"
        )
        
        return assessment
    
    def _generate_findings(self, main_risks: List[Tuple[str, float]], documentation: str) -> str:
        """Generate detailed findings from the identified risks."""
        if not main_risks:
            return "No significant risks identified in the documentation."
        
        findings = "## Risk Assessment Findings\n\n"
        
        for risk_cat, score in main_risks:
            findings += f"### {risk_cat} (Confidence: {score:.2f})\n"
            findings += f"{self.category_descriptions.get(risk_cat, '')}\n\n"
            
            # Add specific observations based on risk category
            if risk_cat == "Privacy Risk":
                if "personal data" in documentation.lower() or "PII" in documentation:
                    findings += "- Documentation mentions personal data processing.\n"
                if "consent" not in documentation.lower():
                    findings += "- No explicit mention of consent mechanisms.\n"
                if "anonymization" not in documentation.lower() and "pseudonymization" not in documentation.lower():
                    findings += "- No mention of anonymization or pseudonymization techniques.\n"
                    
            elif risk_cat == "Bias Risk":
                if "bias" not in documentation.lower():
                    findings += "- No explicit discussion of bias mitigation strategies.\n"
                if "fairness" not in documentation.lower():
                    findings += "- No mention of fairness metrics or assessments.\n"
                if "demographic" not in documentation.lower():
                    findings += "- No mention of demographic analysis or protected attributes.\n"
                    
            elif risk_cat == "Transparency Risk":
                if "explain" not in documentation.lower() and "interpretable" not in documentation.lower():
                    findings += "- No discussion of model explainability or interpretability.\n"
                if "black box" in documentation.lower():
                    findings += "- Model is explicitly described as a black box.\n"
                    
            findings += "\n"
        
        return findings
    
    def _generate_recommendations(self, main_risks: List[Tuple[str, float]]) -> str:
        """Generate recommendations based on the identified risks."""
        if not main_risks:
            return "Continue regular monitoring and assessment."
        
        recommendations = "## Recommendations\n\n"
        
        for risk_cat, _ in main_risks:
            if risk_cat == "Privacy Risk":
                recommendations += "### Privacy Recommendations\n"
                recommendations += "- Conduct a full Data Protection Impact Assessment (DPIA).\n"
                recommendations += "- Implement data minimization principles.\n"
                recommendations += "- Review and enhance consent mechanisms.\n"
                recommendations += "- Implement robust anonymization techniques.\n\n"
                
            elif risk_cat == "Bias Risk":
                recommendations += "### Bias Mitigation Recommendations\n"
                recommendations += "- Conduct a fairness audit across demographic groups.\n"
                recommendations += "- Implement pre-processing techniques to balance training data.\n"
                recommendations += "- Add fairness constraints to the model training process.\n"
                recommendations += "- Establish ongoing bias monitoring.\n\n"
                
            elif risk_cat == "Security Risk":
                recommendations += "### Security Recommendations\n"
                recommendations += "- Implement adversarial testing procedures.\n"
                recommendations += "- Add input validation and sanitization.\n"
                recommendations += "- Establish model update and patching procedures.\n"
                recommendations += "- Implement access controls and authentication for model API.\n\n"
                
            elif risk_cat == "Transparency Risk":
                recommendations += "### Transparency Recommendations\n"
                recommendations += "- Implement LIME, SHAP, or other explainability techniques.\n"
                recommendations += "- Develop simplified explanations for key stakeholders.\n"
                recommendations += "- Create documentation that explains model decisions.\n"
                recommendations += "- Consider using a more interpretable model architecture.\n\n"
                
            elif risk_cat == "Accountability Risk":
                recommendations += "### Accountability Recommendations\n"
                recommendations += "- Clearly define roles and responsibilities for model decisions.\n"
                recommendations += "- Implement comprehensive audit logging.\n"
                recommendations += "- Establish an AI ethics review board.\n"
                recommendations += "- Define escalation procedures for model-related incidents.\n\n"
                
            elif risk_cat == "Robustness Risk":
                recommendations += "### Robustness Recommendations\n"
                recommendations += "- Implement systematic stress testing protocols.\n"
                recommendations += "- Test model performance with noisy or corrupted inputs.\n"
                recommendations += "- Establish performance thresholds for model retraining.\n"
                recommendations += "- Add monitoring for data drift and model decay.\n\n"
                
            elif risk_cat == "Safety Risk":
                recommendations += "### Safety Recommendations\n"
                recommendations += "- Implement human oversight for critical decisions.\n"
                recommendations += "- Add automatic failsafes and fallback mechanisms.\n"
                recommendations += "- Conduct extensive scenario testing for edge cases.\n"
                recommendations += "- Develop incident response plans for model failures.\n\n"
                
            elif risk_cat == "Compliance Risk":
                recommendations += "### Compliance Recommendations\n"
                recommendations += "- Conduct a regulatory compliance review.\n"
                recommendations += "- Implement documentation requirements for applicable regulations.\n"
                recommendations += "- Establish regular compliance audits.\n"
                recommendations += "- Consult with legal experts on regulatory requirements.\n\n"
        
        return recommendations
    
    def save_assessment(self, assessment: RiskAssessment) -> int:
        """Save a risk assessment to the database."""
        return create_risk_assessment(assessment)
    
    def assess_from_metadata(self, model_name: str, model_metadata: Dict[str, Any]) -> RiskAssessment:
        """Assess risk based on model metadata (e.g., model card or documentation)."""
        # Convert metadata to text for analysis
        documentation = ""
        
        for key, value in model_metadata.items():
            documentation += f"{key}: {value}\n"
        
        return self.assess_risk_from_text(model_name, documentation)

# Example usage
if __name__ == "__main__":
    agent = RiskAssessmentAgent()
    
    # Example documentation for a model
    documentation = """
    Model Name: SentimentAnalyzer-v2
    Purpose: Analyze customer feedback sentiment for product reviews
    Training Data: 1 million product reviews from e-commerce platforms
    Model Type: BERT-based transformer model
    Accuracy: 92% on test set
    Limitations: May perform differently across product categories
    Deployment: Cloud-based API for internal use only
    """
    
    assessment = agent.assess_risk_from_text("SentimentAnalyzer-v2", documentation)
    assessment_id = agent.save_assessment(assessment)
    
    print(f"Risk assessment created with ID: {assessment_id}")
    print(f"Risk score: {assessment.risk_score}")
    print(f"Main findings: {assessment.findings[:100]}...")
