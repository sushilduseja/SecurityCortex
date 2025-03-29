from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.domain.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity

class PolicyRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all policies from the database."""
        pass
    
    @abstractmethod
    def get_by_id(self, policy_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific policy by ID."""
        pass
    
    @abstractmethod
    def create(self, policy: Policy) -> int:
        """Create a new policy and return its ID."""
        pass
    
    @abstractmethod
    def update(self, policy: Policy) -> bool:
        """Update an existing policy."""
        pass

class RiskAssessmentRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all risk assessments from the database."""
        pass
    
    @abstractmethod
    def get_by_id(self, assessment_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific risk assessment by ID."""
        pass
    
    @abstractmethod
    def create(self, assessment: RiskAssessment) -> int:
        """Create a new risk assessment and return its ID."""
        pass

class ComplianceMonitorRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all compliance monitors from the database."""
        pass
    
    @abstractmethod
    def get_by_id(self, monitor_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific compliance monitor by ID."""
        pass
    
    @abstractmethod
    def create(self, monitor: ComplianceMonitor) -> int:
        """Create a new compliance monitor and return its ID."""
        pass
    
    @abstractmethod
    def update(self, monitor: ComplianceMonitor) -> bool:
        """Update an existing compliance monitor."""
        pass

class ReportRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all reports from the database."""
        pass
    
    @abstractmethod
    def get_by_id(self, report_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific report by ID."""
        pass
    
    @abstractmethod
    def create(self, report: Report) -> int:
        """Create a new report and return its ID."""
        pass

class ActivityRepository(ABC):
    @abstractmethod
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve the most recent activities from the database."""
        pass
    
    @abstractmethod
    def log(self, activity: Activity) -> int:
        """Log a new activity and return its ID."""
        pass