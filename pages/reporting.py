import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Reporting | AI Governance Dashboard",
    page_icon="📋",
    layout="wide"
)

# API endpoints
API_URL = "http://localhost:8000"
REPORTING_API = f"{API_URL}/reporting"

# Page title
st.title("AI Governance Reporting")
st.markdown("Generate, view, and manage AI governance reports with automated insights")

# Function to load data from API
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_reports():
    try:
        response = requests.get(f"{REPORTING_API}/reports")
        if response.status_code == 200:
            return response.json()["items"]
        else:
            st.error(f"Error loading reports: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

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

# Load data
reports = load_reports()
report_types = load_report_types()

# Create tabs for different reporting functions
tab1, tab2 = st.tabs(["View Reports", "Generate Reports"])

with tab1:
    st.header("AI Governance Reports")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox(
            "Filter by Report Type",
            options=["All"] + [rt["type"] for rt in report_types],
            index=0
        )
    
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            options=["All", "Draft", "Final", "Archived"],
            index=0
        )
    
    # Apply filters
    filtered_reports = reports
    if filter_type != "All":
        filtered_reports = [r for r in filtered_reports if r.get("report_type") == filter_type]
    if filter_status != "All":
        filtered_reports = [r for r in filtered_reports if r.get("status") == filter_status]
    
    # Create a dataframe for display
    if filtered_reports:
        report_df = pd.DataFrame([
            {
                "ID": r.get("id"),
                "Title": r.get("title"),
                "Type": r.get("report_type"),
                "Status": r.get("status"),
                "Date": r.get("created_at").split("T")[0] if r.get("created_at") else "Unknown",
            }
            for r in filtered_reports
        ])
        
        # Sort by date (descending)
        report_df = report_df.sort_values(by="Date", ascending=False)
        
        # Display reports table
        st.dataframe(report_df, use_container_width=True, hide_index=True)
        
        # Report viewer
        st.subheader("Report Viewer")
        
        # Check if a report ID is in the session state
        if hasattr(st.session_state, 'report_id'):
            selected_report_id = st.session_state.report_id
            # Clear it after using
            del st.session_state.report_id
        else:
            selected_report_id = st.selectbox(
                "Select a report to view",
                options=[r.get("id") for r in filtered_reports],
                format_func=lambda x: next((f"{r.get('title')} ({r.get('report_type')})" for r in filtered_reports if r.get("id") == x), "Unknown")
            )
        
        # Display selected report
        selected_report = next((r for r in filtered_reports if r.get("id") == selected_report_id), None)
        if selected_report:
            report_date = selected_report.get("created_at", "").split("T")[0] if selected_report.get("created_at") else "Unknown"
            
            # Header with metadata
            st.markdown(f"## {selected_report.get('title')}")
            st.markdown(f"**Type:** {selected_report.get('report_type')} | **Status:** {selected_report.get('status')} | **Date:** {report_date}")
            st.markdown(f"**Description:** {selected_report.get('description')}")
            
            # Display report content with expandable insights
            st.markdown("---")
            
            # Tabs for Content and Insights
            content_tab, insights_tab = st.tabs(["Report Content", "AI Insights"])
            
            with content_tab:
                st.markdown(selected_report.get("content", "No content available"))
            
            with insights_tab:
                st.markdown("### AI-Generated Insights")
                st.markdown(selected_report.get("insights", "No insights available"))
            
            # Export options
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Export as PDF"):
                    st.info("PDF export functionality would be implemented here in a production system.")
            
            with col2:
                if st.button("Export as Markdown"):
                    # Create a download button with the markdown content
                    report_content = selected_report.get("content", "No content available")
                    
                    # Add metadata to the markdown
                    markdown_content = f"""# {selected_report.get('title')}

**Type:** {selected_report.get('report_type')}  
**Status:** {selected_report.get('status')}  
**Date:** {report_date}  
**Description:** {selected_report.get('description')}

---

{report_content}

---

## AI-Generated Insights

{selected_report.get('insights', 'No insights available')}
"""
                    
                    st.download_button(
                        label="Download Markdown",
                        data=markdown_content,
                        file_name=f"{selected_report.get('title').replace(' ', '_')}_{report_date}.md",
                        mime="text/markdown"
                    )
    else:
        st.info("No reports found matching the filter criteria")

with tab2:
    st.header("Generate Reports")
    st.markdown("Generate AI governance reports with automated insights from your data")
    
    # Show available report types with descriptions
    if report_types:
        selected_report_type = st.selectbox(
            "Select Report Type",
            options=[rt["type"] for rt in report_types],
            format_func=lambda x: f"{x} - {next((rt['description'] for rt in report_types if rt['type'] == x), '')}"
        )
        
        # Generate report button
        if st.button("Generate Report"):
            with st.spinner("Generating report... This may take a moment."):
                try:
                    response = requests.post(
                        f"{REPORTING_API}/generate",
                        params={"report_type": selected_report_type}
                    )
                    
                    if response.status_code == 200:
                        report = response.json()
                        st.success("Report generated successfully!")
                        
                        # Store the report ID in session state and redirect to view tab
                        st.session_state.report_id = report.get("id")
                        st.session_state.active_tab = "View Reports"
                        st.rerun()
                    else:
                        st.error(f"Failed to generate report: {response.text}")
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
        
        # Generate all reports button
        if st.button("Generate All Report Types"):
            with st.spinner("Generating all reports... This may take a moment."):
                try:
                    response = requests.post(f"{REPORTING_API}/generate-all")
                    
                    if response.status_code == 200:
                        generated_reports = response.json().get("generated_reports", [])
                        st.success(f"Successfully generated {len(generated_reports)} reports!")
                        
                        # Display generated reports
                        if generated_reports:
                            st.markdown("### Generated Reports")
                            for report in generated_reports:
                                st.markdown(f"- {report.get('title')} (Type: {report.get('report_type')})")
                            
                            # Clear cache and offer to view
                            load_reports.clear()
                            
                            if st.button("View Generated Reports"):
                                st.session_state.active_tab = "View Reports"
                                st.rerun()
                    else:
                        st.error(f"Failed to generate reports: {response.text}")
                except Exception as e:
                    st.error(f"Error generating reports: {str(e)}")
    else:
        st.warning("No report types available. Please check the API connection.")
    
    # Explanation of report types
    with st.expander("About Report Types"):
        st.markdown("""
        ### Report Types
        
        The AI Governance Dashboard offers several types of reports:
        
        1. **Governance Summary** - Overview of AI governance policies and their status
        2. **Risk Assessment Overview** - Summary of risk assessments across AI models
        3. **Compliance Status** - Current compliance monitoring status and alerts
        4. **Comprehensive Governance Report** - Complete overview of governance, risk, and compliance
        
        Each report includes AI-generated insights that highlight key findings and recommendations.
        """)

# Show a refreshed view of reports if changes were made
if st.button("Refresh Data"):
    load_reports.clear()
    st.rerun()
