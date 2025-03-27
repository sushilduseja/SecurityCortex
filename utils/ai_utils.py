import os
from typing import List, Dict, Any, Optional, Tuple
from transformers import pipeline

# Utility class for AI-related functions used across the application
class AiUtils:
    """
    Utility class for AI-related functions used in the AI Governance Dashboard.
    Provides helper methods for text generation, classification, and summarization.
    """
    
    @staticmethod
    def initialize_text_generation(model_name: str = "gpt2") -> Any:
        """
        Initialize a text generation model.
        
        Args:
            model_name: The name of the model to use
            
        Returns:
            A text generation pipeline
        """
        try:
            generator = pipeline(
                "text-generation",
                model=model_name,
                max_length=500,
                num_return_sequences=1
            )
            return generator
        except Exception as e:
            print(f"Error initializing text generation model: {str(e)}")
            return None
    
    @staticmethod
    def initialize_text_classification(model_name: str = "distilbert-base-uncased-finetuned-sst-2-english") -> Any:
        """
        Initialize a text classification model.
        
        Args:
            model_name: The name of the model to use
            
        Returns:
            A text classification pipeline
        """
        try:
            classifier = pipeline(
                "text-classification",
                model=model_name
            )
            return classifier
        except Exception as e:
            print(f"Error initializing text classification model: {str(e)}")
            return None
    
    @staticmethod
    def initialize_zero_shot_classification(model_name: str = "facebook/bart-large-mnli") -> Any:
        """
        Initialize a zero-shot classification model.
        
        Args:
            model_name: The name of the model to use
            
        Returns:
            A zero-shot classification pipeline
        """
        try:
            classifier = pipeline(
                "zero-shot-classification",
                model=model_name
            )
            return classifier
        except Exception as e:
            print(f"Error initializing zero-shot classification model: {str(e)}")
            return None
    
    @staticmethod
    def generate_text(prompt: str, generator: Optional[Any] = None, fallback: str = "") -> str:
        """
        Generate text based on a prompt.
        
        Args:
            prompt: The input prompt to generate text from
            generator: An optional text generation pipeline (will be initialized if None)
            fallback: Fallback text to return if generation fails
            
        Returns:
            Generated text
        """
        if generator is None:
            generator = AiUtils.initialize_text_generation()
        
        if generator is None:
            return fallback
        
        try:
            results = generator(prompt)
            # Clean up the generated text, removing the prompt
            generated_text = results[0]['generated_text']
            return generated_text.replace(prompt, "").strip()
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return fallback
    
    @staticmethod
    def classify_text(text: str, labels: List[str], classifier: Optional[Any] = None) -> Tuple[str, float]:
        """
        Classify text into one of the provided labels.
        
        Args:
            text: The text to classify
            labels: List of possible labels
            classifier: An optional zero-shot classifier (will be initialized if None)
            
        Returns:
            A tuple of (label, confidence)
        """
        if classifier is None:
            classifier = AiUtils.initialize_zero_shot_classification()
        
        if classifier is None:
            return (labels[0] if labels else "Unknown", 0.0)
        
        try:
            result = classifier(text, candidate_labels=labels)
            return (result['labels'][0], result['scores'][0])
        except Exception as e:
            print(f"Error classifying text: {str(e)}")
            return (labels[0] if labels else "Unknown", 0.0)
    
    @staticmethod
    def multi_label_classify(text: str, labels: List[str], classifier: Optional[Any] = None, threshold: float = 0.5) -> List[Tuple[str, float]]:
        """
        Classify text with multiple possible labels.
        
        Args:
            text: The text to classify
            labels: List of possible labels
            classifier: An optional zero-shot classifier (will be initialized if None)
            threshold: Confidence threshold for including a label
            
        Returns:
            A list of (label, confidence) tuples for labels above the threshold
        """
        if classifier is None:
            classifier = AiUtils.initialize_zero_shot_classification()
        
        if classifier is None:
            return []
        
        try:
            result = classifier(text, candidate_labels=labels, multi_label=True)
            
            # Filter results above threshold
            label_scores = [
                (label, score) for label, score in zip(result['labels'], result['scores'])
                if score >= threshold
            ]
            
            # Sort by score in descending order
            label_scores.sort(key=lambda x: x[1], reverse=True)
            
            return label_scores
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
        Analyze the sentiment of text.
        
        Args:
            text: The text to analyze
            classifier: An optional text classification pipeline (will be initialized if None)
            
        Returns:
            A tuple of (sentiment, confidence)
        """
        if classifier is None:
            classifier = AiUtils.initialize_text_classification()
        
        if classifier is None:
            return ("NEUTRAL", 0.5)
        
        try:
            result = classifier(text)[0]
            label = result['label']
            score = result['score']
            
            # Map label to sentiment
            sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
            
            return (sentiment, score)
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return ("NEUTRAL", 0.5)

# Example usage
if __name__ == "__main__":
    # Example text generation
    generated_text = AiUtils.generate_text(
        "AI governance policies should include:",
        fallback="Data privacy, ethical guidelines, and compliance with regulations."
    )
    print(f"Generated text: {generated_text}")
    
    # Example classification
    text = "This AI system processes large amounts of customer data without clear consent mechanisms."
    label, score = AiUtils.classify_text(
        text,
        ["Privacy Risk", "Security Risk", "Ethical Risk", "Compliance Risk"]
    )
    print(f"Classification: {label} (confidence: {score:.2f})")
    
    # Example multi-label classification
    text = "The model shows different accuracy rates for different demographic groups and doesn't explain its decisions."
    labels = AiUtils.multi_label_classify(
        text,
        ["Bias Risk", "Transparency Risk", "Performance Risk", "Privacy Risk"],
        threshold=0.3
    )
    print("Multi-label classification:")
    for label, score in labels:
        print(f"- {label}: {score:.2f}")
