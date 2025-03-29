from typing import Dict, Any, Type
import logging
from app.infrastructure.config.app_config import config
from app.infrastructure.messaging.notification_service import NotificationService

logger = logging.getLogger('aigovernance.container')

class Container:
    """Dependency injection container for the application."""
    
    def __init__(self):
        """Initialize the container with services."""
        self._services = {}
        self._initialize_core_services()
    
    def _initialize_core_services(self):
        """Initialize core application services."""
        # Register singleton services
        self.register_singleton('notification_service', NotificationService())
        
        # Services to be instantiated on first use
        self.register_factory('governance_agent', self._create_governance_agent)
        self.register_factory('risk_assessment_agent', self._create_risk_assessment_agent)
        self.register_factory('monitoring_agent', self._create_monitoring_agent)
        self.register_factory('reporting_agent', self._create_reporting_agent)
    
    def _create_governance_agent(self):
        """Create a new governance agent instance."""
        try:
            from app.domain.services.governance_agent import GovernanceAgent
            return GovernanceAgent()
        except ImportError:
            logger.warning("GovernanceAgent not available, using fallback")
            from app.core.governance.governance_agent import GovernanceAgent
            return GovernanceAgent()
    
    def _create_risk_assessment_agent(self):
        """Create a new risk assessment agent instance."""
        try:
            from app.domain.services.risk_assessment_agent import RiskAssessmentAgent
            return RiskAssessmentAgent()
        except ImportError:
            logger.warning("RiskAssessmentAgent not available, using fallback")
            from app.core.risk_assessment.risk_assessment_agent import RiskAssessmentAgent
            return RiskAssessmentAgent()
    
    def _create_monitoring_agent(self):
        """Create a new monitoring agent instance."""
        try:
            from app.domain.services.monitoring_agent import MonitoringAgent
            return MonitoringAgent()
        except ImportError:
            logger.warning("MonitoringAgent not available, using fallback")
            from app.core.monitoring.monitoring_agent import MonitoringAgent
            return MonitoringAgent()
    
    def _create_reporting_agent(self):
        """Create a new reporting agent instance."""
        try:
            from app.domain.services.reporting_agent import ReportingAgent
            return ReportingAgent()
        except ImportError:
            logger.warning("ReportingAgent not available, using fallback")
            from app.core.reporting.reporting_agent import ReportingAgent
            return ReportingAgent()
    
    def register_singleton(self, name: str, instance: Any):
        """
        Register a singleton service instance.
        
        Args:
            name: Service name
            instance: Service instance
        """
        self._services[name] = {'instance': instance, 'factory': None, 'singleton': True}
        logger.debug(f"Registered singleton service: {name}")
    
    def register_factory(self, name: str, factory: callable):
        """
        Register a factory function for a service.
        
        Args:
            name: Service name
            factory: Factory function to create the service
        """
        self._services[name] = {'instance': None, 'factory': factory, 'singleton': True}
        logger.debug(f"Registered factory for service: {name}")
    
    def register_transient(self, name: str, factory: callable):
        """
        Register a factory function for a transient service (new instance each time).
        
        Args:
            name: Service name
            factory: Factory function to create the service
        """
        self._services[name] = {'instance': None, 'factory': factory, 'singleton': False}
        logger.debug(f"Registered transient service: {name}")
    
    def get(self, name: str) -> Any:
        """
        Get a service instance by name.
        
        Args:
            name: Service name
            
        Returns:
            Service instance
            
        Raises:
            KeyError: If the service is not registered
        """
        if name not in self._services:
            raise KeyError(f"Service not registered: {name}")
        
        service = self._services[name]
        
        # Return existing instance if singleton
        if service['singleton'] and service['instance'] is not None:
            return service['instance']
        
        # Create new instance using factory
        if service['factory'] is not None:
            instance = service['factory']()
            # Store instance if singleton
            if service['singleton']:
                service['instance'] = instance
            return instance
        
        # Return existing instance
        return service['instance']
    
    def has(self, name: str) -> bool:
        """
        Check if a service is registered.
        
        Args:
            name: Service name
            
        Returns:
            True if the service is registered, False otherwise
        """
        return name in self._services


# Create a singleton instance
container = Container()