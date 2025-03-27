import streamlit as st
import os
import sqlite3
from database.db_init import init_db

# Initialize the database
init_db()

# Set page config
st.set_page_config(
    page_title="AI Governance Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app title and description
st.title("AI Governance Dashboard")
st.markdown("""
    ### AI-powered governance, risk assessment, and compliance management
    This dashboard provides automated tools for managing AI governance, 
    assessing risks, monitoring compliance, and generating reports.
""")

# Display overview metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Governance Policies", value="12", delta="2 new")
    
with col2:
    st.metric(label="Risk Score", value="76/100", delta="↑4")
    
with col3:
    st.metric(label="Compliance Rate", value="94%", delta="↑2%")
    
with col4:
    st.metric(label="Active Monitors", value="8", delta="1 new")

# Features section
st.subheader("Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
        #### Governance Management
        - Automated policy generation
        - Governance gap analysis
        - Policy compliance tracking
        
        #### Risk Assessment
        - AI risk classification
        - Documentation analysis
        - Risk mitigation recommendations
    """)

with feature_col2:
    st.markdown("""
        #### Compliance Monitoring
        - Real-time compliance tracking
        - Anomaly detection
        - Alert system
        
        #### Automated Reporting
        - Compliance report generation
        - Insights and recommendations
        - Exportable formats
    """)

# Quick actions
st.subheader("Quick Actions")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("Generate New Policy", use_container_width=True):
        st.session_state.navigate_to = "governance"
        st.rerun()

with action_col2:
    if st.button("Run Risk Assessment", use_container_width=True):
        st.session_state.navigate_to = "risk_assessment"
        st.rerun()

with action_col3:
    if st.button("View Compliance Status", use_container_width=True):
        st.session_state.navigate_to = "monitoring"
        st.rerun()

with action_col4:
    if st.button("Generate Report", use_container_width=True):
        st.session_state.navigate_to = "reporting"
        st.rerun()

# Recent activities
st.subheader("Recent Activities")

# Create a sample table of recent activities
activities = [
    {"activity": "New policy created: Data Privacy", "date": "Today, 10:30 AM", "user": "AI Governance Agent"},
    {"activity": "Risk assessment completed for Model XYZ", "date": "Yesterday, 4:15 PM", "user": "Risk Assessment Agent"},
    {"activity": "Compliance anomaly detected in Model ABC", "date": "Yesterday, 2:00 PM", "user": "Monitoring Agent"},
    {"activity": "Quarterly compliance report generated", "date": "2 days ago, 9:45 AM", "user": "Reporting Agent"},
]

st.table(activities)

# Footer
st.markdown("---")
st.markdown("#### AI Governance Dashboard MVP | Powered by AI Agents")
