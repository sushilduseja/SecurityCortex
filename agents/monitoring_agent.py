import os
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
from database.models import ComplianceMonitor, Activity
from database.db_utils import create_compliance_monitor, update_compliance_monitor, get_compliance_monitor, log_activity

class MonitoringAgent:
    def __init__(self):
        """Initialize the Monitoring Agent with compliance monitoring capabilities."""
        # Define standard compliance metrics
        self.standard_metrics = [
            {
                "name": "Data Privacy Compliance",
                "description": "Monitors compliance with data privacy policies and regulations",
                "typical_threshold": 0.9,  # 90% compliance is typical threshold
                "models": ["all"]
            },
            {
                "name": "Fairness Metric",
                "description": "Monitors fairness across different demographic groups",
                "typical_threshold": 0.85,  # 85% equality is typical threshold
                "models": ["classification", "recommendation"]
            },
            {
                "name": "Explainability Index",
                "description": "Tracks the explainability level of model decisions",
                "typical_threshold": 0.7,  # 70% explainability is typical threshold
                "models": ["decision", "classification"]
            },
            {
                "name": "Security Control Compliance",
                "description": "Monitors adherence to security controls and policies",
                "typical_threshold": 0.95,  # 95% compliance is typical threshold
                "models": ["all"]
            },
            {
                "name": "Documentation Completeness",
                "description": "Tracks the completeness of model documentation",
                "typical_threshold": 0.8,  # 80% completeness is typical threshold
                "models": ["all"]
            },
            {
                "name": "Model Performance Stability",
                "description": "Monitors stability of model performance over time",
                "typical_threshold": 0.9,  # 90% stability is typical threshold
                "models": ["prediction", "classification", "regression"]
            },
            {
                "name": "Data Drift Detection",
                "description": "Monitors for drift in input data distribution",
                "typical_threshold": 0.05,  # 5% drift is typical threshold (lower is better)
                "models": ["all"]
            },
            {
                "name": "Human Oversight Confirmation",
                "description": "Tracks the percentage of decisions reviewed by humans",
                "typical_threshold": 0.25,  # 25% human review is typical threshold
                "models": ["critical", "high-risk"]
            }
        ]
        
        # Alert levels and their descriptions
        self.alert_levels = {
            "Critical": "Immediate action required. Compliance threshold severely breached.",
            "Warning": "Attention needed. Compliance metrics approaching threshold limits.",
            "Normal": "All compliance metrics within acceptable thresholds.",
            "Good": "Compliance metrics exceeding minimum requirements."
        }

    def create_monitor(self, name: str, description: str, model_or_system: str, 
                      threshold_value: float) -> ComplianceMonitor:
        """Create a new compliance monitor with initial values."""
        # Start with a random initial current_value within a reasonable range of the threshold
        if threshold_value > 0.5:  # For metrics where higher is better
            # Generate a value slightly above or below the threshold
            current_value = threshold_value + random.uniform(-0.15, 0.1)
            current_value = max(0, min(1, current_value))  # Ensure it's between 0 and 1
        else:  # For metrics where lower is better (like drift)
            # Generate a value slightly above or below the threshold
            current_value = threshold_value + random.uniform(-0.02, 0.03)
            current_value = max(0, min(0.5, current_value))  # Ensure it's reasonable
        
        # Determine the alert level based on the relation between current and threshold
        alert_level = self._calculate_alert_level(current_value, threshold_value, is_lower_better=(threshold_value <= 0.5))
        
        # Create the monitor object
        monitor = ComplianceMonitor(
            name=name,
            description=description,
            model_or_system=model_or_system,
            threshold_value=threshold_value,
            current_value=current_value,
            status="Active",
            last_checked=datetime.now(),
            alert_level=alert_level
        )
        
        return monitor
    
    def create_standard_monitors(self, model_name: str, model_type: str = "all") -> List[int]:
        """Create a set of standard monitors for a given model."""
        monitor_ids = []
        
        for metric in self.standard_metrics:
            if model_type in metric["models"] or "all" in metric["models"]:
                monitor = self.create_monitor(
                    name=f"{metric['name']} - {model_name}",
                    description=metric["description"],
                    model_or_system=model_name,
                    threshold_value=metric["typical_threshold"]
                )
                
                # Save the monitor to the database
                monitor_id = create_compliance_monitor(monitor)
                monitor_ids.append(monitor_id)
                
                # Log the activity
                activity = Activity(
                    activity_type="create_monitor",
                    description=f"Created compliance monitor: {monitor.name}",
                    actor="Monitoring Agent",
                    related_entity_id=monitor_id,
                    related_entity_type="compliance_monitor"
                )
                log_activity(activity)
        
        return monitor_ids
    
    def _calculate_alert_level(self, current_value: float, threshold_value: float, is_lower_better: bool = False) -> str:
        """Calculate the alert level based on current value and threshold."""
        if is_lower_better:
            # For metrics where lower is better (e.g., drift)
            if current_value > threshold_value * 1.5:
                return "Critical"
            elif current_value > threshold_value:
                return "Warning"
            elif current_value < threshold_value * 0.5:
                return "Good"
            else:
                return "Normal"
        else:
            # For metrics where higher is better (e.g., compliance %)
            if current_value < threshold_value * 0.8:
                return "Critical"
            elif current_value < threshold_value:
                return "Warning"
            elif current_value > threshold_value * 1.1:
                return "Good"
            else:
                return "Normal"
    
    def update_monitor_value(self, monitor_id: int, new_value: Optional[float] = None) -> ComplianceMonitor:
        """Update a monitor's current value and recalculate alert level."""
        # Get the current monitor
        monitor_dict = get_compliance_monitor(monitor_id)
        if not monitor_dict:
            raise ValueError(f"Monitor with ID {monitor_id} not found")
        
        # Convert dict to ComplianceMonitor object
        monitor = ComplianceMonitor(
            id=monitor_dict["id"],
            name=monitor_dict["name"],
            description=monitor_dict["description"],
            model_or_system=monitor_dict["model_or_system"],
            threshold_value=monitor_dict["threshold_value"],
            current_value=monitor_dict["current_value"],
            status=monitor_dict["status"],
            alert_level=monitor_dict["alert_level"]
        )
        
        # If no new value provided, simulate a realistic change
        if new_value is None:
            # Determine if this is a metric where lower is better
            is_lower_better = monitor.threshold_value <= 0.5
            
            if is_lower_better:
                # For metrics like drift where lower is better
                # Small random changes, with tendency to increase over time
                change = random.uniform(-0.01, 0.02)
            else:
                # For metrics like compliance where higher is better
                # Small random changes, with cyclical patterns
                change = random.uniform(-0.03, 0.03)
            
            new_value = monitor.current_value + change
            
            # Ensure value stays in reasonable bounds
            new_value = max(0, min(1, new_value))
            if is_lower_better:
                new_value = min(0.5, new_value)  # Cap at 0.5 for lower-is-better metrics
        
        # Update the monitor
        monitor.current_value = new_value
        monitor.last_checked = datetime.now()
        monitor.alert_level = self._calculate_alert_level(
            new_value, 
            monitor.threshold_value,
            is_lower_better=(monitor.threshold_value <= 0.5)
        )
        
        # Save the updated monitor
        update_compliance_monitor(monitor)
        
        # Log an activity if the alert level changed
        if monitor.alert_level != monitor_dict["alert_level"]:
            activity = Activity(
                activity_type="alert_level_change",
                description=f"Alert level changed to {monitor.alert_level} for {monitor.name}",
                actor="Monitoring Agent",
                related_entity_id=monitor.id,
                related_entity_type="compliance_monitor"
            )
            log_activity(activity)
        
        return monitor
    
    def simulate_monitoring_cycle(self, monitors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simulate a monitoring cycle by updating all monitors."""
        updated_monitors = []
        
        for monitor_dict in monitors:
            try:
                monitor = self.update_monitor_value(monitor_dict["id"])
                updated_monitors.append({
                    "id": monitor.id,
                    "name": monitor.name,
                    "current_value": monitor.current_value,
                    "threshold_value": monitor.threshold_value,
                    "alert_level": monitor.alert_level,
                    "status": monitor.status
                })
            except Exception as e:
                print(f"Error updating monitor {monitor_dict['id']}: {str(e)}")
        
        return updated_monitors
    
    def get_compliance_summary(self, monitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of compliance status based on all monitors."""
        if not monitors:
            return {
                "overall_status": "Unknown",
                "compliance_rate": 0,
                "critical_alerts": 0,
                "warning_alerts": 0,
                "recommendations": ["No monitors available. Create compliance monitors to begin tracking."]
            }
        
        # Count alerts by level
        alert_counts = {
            "Critical": 0,
            "Warning": 0,
            "Normal": 0,
            "Good": 0
        }
        
        # Calculate compliance rate
        compliant_count = 0
        
        for monitor in monitors:
            alert_level = monitor["alert_level"]
            alert_counts[alert_level] = alert_counts.get(alert_level, 0) + 1
            
            # Consider "Normal" and "Good" as compliant
            if alert_level in ["Normal", "Good"]:
                compliant_count += 1
        
        compliance_rate = (compliant_count / len(monitors)) * 100
        
        # Determine overall status
        if alert_counts["Critical"] > 0:
            overall_status = "Critical"
        elif alert_counts["Warning"] > 0:
            overall_status = "Warning"
        elif alert_counts["Good"] > alert_counts["Normal"]:
            overall_status = "Good"
        else:
            overall_status = "Normal"
        
        # Generate recommendations
        recommendations = []
        
        if alert_counts["Critical"] > 0:
            recommendations.append("Immediate attention required for critical alerts.")
        if alert_counts["Warning"] > 0:
            recommendations.append("Address warning alerts to prevent escalation to critical.")
        if compliance_rate < 80:
            recommendations.append("Overall compliance rate is below 80%. Review governance policies.")
        if compliance_rate > 95:
            recommendations.append("Excellent compliance rate. Consider optimizing monitoring thresholds.")
        
        return {
            "overall_status": overall_status,
            "compliance_rate": round(compliance_rate, 1),
            "critical_alerts": alert_counts["Critical"],
            "warning_alerts": alert_counts["Warning"],
            "normal_monitors": alert_counts["Normal"],
            "good_monitors": alert_counts["Good"],
            "recommendations": recommendations
        }

# Example usage
if __name__ == "__main__":
    agent = MonitoringAgent()
    
    # Create standard monitors for a model
    monitor_ids = agent.create_standard_monitors("SentimentAnalyzer-v2", "classification")
    
    # Simulate a monitoring cycle
    for i in range(3):
        print(f"Monitoring cycle {i+1}")
        for monitor_id in monitor_ids:
            monitor = agent.update_monitor_value(monitor_id)
            print(f"  {monitor.name}: {monitor.current_value:.2f} ({monitor.alert_level})")
        time.sleep(1)
