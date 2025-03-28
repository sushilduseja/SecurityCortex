import sqlite3
import os
import datetime
from database.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity
from database.db_utils_sqlite import DB_PATH, get_db_connection

def init_db():
    """Initialize the SQLite database with the required tables if they don't exist."""
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT,
        content TEXT
    );
    
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        model_name TEXT,
        risk_score REAL,
        findings TEXT,
        recommendations TEXT,
        created_at TEXT,
        status TEXT
    );
    
    CREATE TABLE IF NOT EXISTS compliance_monitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        model_or_system TEXT,
        threshold_value REAL,
        current_value REAL,
        status TEXT,
        last_checked TEXT,
        alert_level TEXT
    );
    
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        report_type TEXT,
        created_at TEXT,
        content TEXT,
        insights TEXT,
        status TEXT
    );
    
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_type TEXT,
        description TEXT,
        created_at TEXT,
        actor TEXT,
        related_entity_id INTEGER,
        related_entity_type TEXT
    );
    ''')
    
    conn.commit()
    
    # Check if we need to preload data (only if tables are empty)
    cursor.execute('SELECT COUNT(*) as count FROM policies')
    policy_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM risk_assessments')
    assessment_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM compliance_monitors')
    monitor_count = cursor.fetchone()['count']
    
    # If tables are empty, preload sample data
    if policy_count == 0 and assessment_count == 0 and monitor_count == 0:
        preload_sample_data(conn)
    
    cursor.close()
    conn.close()
    
    print("Database initialized successfully.")

def preload_sample_data(conn):
    """Preload sample data aligned with NIST AI Risk Management Framework."""
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    # Sample Policies based on NIST AI RMF
    policies = [
        Policy(
            title="AI System Documentation Policy",
            description="Requirements for documenting AI systems throughout their lifecycle",
            category="Documentation",
            status="Active",
            content="""
# AI System Documentation Policy

## Purpose
This policy establishes the documentation requirements for all AI systems throughout their lifecycle to ensure transparency, reproducibility, and proper governance.

## Scope
This policy applies to all AI systems developed, deployed, or used within the organization.

## Requirements
1. All AI systems must maintain comprehensive documentation including:
   - System purpose and intended use cases
   - Training data sources, selection criteria, and preprocessing steps
   - Model architecture, hyperparameters, and training methodology
   - Performance metrics and evaluation results
   - Identified limitations and potential risks
   - Deployment environment and integration requirements
   - Monitoring plan and maintenance procedures

2. Documentation must be updated when significant changes occur to the AI system.

3. Documentation must be accessible to all relevant stakeholders.

4. Annual reviews of documentation must be conducted to ensure accuracy and completeness.
            """
        ),
        Policy(
            title="AI Risk Assessment Framework",
            description="Procedures for identifying, evaluating and mitigating AI-related risks",
            category="Risk Management",
            status="Active",
            content="""
# AI Risk Assessment Framework

## Purpose
This framework establishes a standardized approach for identifying, evaluating, and mitigating risks associated with AI systems.

## Risk Assessment Process
1. **Identification**: Document all potential risks including technical, operational, ethical, legal, and reputational risks.

2. **Analysis**: Evaluate the likelihood and potential impact of each identified risk using the following scale:
   - Low: Minimal impact, easily addressed
   - Medium: Moderate impact, requires planned response
   - High: Significant impact, requires immediate attention
   - Critical: Severe impact, could cause major harm or legal issues

3. **Mitigation**: Develop and implement strategies to mitigate each identified risk.

4. **Monitoring**: Establish ongoing monitoring procedures to detect emerging risks.

5. **Review**: Conduct quarterly reviews of risk assessments and update as needed.

## Documentation Requirements
All risk assessments must be documented and maintained in the centralized risk register.
            """
        ),
        Policy(
            title="Responsible AI Development Guidelines",
            description="Ethical principles and guidelines for responsible AI development",
            category="Ethics",
            status="Active",
            content="""
# Responsible AI Development Guidelines

## Purpose
These guidelines establish ethical principles and practices for the responsible development and deployment of AI systems.

## Core Principles
1. **Fairness**: AI systems should be designed to avoid creating or reinforcing unfair bias.

2. **Transparency**: The operation and decision-making processes of AI systems should be explainable and understandable to relevant stakeholders.

3. **Privacy**: AI systems should respect user privacy and adhere to data protection regulations.

4. **Security**: AI systems should be designed with security considerations at all stages of development.

5. **Accountability**: Clear lines of responsibility and accountability must be established for all AI systems.

6. **Human Oversight**: Human oversight and intervention capabilities must be maintained for all automated decision-making systems.

## Implementation Requirements
All AI development teams must:
1. Complete responsible AI training annually
2. Conduct fairness assessments before deployment
3. Document all ethical considerations and decisions
4. Establish feedback mechanisms for users
            """
        ),
        Policy(
            title="AI Model Performance Monitoring Policy",
            description="Requirements for ongoing monitoring of AI model performance",
            category="Monitoring",
            status="Active",
            content="""
# AI Model Performance Monitoring Policy

## Purpose
This policy establishes requirements for the ongoing monitoring of AI model performance to ensure continued effectiveness, reliability, and safety.

## Monitoring Requirements
1. **Baseline Metrics**: Establish baseline performance metrics during development and validation.

2. **Key Performance Indicators**: Define and track appropriate KPIs for each AI model, including:
   - Accuracy metrics relevant to the specific use case
   - Fairness metrics across different demographic groups
   - Drift indicators to detect shifts in data distributions
   - Operational metrics (response time, resource usage)

3. **Monitoring Frequency**: Implement continuous monitoring for production models with:
   - Real-time alerting for critical issues
   - Daily performance reports
   - Weekly comprehensive reviews
   - Monthly trend analysis

4. **Thresholds and Alerts**: Establish thresholds for each KPI that trigger alerts when exceeded.

5. **Response Procedures**: Define clear procedures for responding to performance degradation.

## Documentation Requirements
All monitoring activities, findings, and responses must be documented in the AI governance system.
            """
        ),
        Policy(
            title="AI Testing and Validation Standards",
            description="Standards for testing and validating AI systems before deployment",
            category="Quality Assurance",
            status="Active",
            content="""
# AI Testing and Validation Standards

## Purpose
These standards establish requirements for the comprehensive testing and validation of AI systems prior to deployment.

## Testing Requirements
1. **Validation Dataset Requirements**: 
   - Must be representative of the intended operational environment
   - Must be separate from training and testing datasets
   - Must include edge cases and potential corner scenarios

2. **Performance Testing**:
   - Accuracy metrics appropriate to the use case
   - Reliability testing under various conditions
   - Stress testing to identify breaking points
   - Response time and resource usage evaluation

3. **Fairness Testing**:
   - Evaluate performance across different demographic groups
   - Identify and address potential bias issues
   - Document fairness considerations and trade-offs

4. **Security Testing**:
   - Vulnerability assessment
   - Adversarial attack resistance
   - Data poisoning resistance

5. **Integration Testing**:
   - End-to-end system testing
   - API and interface testing
   - Compatibility with existing systems

## Documentation Requirements
Test plans, procedures, results, and validation reports must be documented and maintained for each AI system.
            """
        ),
        Policy(
            title="AI Compliance Requirements Policy",
            description="Guidelines for ensuring AI systems comply with relevant regulations",
            category="Compliance",
            status="Active",
            content="""
# AI Compliance Requirements Policy

## Purpose
This policy establishes requirements for ensuring AI systems comply with all relevant laws, regulations, and industry standards.

## Compliance Areas
1. **Data Protection and Privacy**:
   - GDPR compliance for EU-related activities
   - CCPA compliance for California-related activities
   - Other applicable privacy laws based on operational regions

2. **Anti-discrimination and Fairness**:
   - Equal opportunity laws
   - Sector-specific fairness requirements

3. **Transparency and Explainability**:
   - Disclosure requirements for automated decision-making
   - Right to explanation where applicable

4. **Industry-Specific Regulations**:
   - Financial services regulations (if applicable)
   - Healthcare regulations (if applicable)
   - Other sector-specific requirements

## Implementation Requirements
1. Conduct compliance assessment before deployment of any new AI system
2. Document all compliance considerations and measures
3. Establish regular compliance audits and reviews
4. Maintain awareness of regulatory developments
            """
        ),
        Policy(
            title="Data Quality Standards for AI",
            description="Standards for data used in AI training and operations",
            category="Data Governance",
            status="Draft",
            content="""
# Data Quality Standards for AI

## Purpose
These standards establish requirements for ensuring the quality, integrity, and appropriateness of data used for AI system training and operations.

## Data Quality Requirements
1. **Accuracy**: Data must accurately represent the real-world entities, events, or phenomena it describes.

2. **Completeness**: Data must contain all necessary elements for its intended use.

3. **Consistency**: Data must be consistent across all sources and over time.

4. **Timeliness**: Data must be sufficiently current for its intended use.

5. **Representativeness**: Data must adequately represent the population or environment in which the AI system will operate.

6. **Provenance**: Origin and lineage of all data must be documented.

## Data Quality Procedures
1. Data profiling to identify quality issues
2. Data cleaning to address identified issues
3. Ongoing data quality monitoring
4. Regular data quality audits

## Documentation Requirements
All data quality assessments, procedures, and interventions must be documented and maintained.
            """
        )
    ]
    
    # Sample Risk Assessments based on NIST AI RMF
    risk_assessments = [
        RiskAssessment(
            title="Facial Recognition System Risk Assessment",
            model_name="FaceDetect-v2",
            risk_score=78.5,
            findings="""
## Key Findings

1. **Demographic Performance Disparities**: The system demonstrates variable accuracy rates across different demographic groups, with higher error rates for certain ethnicities and age groups.

2. **Environmental Limitations**: Performance significantly degrades in low-light conditions and with certain camera angles, potentially creating operational blind spots.

3. **Lack of Explainability Mechanisms**: The system provides confidence scores but lacks detailed explanations for its identifications, creating a "black box" problem for operators.

4. **Data Provenance Concerns**: Training data includes datasets with unclear consent and licensing status, creating potential legal and ethical exposures.

5. **Integration Security Vulnerabilities**: API endpoints lack comprehensive authentication measures, creating potential for unauthorized access.
            """,
            recommendations="""
## Recommendations

1. **Implement Fairness Interventions**: Enhance training data diversity and implement algorithmic fairness techniques to address demographic performance disparities.

2. **Enhance Environmental Robustness**: Deploy pre-processing modules to improve performance in challenging environmental conditions.

3. **Develop Explainability Layer**: Implement LIME or SHAP explanations for high-stakes identifications to improve operator understanding.

4. **Conduct Data Audit**: Review all training data sources and replace problematic datasets with properly licensed alternatives.

5. **Strengthen API Security**: Implement OAuth 2.0 with role-based access controls for all system interfaces.

6. **Create Human Review Process**: Establish procedures for human review of high-impact decisions.
            """,
            status="High Risk"
        ),
        RiskAssessment(
            title="Natural Language Processing Risk Assessment",
            model_name="TextAnalyzer-Pro",
            risk_score=62.3,
            findings="""
## Key Findings

1. **Content Moderation Gaps**: The system occasionally fails to detect subtle forms of harmful content, particularly culturally-specific expressions.

2. **Bias in Sentiment Analysis**: Sentiment analysis shows varying accuracy based on dialect, regional expressions, and cultural context.

3. **Hallucination in Text Generation**: When used for generation, the model occasionally produces factually incorrect or misleading information.

4. **Privacy Leakage Risk**: The model may occasionally reproduce verbatim text from training data, creating potential privacy exposures.

5. **Resource Intensive Operation**: The model's computational requirements limit real-time application in resource-constrained environments.
            """,
            recommendations="""
## Recommendations

1. **Enhance Content Filters**: Develop and implement improved detection mechanisms for culturally-specific harmful content.

2. **Dialect and Expression Training**: Augment training data with more diverse linguistic expressions and develop dialect-specific calibrations.

3. **Implement Fact-Checking Layer**: Add a verification mechanism for factual claims in generated content.

4. **Privacy Enhancement**: Implement differential privacy techniques and content filtering to reduce verbatim reproduction.

5. **Model Optimization**: Develop a distilled version of the model for deployment in resource-constrained environments.

6. **Implement User Feedback Mechanisms**: Create channels for users to report model failures and problematic outputs.
            """,
            status="Medium Risk"
        ),
        RiskAssessment(
            title="Predictive Maintenance AI Risk Assessment",
            model_name="MaintenancePredictor",
            risk_score=45.7,
            findings="""
## Key Findings

1. **Imbalanced Failure Data**: The model has been trained on limited failure examples, potentially reducing its ability to detect rare failure modes.

2. **Sensor Data Quality Issues**: Input data from older sensors shows inconsistent quality, affecting prediction reliability for legacy equipment.

3. **Alert Fatigue Potential**: Current threshold settings may generate excessive alerts, creating risk of operator desensitization.

4. **Limited Causal Insights**: The model identifies potential failures but provides limited insight into underlying causes.

5. **Integration Complexity**: Complex integration requirements with existing maintenance systems create potential points of failure.
            """,
            recommendations="""
## Recommendations

1. **Synthetic Data Augmentation**: Generate synthetic failure examples to improve detection of rare failure modes.

2. **Sensor Quality Normalization**: Implement preprocessing to normalize data quality from older sensors.

3. **Dynamic Alert Thresholds**: Develop adaptive thresholding based on historical alert patterns and operator responses.

4. **Causal Factor Analysis**: Enhance the model with additional features to identify potential causal factors in predicted failures.

5. **Integration Middleware**: Develop dedicated middleware layer to simplify integration with existing maintenance systems.

6. **Implement Feedback Loop**: Create structured process for maintenance technicians to provide feedback on prediction accuracy.
            """,
            status="Medium Risk"
        ),
        RiskAssessment(
            title="Credit Scoring Model Risk Assessment",
            model_name="CreditRisk-AI",
            risk_score=83.2,
            findings="""
## Key Findings

1. **Disparate Impact Concerns**: The model shows statistically significant differences in approval rates across protected demographic groups.

2. **Limited Explainability**: Complex model structure limits ability to provide clear explanations for credit decisions.

3. **Sensitivity to Economic Shifts**: Model performance degraded during simulated economic downturn scenarios.

4. **Data Staleness Issues**: Some training data features reflect historical patterns that may no longer be relevant.

5. **Regulatory Compliance Gaps**: Current implementation may not fully satisfy explainability requirements in certain jurisdictions.
            """,
            recommendations="""
## Recommendations

1. **Fairness Constraints**: Implement algorithmic fairness constraints to mitigate disparate impact while preserving model performance.

2. **Develop Interpretable Companion Model**: Create simpler, more interpretable companion model for explanation purposes.

3. **Economic Scenario Testing**: Enhance testing with more diverse economic scenarios and implement adaptive calibration.

4. **Feature Refresh Program**: Establish program to regularly assess and update feature relevance.

5. **Jurisdictional Compliance Review**: Conduct comprehensive review of explainability requirements across all operating jurisdictions.

6. **Human Review Process**: Implement human review for all rejected applications with borderline scores.
            """,
            status="High Risk"
        ),
        RiskAssessment(
            title="Healthcare Diagnostic AI Risk Assessment",
            model_name="MedicalDiagnostic-AI",
            risk_score=91.5,
            findings="""
## Key Findings

1. **Clinical Validation Gaps**: Validation has not covered all patient demographics and comorbidity combinations.

2. **Workflow Integration Risks**: Integration with clinical workflows creates potential for decision-making confusion between AI and healthcare providers.

3. **Explainability Limitations**: The system provides diagnoses with confidence scores but limited supporting evidence or reasoning.

4. **Data Privacy Vulnerabilities**: Current architecture may create protected health information exposures in certain integration scenarios.

5. **Over-reliance Risk**: Testing indicates potential for healthcare provider over-reliance on system recommendations.
            """,
            recommendations="""
## Recommendations

1. **Expanded Validation Study**: Conduct additional validation across broader patient demographics and clinical scenarios.

2. **Workflow Design Review**: Engage clinical UX specialists to redesign integration points to clarify decision authority.

3. **Evidence Enhancement**: Augment system outputs with supporting evidence, relevant literature, and reasoning factors.

4. **Privacy Architecture Redesign**: Implement enhanced anonymization and data protection measures throughout the processing pipeline.

5. **Clinical Training Program**: Develop training for healthcare providers on appropriate system use, limitations, and override procedures.

6. **Monitoring Framework**: Implement comprehensive monitoring of system recommendations and provider interactions.
            """,
            status="Critical Risk"
        )
    ]
    
    # Sample Compliance Monitors based on NIST AI RMF
    compliance_monitors = [
        ComplianceMonitor(
            name="Fairness Compliance Monitor",
            description="Monitors AI system outputs for demographic performance disparities",
            model_or_system="All ML Systems",
            threshold_value=0.10,
            current_value=0.08,
            status="Active",
            alert_level="Normal"
        ),
        ComplianceMonitor(
            name="Privacy Control Monitor",
            description="Tracks compliance with data privacy requirements",
            model_or_system="Data Processing Pipeline",
            threshold_value=0.95,
            current_value=0.97,
            status="Active",
            alert_level="Normal"
        ),
        ComplianceMonitor(
            name="Model Accuracy Drift Monitor",
            description="Detects drift in model accuracy compared to baseline",
            model_or_system="CreditRisk-AI",
            threshold_value=0.05,
            current_value=0.02,
            status="Active",
            alert_level="Normal"
        ),
        ComplianceMonitor(
            name="Data Quality Monitor",
            description="Monitors quality metrics for training and inference data",
            model_or_system="All Data Sources",
            threshold_value=0.95,
            current_value=0.96,
            status="Active",
            alert_level="Normal"
        ),
        ComplianceMonitor(
            name="Explainability Compliance Monitor",
            description="Tracks compliance with explainability requirements",
            model_or_system="Medical Diagnostic AI",
            threshold_value=0.90,
            current_value=0.83,
            status="Active",
            alert_level="Warning"
        ),
        ComplianceMonitor(
            name="Security Vulnerability Monitor",
            description="Monitors for security vulnerabilities in AI systems",
            model_or_system="All AI Infrastructure",
            threshold_value=0.98,
            current_value=0.99,
            status="Active",
            alert_level="Normal"
        ),
        ComplianceMonitor(
            name="Demographic Performance Parity",
            description="Monitors performance differences across demographic groups",
            model_or_system="FaceDetect-v2",
            threshold_value=0.05,
            current_value=0.12,
            status="Active",
            alert_level="Critical"
        ),
        ComplianceMonitor(
            name="Documentation Compliance Monitor",
            description="Tracks compliance with documentation requirements",
            model_or_system="All AI Systems",
            threshold_value=0.90,
            current_value=0.86,
            status="Active",
            alert_level="Warning"
        )
    ]
    
    # Sample Reports based on NIST AI RMF
    reports = [
        Report(
            title="Quarterly AI Governance Summary",
            description="Summary of AI governance activities for Q1 2025",
            report_type="governance_summary",
            content="""
# Quarterly AI Governance Summary - Q1 2025

## Overview
This report provides a summary of AI governance activities and metrics for the first quarter of 2025.

## Key Metrics
- **Total Active Policies**: 6
- **Policy Categories**: Documentation, Risk Management, Ethics, Monitoring, Quality Assurance, Compliance
- **Policy Compliance Rate**: 92%
- **Open Policy Review Items**: 3

## Policy Updates
- Implemented new Data Quality Standards policy (draft status)
- Updated AI Compliance Requirements to reflect new EU regulations
- Reviewed and reaffirmed 4 existing policies

## Recommendations
1. Finalize the Data Quality Standards policy in Q2
2. Develop additional policies for AI incident response
3. Enhance policy awareness through targeted training sessions
            """,
            insights="""
## Key Insights

The organization's AI governance framework is maturing well with a comprehensive set of policies covering key risk areas. Policy awareness and compliance are strong, though there are opportunities to further enhance specific domain policies.

The implementation of operational controls to enforce policy requirements remains an area for continued focus, particularly for newer AI systems being deployed across the organization.

Recommend increasing governance team engagement with AI development teams during early project phases to ensure governance requirements are incorporated from the outset.
            """,
            status="Published"
        ),
        Report(
            title="AI Risk Assessment Overview",
            description="Summary of AI system risk assessments",
            report_type="risk_assessment_overview",
            content="""
# AI Risk Assessment Overview - March 2025

## Overview
This report summarizes the risk assessment status and findings across all AI systems in the organization.

## Risk Assessment Metrics
- **Total Systems Assessed**: 5
- **Average Risk Score**: 72.3
- **Risk Distribution**:
  - Critical Risk: 1 systems
  - High Risk: 2 systems
  - Medium Risk: 2 systems
  - Low Risk: 0 systems

## Common Risk Areas
1. **Fairness and Bias**: 4 of 5 systems identified fairness concerns
2. **Explainability**: 3 of 5 systems have limited explainability
3. **Data Quality**: 3 of 5 systems identified data quality issues
4. **Privacy**: 2 of 5 systems have privacy vulnerabilities
5. **Integration Complexity**: 2 of 5 systems have integration challenges

## High Priority Remediation Areas
1. Address critical risks in Medical Diagnostic AI system
2. Implement fairness interventions for high-risk systems
3. Enhance explainability for credit scoring system
            """,
            insights="""
## Key Insights

Risk assessments reveal a pattern of challenges around model fairness and explainability across multiple systems. These issues appear to stem from common root causes in development practices and testing procedures.

The highest risk systems share characteristics of high autonomy, limited human oversight, and operation in regulated domains. Recommend developing enhanced governance controls specifically tailored to systems with these characteristics.

There is an opportunity to develop reusable remediation approaches for common risk patterns, particularly for fairness testing and explainability enhancements.
            """,
            status="Published"
        ),
        Report(
            title="Compliance Monitoring Status",
            description="Status of AI compliance monitoring program",
            report_type="compliance_status",
            content="""
# AI Compliance Monitoring Status - March 2025

## Overview
This report summarizes the status of compliance monitoring across AI systems in the organization.

## Monitoring Metrics
- **Total Active Monitors**: 8
- **Compliance Rate**: 75% (6 of 8 monitors within thresholds)
- **Alert Distribution**:
  - Normal: 6 monitors
  - Warning: 2 monitors
  - Critical: 1 monitor

## Non-Compliant Areas
1. **FaceDetect-v2 Demographic Performance**: Performance disparities exceed threshold (0.12 vs 0.05 threshold)
2. **Medical Diagnostic AI Explainability**: Below required explainability threshold (0.83 vs 0.90 threshold)
3. **Documentation Compliance**: Slightly below requirement (0.86 vs 0.90 threshold)

## Monitoring Program Updates
- Implemented 2 new monitors this quarter
- Enhanced alert sensitivity for fairness monitors
- Improved monitoring dashboard for real-time visibility
            """,
            insights="""
## Key Insights

The compliance monitoring program is effectively identifying areas where AI systems are deviating from governance requirements. Most systems maintain compliance with established thresholds, with specific exceptions requiring intervention.

The pattern of compliance issues suggests that explainability requirements and demographic performance parity are the most challenging areas for teams to consistently maintain compliance.

Recommend developing focused technical enablement resources to help teams address these common compliance challenges more effectively.
            """,
            status="Published"
        ),
        Report(
            title="Comprehensive AI Governance Report",
            description="Comprehensive overview of AI governance program",
            report_type="comprehensive_report",
            content="""
# Comprehensive AI Governance Report - Q1 2025

## Executive Summary
This report provides a comprehensive overview of the organization's AI governance program, covering policies, risk assessments, compliance monitoring, and key recommendations.

## Governance Framework Status
- **Policy Framework**: 7 policies (6 active, 1 draft)
- **Risk Assessment**: 5 systems assessed
- **Compliance Monitoring**: 8 active monitors
- **Governance Maturity**: Level 3 (Defined)

## Key Metrics
- **Average Risk Score**: 72.3
- **Compliance Rate**: 75%
- **Policy Implementation**: 92%
- **Governance Coverage**: 85% of production AI systems

## Achievements
1. Completed risk assessments for all high-priority AI systems
2. Implemented comprehensive compliance monitoring program
3. Developed and deployed 6 governance policies
4. Established governance review process for new AI initiatives

## Key Challenges
1. Demographic performance disparities in facial recognition system
2. Explainability limitations in high-risk systems
3. Documentation compliance below targets
4. Resource constraints for governance activities

## Strategic Recommendations
1. Enhance fairness testing capabilities across development teams
2. Develop standardized explainability approaches for high-risk domains
3. Implement automated documentation compliance tooling
4. Expand governance coverage to remaining AI systems
            """,
            insights="""
## Key Insights

The organization has established a solid foundation for AI governance with appropriate policies, risk assessment methodologies, and compliance monitoring. The framework demonstrates good coverage across AI risk dimensions aligned with industry standards.

While the governance processes are well-defined, there are opportunities to further operationalize these processes into development workflows to address common compliance challenges earlier in the lifecycle.

Recommend focusing the next phase of governance maturity on developing reusable technical components that make compliance easier for development teams, particularly in the areas of fairness testing, explainability, and automated documentation.
            """,
            status="Draft"
        )
    ]
    
    # Insert sample policies
    for policy in policies:
        cursor.execute(
            'INSERT INTO policies (title, description, category, status, created_at, updated_at, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (policy.title, policy.description, policy.category, policy.status, now, now, policy.content)
        )
        policy_id = cursor.lastrowid
        
        # Log activity for policy creation
        cursor.execute(
            'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
            ('create_policy', f'Created policy: {policy.title}', now, 'System Initialization', policy_id, 'policy')
        )
    
    # Insert sample risk assessments
    for assessment in risk_assessments:
        cursor.execute(
            'INSERT INTO risk_assessments (title, model_name, risk_score, findings, recommendations, created_at, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (assessment.title, assessment.model_name, assessment.risk_score, assessment.findings, assessment.recommendations, now, assessment.status)
        )
        assessment_id = cursor.lastrowid
        
        # Log activity for risk assessment creation
        cursor.execute(
            'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
            ('create_risk_assessment', f'Created risk assessment: {assessment.title}', now, 'System Initialization', assessment_id, 'risk_assessment')
        )
    
    # Insert sample compliance monitors
    for monitor in compliance_monitors:
        cursor.execute(
            'INSERT INTO compliance_monitors (name, description, model_or_system, threshold_value, current_value, status, last_checked, alert_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level)
        )
        monitor_id = cursor.lastrowid
        
        # Log activity for compliance monitor creation
        cursor.execute(
            'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
            ('create_compliance_monitor', f'Created compliance monitor: {monitor.name}', now, 'System Initialization', monitor_id, 'compliance_monitor')
        )
    
    # Insert sample reports
    for report in reports:
        cursor.execute(
            'INSERT INTO reports (title, description, report_type, created_at, content, insights, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (report.title, report.description, report.report_type, now, report.content, report.insights, report.status)
        )
        report_id = cursor.lastrowid
        
        # Log activity for report creation
        cursor.execute(
            'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
            ('create_report', f'Created report: {report.title}', now, 'System Initialization', report_id, 'report')
        )
    
    # Log activity for sample data initialization
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('system_initialization', 'Initialized database with sample data based on NIST AI RMF', now, 'System', None, None)
    )
    
    conn.commit()
    print("Sample data preloaded successfully.")
    
if __name__ == "__main__":
    init_db()