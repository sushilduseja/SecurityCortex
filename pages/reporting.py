import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Reports | AI Governance Dashboard",
    page_icon="📊",
    layout="wide"
)

# API endpoints
API_URL = "http://localhost:8000"
REPORTING_API = f"{API_URL}/reporting"

# Page header with consistent styling
st.markdown("""
    <style>
    .report-header {
        padding: 1rem 0;
        border-bottom: 1px solid #e1e4e8;
        margin-bottom: 2rem;
    }
    .report-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        margin-bottom: 1rem;
    }
    .report-stats {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
    }
    .status-draft { background-color: #fff3cd; color: #856404; }
    .status-final { background-color: #d4edda; color: #155724; }
    .status-archived { background-color: #e2e3e5; color: #383d41; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="report-header">', unsafe_allow_html=True)
st.title("AI Governance Reports")
st.markdown("Generate, manage, and analyze comprehensive governance reports")
st.markdown('</div>', unsafe_allow_html=True)

# Report Type Overview with consistent naming
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="report-card">
            <h3>Comprehensive Reports</h3>
            <p>1 Report</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="report-card">
            <h3>Governance Reports</h3>
            <p>1 Report</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="report-card">
            <h3>Risk Assessment Reports</h3>
            <p>1 Report</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="report-card">
            <h3>Compliance Reports</h3>
            <p>1 Report</p>
        </div>
    """, unsafe_allow_html=True)

# Information section
st.markdown("""
    <div class="report-card">
        <h3>📋 AI Governance Reports</h3>
        <p>These reports provide comprehensive insights into your organization's AI governance practices. 
        Use them to track policy compliance, risk assessments, and overall governance status.</p>
    </div>
""", unsafe_allow_html=True)

# Load reports with error handling
@st.cache_data(ttl=60)
def load_reports():
    try:
        response = requests.get(f"{REPORTING_API}/reports")
        if response.status_code == 200:
            reports = response.json()["items"]
            # Validate report data
            for report in reports:
                if not report.get("title"):
                    report["title"] = "Untitled Report"
            return reports
        else:
            st.error(f"Error loading reports: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Create tabs
tab1, tab2 = st.tabs(["View Reports", "Generate Reports"])

with tab1:
    reports = load_reports()

    # Filters in a card
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox(
            "Report Type",
            ["All Types", "Comprehensive", "Governance", "Risk Assessment", "Compliance"]
        )
    with col2:
        filter_status = st.selectbox(
            "Status",
            ["All Statuses", "Draft", "Final", "Archived"]
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Reports table with improved styling
    if reports:
        for report in reports:
            st.markdown(f"""
                <div class="report-card">
                    <h3>{report.get('title', 'Untitled Report')}</h3>
                    <p><strong>Type:</strong> {report.get('report_type')} | 
                    <strong>Created:</strong> {report.get('created_at', '').split('T')[0]} | 
                    <span class="status-badge status-{report.get('status', 'draft').lower()}">{report.get('status', 'Draft')}</span></p>
                    <p>{report.get('description', 'No description available')}</p>
                    <div style="display: flex; gap: 0.5rem;">
                        <button>View</button>
                        <button>Download</button>
                        <button>Share</button>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No reports found matching the selected filters")

with tab2:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.header("Generate New Report")

    # Form with validation
    with st.form("report_form"):
        title = st.text_input("Report Title", max_chars=100)
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive", "Governance", "Risk Assessment", "Compliance"]
        )
        description = st.text_area("Description", max_chars=500)
        submitted = st.form_submit_button("Generate Report")

        if submitted:
            if not title:
                st.error("Report title is required")
            elif not description:
                st.error("Description is required")
            else:
                with st.spinner("Generating report..."):
                    try:
                        response = requests.post(
                            f"{REPORTING_API}/generate",
                            json={
                                "title": title,
                                "report_type": report_type,
                                "description": description
                            }
                        )
                        if response.status_code == 200:
                            st.success("Report generated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error generating report: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_report_types():
    try:
        response = requests.get(f"{REPORTING_API}/types")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading report types: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

#This part is removed because it is not used in the edited code and the intention is to improve UI and add validation.
#Keeping it would create conflict and unnecessary complexity.

# Show a refreshed view of reports if changes were made
if st.button("Refresh Data"):
    load_reports.clear()
    st.rerun()