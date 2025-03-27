import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import json
from database.models import Report, Activity
from database.db_utils import (
    create_report, get_report, get_all_policies, 
    get_all_risk_assessments, get_all_compliance_monitors,
    log_activity
)

class ReportingAgent:
    def __init__(self):
        """Initialize the Reporting Agent."""
        # Define report types and templates
        self.report_types = [
            "Governance Summary",
            "Risk Assessment Overview",
            "Compliance Status",
            "Comprehensive Governance Report"
        ]
        
        # Report status options
        self.report_statuses = ["Draft", "Final", "Archived"]

    def generate_governance_summary(self) -> Report:
        """Generate a summary report on governance policies."""
        # Get all policies from database
        policies = get_all_policies()
        
        # Categorize policies by category and status
        categories = {}
        statuses = {"Draft": 0, "Active": 0, "Under Review": 0, "Deprecated": 0}
        
        for policy in policies:
            # Count by category
            category = policy.get("category", "Uncategorized")
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
            
            # Count by status
            status = policy.get("status", "Draft")
            if status in statuses:
                statuses[status] += 1
            else:
                statuses["Draft"] += 1
        
        # Generate insights
        insights = self._generate_governance_insights(categories, statuses, len(policies))
        
        # Create report content
        content = """
# AI Governance Summary Report

## Overview
This report provides a summary of the organization's AI governance policies and their status.

## Policy Statistics
"""
        # Add category breakdown
        content += "\n### Policies by Category\n"
        for category, count in categories.items():
            content += f"- {category}: {count} policies\n"
        
        # Add status breakdown
        content += "\n### Policies by Status\n"
        for status, count in statuses.items():
            content += f"- {status}: {count} policies\n"
        
        # Add policy listing
        content += "\n## Policy Listing\n"
        for policy in policies:
            content += f"\n### {policy.get('title', 'Untitled Policy')}\n"
            content += f"**Category:** {policy.get('category', 'Uncategorized')}\n"
            content += f"**Status:** {policy.get('status', 'Draft')}\n"
            content += f"**Created:** {policy.get('created_at', 'Unknown')}\n"
            content += f"**Description:** {policy.get('description', 'No description provided.')}\n"
        
        # Create the report
        report = Report(
            title="AI Governance Summary Report",
            description="Summary of AI governance policies and their status",
            report_type="Governance Summary",
            created_at=datetime.now(),
            content=content,
            insights=insights,
            status="Final"
        )
        
        return report
    
    def _generate_governance_insights(self, categories: Dict[str, int], 
                                     statuses: Dict[str, int], total_policies: int) -> str:
        """Generate insights for governance summary report."""
        insights = "## Key Insights\n\n"
        
        # Check for policy coverage
        if total_policies < 5:
            insights += "- **Limited Policy Coverage**: The organization has fewer than 5 governance policies. Consider developing more comprehensive governance guidelines.\n\n"
        elif total_policies > 15:
            insights += "- **Extensive Policy Framework**: The organization has a robust set of governance policies. Consider consolidating overlapping policies.\n\n"
        
        # Check for policy status
        if statuses.get("Draft", 0) > total_policies * 0.5:
            insights += "- **High Draft Rate**: More than 50% of policies are in draft status. Focus on finalizing these policies.\n\n"
        
        if statuses.get("Active", 0) < total_policies * 0.3:
            insights += "- **Low Active Policy Rate**: Less than 30% of policies are active. Accelerate policy review and activation.\n\n"
        
        # Check for policy categories
        missing_categories = []
        important_categories = ["Data Privacy", "Ethical AI", "Bias Mitigation", "Transparency", "Accountability"]
        for category in important_categories:
            if category not in categories or categories[category] == 0:
                missing_categories.append(category)
        
        if missing_categories:
            insights += f"- **Missing Key Policies**: The following important policy categories are missing: {', '.join(missing_categories)}. Consider developing policies in these areas.\n\n"
        
        # Add general recommendation
        insights += "- **Recommendation**: Regularly review and update policies to ensure they remain relevant and effective as AI technologies and regulatory requirements evolve.\n"
        
        return insights
    
    def generate_risk_assessment_overview(self) -> Report:
        """Generate an overview report on risk assessments."""
        # Get all risk assessments from database
        assessments = get_all_risk_assessments()
        
        # Calculate statistics
        avg_risk_score = 0
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for assessment in assessments:
            risk_score = assessment.get("risk_score", 50)
            avg_risk_score += risk_score
            
            if risk_score >= 75:
                high_risk_count += 1
            elif risk_score >= 50:
                medium_risk_count += 1
            else:
                low_risk_count += 1
        
        if assessments:
            avg_risk_score /= len(assessments)
        
        # Generate insights
        insights = self._generate_risk_assessment_insights(
            avg_risk_score, high_risk_count, medium_risk_count, low_risk_count, assessments
        )
        
        # Create report content
        content = """
# AI Risk Assessment Overview

## Summary
This report provides an overview of AI risk assessments conducted across the organization.

## Risk Statistics
"""
        content += f"- **Average Risk Score**: {avg_risk_score:.1f}/100\n"
        content += f"- **High Risk Models**: {high_risk_count}\n"
        content += f"- **Medium Risk Models**: {medium_risk_count}\n"
        content += f"- **Low Risk Models**: {low_risk_count}\n"
        content += f"- **Total Assessments**: {len(assessments)}\n"
        
        # Add assessment listing
        content += "\n## Recent Risk Assessments\n"
        sorted_assessments = sorted(assessments, key=lambda x: x.get("created_at", ""), reverse=True)
        for assessment in sorted_assessments[:5]:  # Show only the 5 most recent
            content += f"\n### {assessment.get('title', 'Untitled Assessment')}\n"
            content += f"**Model:** {assessment.get('model_name', 'Unknown Model')}\n"
            content += f"**Risk Score:** {assessment.get('risk_score', 0):.1f}/100\n"
            content += f"**Status:** {assessment.get('status', 'Unknown')}\n"
            content += f"**Date:** {assessment.get('created_at', 'Unknown')}\n"
            
            # Add truncated findings
            findings = assessment.get('findings', '')
            if len(findings) > 200:
                findings = findings[:200] + "..."
            content += f"\n**Key Findings:** {findings}\n"
        
        # Create the report
        report = Report(
            title="AI Risk Assessment Overview",
            description="Overview of AI risk assessments and key findings",
            report_type="Risk Assessment Overview",
            created_at=datetime.now(),
            content=content,
            insights=insights,
            status="Final"
        )
        
        return report
    
    def _generate_risk_assessment_insights(self, avg_risk_score: float, high_risk: int, 
                                          medium_risk: int, low_risk: int, 
                                          assessments: List[Dict[str, Any]]) -> str:
        """Generate insights for risk assessment overview report."""
        insights = "## Risk Insights\n\n"
        
        # Risk score insights
        if avg_risk_score >= 75:
            insights += "- **High Overall Risk**: The average risk score across AI systems is high. Immediate risk mitigation actions should be prioritized.\n\n"
        elif avg_risk_score >= 60:
            insights += "- **Elevated Risk Level**: The average risk score indicates moderate to high risk. Review high-risk systems and implement controls.\n\n"
        elif avg_risk_score >= 40:
            insights += "- **Moderate Risk Level**: The average risk score indicates acceptable risk with room for improvement.\n\n"
        else:
            insights += "- **Low Overall Risk**: The AI systems demonstrate good risk management. Continue monitoring and maintain controls.\n\n"
        
        # Distribution insights
        if high_risk > 0:
            insights += f"- **High-Risk Systems Detected**: {high_risk} systems were identified as high-risk. These should be prioritized for remediation.\n\n"
        
        if high_risk > medium_risk + low_risk:
            insights += "- **Risk Concentration**: The majority of systems are high-risk, indicating a need for organization-wide risk management improvement.\n\n"
        
        # Assessment coverage
        if len(assessments) < 3:
            insights += "- **Limited Assessment Coverage**: Few risk assessments have been conducted. Expand risk assessment to all AI systems.\n\n"
        
        # Check for recent assessments
        recent_count = 0
        thirty_days_ago = datetime.now() - timedelta(days=30)
        for assessment in assessments:
            try:
                assessment_date = datetime.fromisoformat(assessment.get("created_at", ""))
                if assessment_date > thirty_days_ago:
                    recent_count += 1
            except (ValueError, TypeError):
                pass
        
        if recent_count < len(assessments) * 0.3:
            insights += "- **Outdated Assessments**: Less than 30% of risk assessments are recent (within 30 days). Schedule regular reassessments.\n\n"
        
        # Add general recommendation
        insights += "- **Recommendation**: Implement a systematic risk assessment schedule based on the criticality of AI systems. High-risk systems should be assessed more frequently.\n"
        
        return insights
    
    def generate_compliance_status_report(self) -> Report:
        """Generate a report on compliance monitoring status."""
        # Get all compliance monitors from database
        monitors = get_all_compliance_monitors()
        
        # Calculate compliance statistics
        alert_counts = {"Critical": 0, "Warning": 0, "Normal": 0, "Good": 0}
        model_compliance = {}
        
        for monitor in monitors:
            # Count by alert level
            alert_level = monitor.get("alert_level", "Normal")
            alert_counts[alert_level] = alert_counts.get(alert_level, 0) + 1
            
            # Group by model/system
            model = monitor.get("model_or_system", "Unknown")
            if model not in model_compliance:
                model_compliance[model] = {
                    "total": 0,
                    "compliant": 0,
                    "monitors": []
                }
            
            model_compliance[model]["total"] += 1
            if alert_level in ["Normal", "Good"]:
                model_compliance[model]["compliant"] += 1
            
            model_compliance[model]["monitors"].append(monitor)
        
        # Calculate overall compliance rate
        total_monitors = len(monitors)
        compliant_monitors = alert_counts["Normal"] + alert_counts["Good"]
        compliance_rate = (compliant_monitors / total_monitors * 100) if total_monitors > 0 else 0
        
        # Generate insights
        insights = self._generate_compliance_insights(compliance_rate, alert_counts, model_compliance)
        
        # Create report content
        content = """
# AI Compliance Status Report

## Compliance Summary
"""
        content += f"- **Overall Compliance Rate**: {compliance_rate:.1f}%\n"
        content += f"- **Critical Alerts**: {alert_counts['Critical']}\n"
        content += f"- **Warning Alerts**: {alert_counts['Warning']}\n"
        content += f"- **Normal Status**: {alert_counts['Normal']}\n"
        content += f"- **Good Status**: {alert_counts['Good']}\n"
        content += f"- **Total Monitors**: {total_monitors}\n"
        
        # Add model/system compliance breakdown
        content += "\n## System Compliance Breakdown\n"
        for model, data in model_compliance.items():
            model_compliance_rate = (data["compliant"] / data["total"] * 100) if data["total"] > 0 else 0
            content += f"\n### {model}\n"
            content += f"- **Compliance Rate**: {model_compliance_rate:.1f}%\n"
            content += f"- **Compliant Monitors**: {data['compliant']}/{data['total']}\n"
            
            # Add details for non-compliant monitors
            non_compliant = [m for m in data["monitors"] if m.get("alert_level") in ["Critical", "Warning"]]
            if non_compliant:
                content += "- **Non-compliant Monitors**:\n"
                for monitor in non_compliant:
                    content += f"  - {monitor.get('name')}: {monitor.get('alert_level')} (Current: {monitor.get('current_value'):.2f}, Threshold: {monitor.get('threshold_value'):.2f})\n"
        
        # Add recent changes section
        content += "\n## Recent Compliance Changes\n"
        content += "This section tracks significant changes in compliance status over the past reporting period.\n"
        # In a real system, this would track actual changes over time
        
        # Create the report
        report = Report(
            title="AI Compliance Status Report",
            description="Current status of compliance monitoring across AI systems",
            report_type="Compliance Status",
            created_at=datetime.now(),
            content=content,
            insights=insights,
            status="Final"
        )
        
        return report
    
    def _generate_compliance_insights(self, compliance_rate: float, alert_counts: Dict[str, int], 
                                     model_compliance: Dict[str, Dict[str, Any]]) -> str:
        """Generate insights for compliance status report."""
        insights = "## Compliance Insights\n\n"
        
        # Overall compliance insights
        if compliance_rate >= 90:
            insights += "- **Strong Compliance**: The organization demonstrates excellent compliance with AI governance policies.\n\n"
        elif compliance_rate >= 80:
            insights += "- **Good Compliance**: The organization maintains good compliance with some areas for improvement.\n\n"
        elif compliance_rate >= 70:
            insights += "- **Moderate Compliance**: Several compliance gaps exist that should be addressed.\n\n"
        else:
            insights += "- **Poor Compliance**: Significant compliance issues require immediate attention.\n\n"
        
        # Critical alert insights
        if alert_counts["Critical"] > 0:
            insights += f"- **Critical Alerts**: {alert_counts['Critical']} critical compliance alerts require immediate remediation.\n\n"
        
        # Model/system insights
        high_risk_systems = []
        for model, data in model_compliance.items():
            model_compliance_rate = (data["compliant"] / data["total"] * 100) if data["total"] > 0 else 0
            if model_compliance_rate < 70 and data["total"] >= 3:
                high_risk_systems.append(model)
        
        if high_risk_systems:
            insights += f"- **High-Risk Systems**: The following systems have low compliance rates: {', '.join(high_risk_systems)}. Prioritize remediation for these systems.\n\n"
        
        # Add general recommendation
        if compliance_rate < 80:
            insights += "- **Recommendation**: Develop a compliance improvement plan focusing on critical and warning alerts. Review governance policies for clarity and implementability.\n"
        else:
            insights += "- **Recommendation**: Maintain strong compliance by continuing to monitor systems and addressing warning alerts promptly.\n"
        
        return insights
    
    def generate_comprehensive_report(self) -> Report:
        """Generate a comprehensive governance report covering all aspects."""
        # Get data from all areas
        policies = get_all_policies()
        assessments = get_all_risk_assessments()
        monitors = get_all_compliance_monitors()
        
        # Calculate key metrics
        policy_count = len(policies)
        policy_categories = set([p.get("category", "") for p in policies])
        
        avg_risk_score = 0
        for assessment in assessments:
            avg_risk_score += assessment.get("risk_score", 50)
        if assessments:
            avg_risk_score /= len(assessments)
        
        compliant_monitors = 0
        for monitor in monitors:
            if monitor.get("alert_level") in ["Normal", "Good"]:
                compliant_monitors += 1
        compliance_rate = (compliant_monitors / len(monitors) * 100) if monitors else 0
        
        # Generate comprehensive insights
        insights = self._generate_comprehensive_insights(
            policy_count, len(policy_categories), avg_risk_score, compliance_rate
        )
        
        # Create report content
        content = """
# Comprehensive AI Governance Report

## Executive Summary
This report provides a comprehensive overview of the organization's AI governance, risk management, and compliance status.

## Governance Overview
"""
        content += f"- **Total Policies**: {policy_count}\n"
        content += f"- **Policy Categories**: {len(policy_categories)}\n"
        content += f"- **Policy Coverage**: {', '.join(policy_categories)}\n"
        
        content += "\n## Risk Management\n"
        content += f"- **Risk Assessments Conducted**: {len(assessments)}\n"
        content += f"- **Average Risk Score**: {avg_risk_score:.1f}/100\n"
        
        # Add top risks section
        high_risk_assessments = [a for a in assessments if a.get("risk_score", 0) >= 75]
        if high_risk_assessments:
            content += "\n### Top Risk Areas\n"
            for assessment in sorted(high_risk_assessments, key=lambda x: x.get("risk_score", 0), reverse=True)[:3]:
                content += f"- **{assessment.get('model_name', 'Unknown Model')}**: Risk Score {assessment.get('risk_score', 0):.1f}/100\n"
        
        content += "\n## Compliance Status\n"
        content += f"- **Overall Compliance Rate**: {compliance_rate:.1f}%\n"
        content += f"- **Compliant Controls**: {compliant_monitors}/{len(monitors)}\n"
        
        # Add non-compliant controls section
        non_compliant = [m for m in monitors if m.get("alert_level") in ["Critical", "Warning"]]
        if non_compliant:
            content += "\n### Non-Compliant Controls\n"
            for monitor in sorted(non_compliant, key=lambda x: x.get("alert_level") == "Critical", reverse=True)[:5]:
                content += f"- **{monitor.get('name')}**: {monitor.get('alert_level')} Alert\n"
        
        content += "\n## Governance Maturity Assessment\n"
        
        # Calculate a simple governance maturity score
        maturity_score = 0
        if policy_count >= 10:
            maturity_score += 25
        elif policy_count >= 5:
            maturity_score += 15
        else:
            maturity_score += 5
            
        if len(assessments) >= 5:
            maturity_score += 25
        elif len(assessments) >= 2:
            maturity_score += 15
        else:
            maturity_score += 5
            
        if len(monitors) >= 8:
            maturity_score += 25
        elif len(monitors) >= 4:
            maturity_score += 15
        else:
            maturity_score += 5
            
        if compliance_rate >= 85:
            maturity_score += 25
        elif compliance_rate >= 70:
            maturity_score += 15
        else:
            maturity_score += 5
        
        # Determine maturity level
        maturity_level = "Initial"
        if maturity_score >= 80:
            maturity_level = "Optimized"
        elif maturity_score >= 60:
            maturity_level = "Managed"
        elif maturity_score >= 40:
            maturity_level = "Defined"
        elif maturity_score >= 20:
            maturity_level = "Repeatable"
        
        content += f"- **Governance Maturity Score**: {maturity_score}/100\n"
        content += f"- **Maturity Level**: {maturity_level}\n"
        
        # Create the report
        report = Report(
            title="Comprehensive AI Governance Report",
            description="Comprehensive overview of AI governance, risk, and compliance",
            report_type="Comprehensive Governance Report",
            created_at=datetime.now(),
            content=content,
            insights=insights,
            status="Final"
        )
        
        return report
    
    def _generate_comprehensive_insights(self, policy_count: int, category_count: int, 
                                        avg_risk_score: float, compliance_rate: float) -> str:
        """Generate insights for comprehensive governance report."""
        insights = "## Key Insights and Recommendations\n\n"
        
        # Governance insights
        if policy_count < 5:
            insights += "- **Governance Gap**: The organization has limited governance policies. Develop a more comprehensive policy framework.\n\n"
        elif category_count < 4:
            insights += "- **Limited Governance Scope**: Governance policies cover few categories. Expand policy coverage to address all relevant areas.\n\n"
        else:
            insights += "- **Strong Governance Framework**: The organization has a good foundation of governance policies across multiple categories.\n\n"
        
        # Risk insights
        if avg_risk_score >= 70:
            insights += "- **High Risk Environment**: The average risk score indicates significant risks that require mitigation.\n\n"
        elif avg_risk_score >= 50:
            insights += "- **Moderate Risk Environment**: Risks are present but generally manageable with proper controls.\n\n"
        else:
            insights += "- **Well-Managed Risk**: The organization demonstrates good risk management practices.\n\n"
        
        # Compliance insights
        if compliance_rate < 70:
            insights += "- **Compliance Challenges**: The organization faces significant compliance gaps that should be addressed.\n\n"
        elif compliance_rate >= 90:
            insights += "- **Strong Compliance Culture**: The organization demonstrates excellent compliance with governance requirements.\n\n"
        
        # Overall assessment
        if policy_count < 5 or avg_risk_score >= 70 or compliance_rate < 70:
            insights += "### Priority Recommendations\n"
            if policy_count < 5:
                insights += "1. Develop additional governance policies covering critical areas such as data privacy, bias mitigation, and explainability.\n"
            if avg_risk_score >= 70:
                insights += "2. Implement risk mitigation measures for high-risk AI systems, particularly those with scores above 75.\n"
            if compliance_rate < 70:
                insights += "3. Establish a compliance improvement program focusing on critical and warning-level controls.\n"
        else:
            insights += "### Continuous Improvement Recommendations\n"
            insights += "1. Regularly review and update governance policies to adapt to evolving AI technologies and regulatory requirements.\n"
            insights += "2. Expand risk assessments to cover all AI systems in the organization, prioritizing business-critical systems.\n"
            insights += "3. Enhance monitoring capabilities to provide early detection of compliance issues and emerging risks.\n"
        
        return insights
    
    def generate_report(self, report_type: str) -> int:
        """Generate a report of the specified type and save it to the database."""
        if report_type == "Governance Summary":
            report = self.generate_governance_summary()
        elif report_type == "Risk Assessment Overview":
            report = self.generate_risk_assessment_overview()
        elif report_type == "Compliance Status":
            report = self.generate_compliance_status_report()
        elif report_type == "Comprehensive Governance Report":
            report = self.generate_comprehensive_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Save the report to the database
        report_id = create_report(report)
        
        # Log the activity
        activity = Activity(
            activity_type="generate_report",
            description=f"Generated report: {report.title}",
            actor="Reporting Agent",
            related_entity_id=report_id,
            related_entity_type="report"
        )
        log_activity(activity)
        
        return report_id
    
    def get_available_report_types(self) -> List[Dict[str, str]]:
        """Get a list of available report types with descriptions."""
        return [
            {
                "type": "Governance Summary",
                "description": "Summary of governance policies and their status"
            },
            {
                "type": "Risk Assessment Overview",
                "description": "Overview of risk assessments and key findings"
            },
            {
                "type": "Compliance Status",
                "description": "Current status of compliance monitoring across AI systems"
            },
            {
                "type": "Comprehensive Governance Report",
                "description": "Comprehensive overview of governance, risk, and compliance"
            }
        ]

# Example usage
if __name__ == "__main__":
    agent = ReportingAgent()
    report_types = agent.get_available_report_types()
    
    for report_type in report_types:
        print(f"Generating {report_type['type']} report...")
        report_id = agent.generate_report(report_type["type"])
        print(f"Report generated with ID: {report_id}")
