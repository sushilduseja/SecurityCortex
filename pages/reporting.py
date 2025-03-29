import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Reports | AI Governance Dashboard",
    page_icon="📊",
    layout="wide"
)

# API endpoints
API_URL = "http://0.0.0.0:8000"
REPORTING_API = f"{API_URL}/reporting"

# Custom CSS for better styling
st.markdown("""
    <style>
    .report-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .report-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        transition: transform 0.2s;
    }
    .report-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .report-type {
        font-size: 0.875rem;
        color: #586069;
        margin-bottom: 0.5rem;
    }
    .report-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #24292e;
        margin-bottom: 1rem;
    }
    .report-meta {
        font-size: 0.875rem;
        color: #586069;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .status-draft { background: #fff3cd; color: #856404; }
    .status-final { background: #d4edda; color: #155724; }
    .generate-btn {
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Page header
st.title("Reports")
st.markdown("Generate and view AI governance reports")

# Report type cards (from original, adapted to new styling)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="report-card">
            <h3>Comprehensive Assessment</h3>
            <p>Complete governance overview</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="report-card">
            <h3>Governance Summary</h3>
            <p>Key governance metrics</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="report-card">
            <h3>Risk Assessment</h3>
            <p>Risk analysis overview</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="report-card">
            <h3>Compliance Status</h3>
            <p>Compliance metrics</p>
        </div>
    """, unsafe_allow_html=True)

# Generate Report Button (from edited code)
st.button("➕ Generate Report", type="primary", use_container_width=False)

# Reports section (from edited code)
st.subheader("Available Reports")

# Filters (combining original and edited code)
col1, col2 = st.columns(2)
with col1:
    report_type = st.selectbox(
        "Report Type",
        ["All Types", "Comprehensive", "Governance", "Risk", "Compliance"]
    )
with col2:
    status = st.selectbox(
        "Status",
        ["All", "Draft", "Final", "Archived"]
    )

# Load and display reports (combining original and edited code)
@st.cache_data(ttl=60)
def load_reports():
    try:
        response = requests.get(f"{REPORTING_API}/reports")
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error(f"Error loading reports: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

reports = load_reports()
for report in reports:
    with st.container():
        st.markdown(f"""
            <div class="report-card">
                <div class="report-type">{report.get('report_type', 'Unknown Type')}</div>
                <div class="report-title">{report.get('title', 'Untitled Report')}</div>
                <div class="report-meta">
                    Created: {report.get('created_at', '').split('T')[0]}
                    <span class="status-badge status-{report.get('status', 'draft').lower()}">
                        {report.get('status', 'Draft')}
                    </span>
                </div>
                <p>{report.get('description', 'No description available')}</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.button("📥 Download", key=f"download_{report.get('id')}")
        with col2:
            st.button("👁️ View", key=f"view_{report.get('id')}")
        with col3:
            st.button("🔄 Share", key=f"share_{report.get('id')}")


# Report generation form (from edited code, enhanced with original's validation)
with st.expander("Generate New Report"):
    with st.form("report_form"):
        title = st.text_input("Report Title", max_chars=100)
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive Assessment", "Governance Summary", "Risk Assessment", "Compliance Status"]
        )
        description = st.text_area("Description", max_chars=500)

        if st.form_submit_button("Generate"):
            if not title or not description:
                st.error("Please fill in all required fields")
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