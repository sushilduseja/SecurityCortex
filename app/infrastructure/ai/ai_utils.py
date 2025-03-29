import os
import random
import re
from typing import List, Dict, Any, Optional, Tuple

class AiUtils:
    """
    Utility class for AI-related functions used in the AI Governance Dashboard.
    Provides helper methods for text generation, classification, and summarization.
    """
    
    @staticmethod
    def initialize_text_generation(model_name: str = "rule-based") -> Any:
        """
        Initialize a text generation capability.
        
        Args:
            model_name: The name of the model to use (used for identification only)
            
        Returns:
            A text generation object
        """
        try:
            return {"model": model_name, "initialized": True}
        except Exception as e:
            print(f"Error initializing text generation: {str(e)}")
            return None
    
    @staticmethod
    def initialize_text_classification(model_name: str = "rule-based") -> Any:
        """
        Initialize a text classification capability.
        
        Args:
            model_name: The name of the model to use (used for identification only)
            
        Returns:
            A text classification object
        """
        try:
            return {"model": model_name, "initialized": True}
        except Exception as e:
            print(f"Error initializing text classification: {str(e)}")
            return None
    
    @staticmethod
    def initialize_zero_shot_classification(model_name: str = "rule-based") -> Any:
        """
        Initialize a zero-shot classification capability.
        
        Args:
            model_name: The name of the model to use (used for identification only)
            
        Returns:
            A zero-shot classification object
        """
        try:
            return {"model": model_name, "initialized": True}
        except Exception as e:
            print(f"Error initializing zero-shot classification: {str(e)}")
            return None
    
    @staticmethod
    def generate_text(prompt: str, generator: Optional[Any] = None, fallback: str = "") -> str:
        """
        Generate text based on a prompt using rule-based templates.
        
        Args:
            prompt: The input prompt to generate text from
            generator: An optional text generation object (will be initialized if None)
            fallback: Fallback text to return if generation fails
            
        Returns:
            Generated text
        """
        if generator is None:
            generator = AiUtils.initialize_text_generation()
        
        if generator is None:
            return fallback
        
        try:
            # Deterministic rule-based text generation using templates
            governance_templates = {
                "AI governance policies should include:": 
                    "Data privacy protection, ethical guidelines, transparency requirements, compliance with regulations, risk assessment protocols, bias mitigation strategies, and regular audit mechanisms.",
                
                "Key principles for responsible AI:": 
                    "Transparency, fairness, accountability, data privacy, human oversight, safety, and societal benefit.",
                
                "AI risk assessment framework:": 
                    "Identify AI systems, assess potential risks, evaluate impact severity, determine likelihood, implement controls, monitor continuously, and review periodically.",
                
                "Compliance requirements for AI systems:": 
                    "Data protection regulations, industry standards, ethical guidelines, transparency requirements, fairness assessments, and security protocols.",
                
                "AI monitoring best practices:": 
                    "Real-time performance tracking, bias detection, explainability verification, data quality assessment, security monitoring, and compliance validation."
            }
            
            # Find the closest template key to the prompt
            best_match = fallback
            for template_key, template_text in governance_templates.items():
                if template_key in prompt or prompt in template_key:
                    best_match = template_text
                    break
            
            return best_match
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return fallback
    
    @staticmethod
    def classify_text(text: str, labels: List[str], classifier: Optional[Any] = None) -> Tuple[str, float]:
        """
        Classify text into one of the provided labels using keyword matching.
        
        Args:
            text: The text to classify
            labels: List of possible labels
            classifier: An optional classifier object (will be initialized if None)
            
        Returns:
            A tuple of (label, confidence)
        """
        if classifier is None:
            classifier = AiUtils.initialize_zero_shot_classification()
        
        if classifier is None or not labels:
            return (labels[0] if labels else "Unknown", 0.0)
        
        try:
            # Simple rule-based classification using keyword matching
            text_lower = text.lower()
            
            # Dictionary of keywords associated with common governance categories
            keyword_map = {
                "privacy": ["privacy", "personal data", "confidential", "consent", "gdpr", "ccpa", "data protection"],
                "security": ["security", "breach", "attack", "vulnerability", "threat", "encryption", "safeguard"],
                "ethics": ["ethics", "moral", "fairness", "bias", "discrimination", "equity", "transparency", "explainable"],
                "compliance": ["compliance", "regulation", "law", "requirement", "standard", "policy", "governance"],
                "risk": ["risk", "hazard", "danger", "threat", "vulnerability", "exposure", "impact", "severity"],
                "performance": ["performance", "accuracy", "precision", "recall", "efficiency", "effectiveness", "reliability"],
                "transparency": ["transparency", "explainable", "interpretable", "understandable", "black box", "opaque"]
            }
            
            # Count matches for each label
            scores = []
            for label in labels:
                label_lower = label.lower()
                # Extract the base category from the label
                category = None
                for key in keyword_map:
                    if key in label_lower:
                        category = key
                        break
                
                if category:
                    # Count keyword matches
                    matches = sum(1 for keyword in keyword_map[category] if keyword in text_lower)
                    # Calculate a confidence score based on matches
                    confidence = min(0.5 + (matches * 0.1), 0.95)  # Cap at 0.95
                else:
                    # For labels without a keyword map, check for direct label appearances
                    if label_lower in text_lower:
                        confidence = 0.8
                    else:
                        confidence = 0.3
                
                scores.append((label, confidence))
            
            # Sort by confidence and return the best match
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[0]
        except Exception as e:
            print(f"Error classifying text: {str(e)}")
            return (labels[0] if labels else "Unknown", 0.0)
    
    @staticmethod
    def multi_label_classify(text: str, labels: List[str], classifier: Optional[Any] = None, threshold: float = 0.5) -> List[Tuple[str, float]]:
        """
        Classify text with multiple possible labels using keyword matching.
        
        Args:
            text: The text to classify
            labels: List of possible labels
            classifier: An optional classifier object (will be initialized if None)
            threshold: Confidence threshold for including a label
            
        Returns:
            A list of (label, confidence) tuples for labels above the threshold
        """
        if classifier is None:
            classifier = AiUtils.initialize_zero_shot_classification()
        
        if classifier is None or not labels:
            return []
        
        try:
            # Apply the same classification logic as classify_text but return multiple results
            text_lower = text.lower()
            
            # Dictionary of keywords associated with common governance categories
            keyword_map = {
                "privacy": ["privacy", "personal data", "confidential", "consent", "gdpr", "ccpa", "data protection"],
                "security": ["security", "breach", "attack", "vulnerability", "threat", "encryption", "safeguard"],
                "ethics": ["ethics", "moral", "fairness", "bias", "discrimination", "equity", "transparency", "explainable"],
                "compliance": ["compliance", "regulation", "law", "requirement", "standard", "policy", "governance"],
                "risk": ["risk", "hazard", "danger", "threat", "vulnerability", "exposure", "impact", "severity"],
                "performance": ["performance", "accuracy", "precision", "recall", "efficiency", "effectiveness", "reliability"],
                "transparency": ["transparency", "explainable", "interpretable", "understandable", "black box", "opaque"],
                "bias": ["bias", "fairness", "discrimination", "equity", "diversity", "inclusion", "representation"]
            }
            
            # Calculate scores for each label
            scores = []
            for label in labels:
                label_lower = label.lower()
                # Extract the base category from the label
                category = None
                for key in keyword_map:
                    if key in label_lower:
                        category = key
                        break
                
                if category:
                    # Count keyword matches
                    matches = sum(1 for keyword in keyword_map[category] if keyword in text_lower)
                    # Calculate a confidence score based on matches
                    confidence = min(0.5 + (matches * 0.1), 0.95)  # Cap at 0.95
                else:
                    # For labels without a keyword map, check for direct label appearances
                    if label_lower in text_lower:
                        confidence = 0.8
                    else:
                        confidence = 0.3
                
                scores.append((label, confidence))
            
            # Filter by threshold and sort by confidence
            result = [item for item in scores if item[1] >= threshold]
            result.sort(key=lambda x: x[1], reverse=True)
            
            return result
        except Exception as e:
            print(f"Error multi-label classifying text: {str(e)}")
            return []
    
    @staticmethod
    def extract_key_points(text: str, num_points: int = 3) -> List[str]:
        """
        Extract key points from text using NLP techniques.
        This is a simple implementation; a more sophisticated one would use a summarization model.
        
        Args:
            text: The input text
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        # Simple implementation - split text into sentences and return the first num_points
        sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
        
        if len(sentences) <= num_points:
            return sentences
        
        # For a simple implementation, return first, middle and last sentences
        if num_points == 3 and len(sentences) > 4:
            return [
                sentences[0],
                sentences[len(sentences) // 2],
                sentences[-2]
            ]
        
        # Otherwise return the first num_points sentences
        return sentences[:num_points]
    
    @staticmethod
    def analyze_sentiment(text: str, classifier: Optional[Any] = None) -> Tuple[str, float]:
        """
        Analyze the sentiment of text using keyword matching.
        
        Args:
            text: The text to analyze
            classifier: An optional classifier object (will be initialized if None)
            
        Returns:
            A tuple of (sentiment, confidence)
        """
        if classifier is None:
            classifier = AiUtils.initialize_text_classification()
        
        if classifier is None:
            return ("NEUTRAL", 0.5)
        
        try:
            # Simple rule-based sentiment analysis
            text_lower = text.lower()
            
            # Lists of positive and negative keywords for governance context
            positive_keywords = [
                "compliant", "secure", "protected", "ethical", "transparent", "responsible", 
                "trustworthy", "reliable", "fair", "unbiased", "robust", "accountable",
                "verified", "validated", "safe", "beneficial", "effective", "improved",
                "enhancement", "success", "strength", "advantage", "opportunity"
            ]
            
            negative_keywords = [
                "non-compliant", "insecure", "unprotected", "unethical", "opaque", "irresponsible",
                "untrustworthy", "unreliable", "unfair", "biased", "weak", "unaccountable",
                "unverified", "unvalidated", "unsafe", "harmful", "ineffective", "degraded",
                "violation", "fail", "failure", "risk", "threat", "vulnerability", "issue", "concern"
            ]
            
            # Count matches
            positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
            negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
            
            # Determine sentiment based on counts
            if positive_count > negative_count:
                score = min(0.5 + ((positive_count - negative_count) * 0.05), 0.95)
                return ("POSITIVE", score)
            elif negative_count > positive_count:
                score = min(0.5 + ((negative_count - positive_count) * 0.05), 0.95)
                return ("NEGATIVE", score)
            else:
                # If counts are equal, check for strong negative indicators
                strong_negatives = ["risk", "violation", "fail", "threat"]
                if any(neg in text_lower for neg in strong_negatives):
                    return ("NEGATIVE", 0.6)
                # Otherwise neutral
                return ("NEUTRAL", 0.5)
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return ("NEUTRAL", 0.5)