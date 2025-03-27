import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Compliance Monitoring | AI Governance Dashboard",
    page_icon="📊",
    layout="wide"
)

# API endpoints
API_URL = "http://localhost:8000"
MONITORING_API = f"{API_URL}/monitoring"

# Page title
st.title("AI Compliance Monitoring")
st.markdown("Monitor compliance status of AI systems in real-time")

# Function to load data from API
@st.cache_data(ttl=30)  # Cache for 30 seconds - shorter for monitoring
def load_compliance_monitors():
    try:
        response = requests.get(f"{MONITORING_API}/monitors")
        if response.status_code == 200:
            return response.json()["items"]
        else:
            st.error(f"Error loading compliance monitors: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

@st.cache_data(ttl=30)  # Cache for 30 seconds
def load_compliance_summary():
    try:
        response = requests.get(f"{MONITORING_API}/summary")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading compliance summary: {response.text}")
            return {}
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return {}

# Load data
monitors = load_compliance_monitors()
compliance_summary = load_compliance_summary()

# Create tabs for different monitoring functions
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Monitors", "Create Monitor", "Simulation"])

with tab1:
    st.header("Compliance Dashboard")
    
    # Summary metrics at the top
    if compliance_summary:
        # Overall status with color coding
        status = compliance_summary.get("overall_status", "Unknown")
        status_color = "green" if status == "Good" else "blue" if status == "Normal" else "orange" if status == "Warning" else "red"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Compliance Rate", 
                value=f"{compliance_summary.get('compliance_rate', 0):.1f}%"
            )
            
        with col2:
            st.metric(
                label="Overall Status", 
                value=status,
                delta=None
            )
            st.markdown(f"<div style='color:{status_color};font-weight:bold;text-align:center;'>{status}</div>", unsafe_allow_html=True)
            
        with col3:
            st.metric(
                label="Critical Alerts", 
                value=compliance_summary.get('critical_alerts', 0),
                delta=None
            )
            
        with col4:
            st.metric(
                label="Warning Alerts", 
                value=compliance_summary.get('warning_alerts', 0),
                delta=None
            )
        
        # Compliance distribution chart
        st.subheader("Compliance Monitor Distribution")
        
        # Create a donut chart for compliance distribution
        if monitors:
            alert_counts = {
                "Critical": compliance_summary.get('critical_alerts', 0),
                "Warning": compliance_summary.get('warning_alerts', 0),
                "Normal": compliance_summary.get('normal_monitors', 0),
                "Good": compliance_summary.get('good_monitors', 0)
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(alert_counts.keys()),
                values=list(alert_counts.values()),
                hole=.4,
                marker_colors=['#d9534f', '#f0ad4e', '#5bc0de', '#5cb85c']
            )])
            
            fig.update_layout(
                title_text="Monitor Status Distribution",
                annotations=[dict(text=f"Total: {sum(alert_counts.values())}", x=0.5, y=0.5, font_size=15, showarrow=False)]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("Recommendations")
        for recommendation in compliance_summary.get('recommendations', []):
            st.info(recommendation)
        
        # Critical and Warning Alerts
        if compliance_summary.get('critical_alerts', 0) > 0 or compliance_summary.get('warning_alerts', 0) > 0:
            st.subheader("Active Alerts")
            
            # Filter monitors with alerts
            alert_monitors = [m for m in monitors if m.get('alert_level') in ['Critical', 'Warning']]
            
            if alert_monitors:
                for monitor in alert_monitors:
                    alert_color = "red" if monitor.get('alert_level') == 'Critical' else "orange"
                    with st.expander(f"{monitor.get('name')} - {monitor.get('alert_level')}", expanded=monitor.get('alert_level') == 'Critical'):
                        st.markdown(f"**Model/System:** {monitor.get('model_or_system')}")
                        st.markdown(f"**Alert Level:** <span style='color:{alert_color};font-weight:bold;'>{monitor.get('alert_level')}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Current Value:** {monitor.get('current_value'):.2f} (Threshold: {monitor.get('threshold_value'):.2f})")
                        st.markdown(f"**Last Checked:** {monitor.get('last_checked').split('T')[0] if monitor.get('last_checked') else 'Unknown'}")
                        st.markdown(f"**Description:** {monitor.get('description')}")
                        
                        # Action buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Acknowledge", key=f"ack_{monitor.get('id')}"):
                                st.info("Alert acknowledged. In a production system, this would log the acknowledgment.")
                        with col2:
                            if st.button("View Details", key=f"view_{monitor.get('id')}"):
                                st.session_state.selected_monitor_id = monitor.get('id')
                                st.rerun()
    else:
        st.warning("Compliance summary data not available")

with tab2:
    st.header("Compliance Monitors")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_model = st.text_input("Filter by Model/System")
    
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            options=["All", "Active", "Inactive", "Paused"],
            index=0
        )
    
    with col3:
        filter_alert = st.selectbox(
            "Filter by Alert Level",
            options=["All", "Critical", "Warning", "Normal", "Good"],
            index=0
        )
    
    # Apply filters
    filtered_monitors = monitors
    if filter_model:
        filtered_monitors = [m for m in filtered_monitors if filter_model.lower() in m.get("model_or_system", "").lower()]
    if filter_status != "All":
        filtered_monitors = [m for m in filtered_monitors if m.get("status") == filter_status]
    if filter_alert != "All":
        filtered_monitors = [m for m in filtered_monitors if m.get("alert_level") == filter_alert]
    
    # Create a dataframe for display
    if filtered_monitors:
        monitor_df = pd.DataFrame([
            {
                "ID": m.get("id"),
                "Name": m.get("name"),
                "Model/System": m.get("model_or_system"),
                "Current Value": f"{m.get('current_value', 0):.2f}",
                "Threshold": f"{m.get('threshold_value', 0):.2f}",
                "Alert Level": m.get("alert_level"),
                "Status": m.get("status"),
                "Last Checked": m.get("last_checked").split("T")[0] if m.get("last_checked") else "Unknown",
            }
            for m in filtered_monitors
        ])
        
        # Display monitors table
        st.dataframe(monitor_df, use_container_width=True, hide_index=True)
        
        # Monitor viewer/editor
        st.subheader("Monitor Details")
        
        # Use session state if already selected, otherwise use selectbox
        if hasattr(st.session_state, 'selected_monitor_id'):
            selected_monitor_id = st.session_state.selected_monitor_id
            # Clear the session state after using it
            del st.session_state.selected_monitor_id
        else:
            selected_monitor_id = st.selectbox(
                "Select a monitor to view/edit",
                options=[m.get("id") for m in filtered_monitors],
                format_func=lambda x: next((m.get("name") for m in filtered_monitors if m.get("id") == x), "Unknown")
            )
        
        # Display selected monitor
        selected_monitor = next((m for m in filtered_monitors if m.get("id") == selected_monitor_id), None)
        if selected_monitor:
            # Create columns for display and edit button
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {selected_monitor.get('name')}")
            
            with col2:
                if st.button("Edit Monitor", key="edit_monitor_button"):
                    st.session_state.edit_monitor = True
            
            # Display details or edit form
            if hasattr(st.session_state, 'edit_monitor') and st.session_state.edit_monitor:
                with st.form("edit_monitor_form"):
                    edit_name = st.text_input("Name", value=selected_monitor.get("name", ""))
                    edit_description = st.text_area("Description", value=selected_monitor.get("description", ""), height=100)
                    edit_model = st.text_input("Model/System", value=selected_monitor.get("model_or_system", ""))
                    edit_threshold = st.number_input("Threshold Value", value=float(selected_monitor.get("threshold_value", 0)), min_value=0.0, max_value=1.0, step=0.01)
                    edit_status = st.selectbox(
                        "Status",
                        options=["Active", "Inactive", "Paused"],
                        index=["Active", "Inactive", "Paused"].index(selected_monitor.get("status")) if selected_monitor.get("status") in ["Active", "Inactive", "Paused"] else 0
                    )
                    
                    save_button = st.form_submit_button("Save Changes")
                    
                    if save_button:
                        try:
                            response = requests.put(
                                f"{MONITORING_API}/monitors/{selected_monitor_id}",
                                json={
                                    "name": edit_name,
                                    "description": edit_description,
                                    "model_or_system": edit_model,
                                    "threshold_value": edit_threshold,
                                    "status": edit_status
                                }
                            )
                            
                            if response.status_code == 200:
                                st.success("Monitor updated successfully!")
                                # Clear cache and edit mode
                                load_compliance_monitors.clear()
                                load_compliance_summary.clear()
                                if hasattr(st.session_state, 'edit_monitor'):
                                    del st.session_state.edit_monitor
                                st.rerun()
                            else:
                                st.error(f"Failed to update monitor: {response.text}")
                        except Exception as e:
                            st.error(f"Error updating monitor: {str(e)}")
            else:
                # Display monitor details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Model/System:** {selected_monitor.get('model_or_system')}")
                    st.markdown(f"**Description:** {selected_monitor.get('description')}")
                    st.markdown(f"**Status:** {selected_monitor.get('status')}")
                
                with col2:
                    # Alert level with color coding
                    alert_level = selected_monitor.get('alert_level')
                    alert_color = "green" if alert_level == "Good" else "blue" if alert_level == "Normal" else "orange" if alert_level == "Warning" else "red"
                    st.markdown(f"**Alert Level:** <span style='color:{alert_color};font-weight:bold;'>{alert_level}</span>", unsafe_allow_html=True)
                    
                    st.markdown(f"**Last Checked:** {selected_monitor.get('last_checked').split('T')[0] if selected_monitor.get('last_checked') else 'Unknown'}")
                
                # Current value vs threshold visualization
                st.subheader("Current Value vs Threshold")
                
                # Create a gauge chart for the current value
                current_val = selected_monitor.get('current_value', 0)
                threshold_val = selected_monitor.get('threshold_value', 0)
                
                # Check if this is a metric where lower is better (threshold <= 0.5)
                is_lower_better = threshold_val <= 0.5
                
                if is_lower_better:
                    # For metrics where lower is better (e.g., drift)
                    gauge_color = "green" if current_val <= threshold_val else "red"
                    gauge_title = "Current Value (Lower is Better)"
                else:
                    # For metrics where higher is better (e.g., compliance %)
                    gauge_color = "green" if current_val >= threshold_val else "red"
                    gauge_title = "Current Value"
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=current_val,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': gauge_title},
                    gauge={
                        'axis': {'range': [0, 1]},
                        'bar': {'color': gauge_color},
                        'steps': [
                            {'range': [0, threshold_val], 'color': "lightgray" if not is_lower_better else "lightgreen"},
                            {'range': [threshold_val, 1], 'color': "lightgray" if is_lower_better else "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': threshold_val
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add buttons for updating the monitor value
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Update Monitor", key="update_monitor_value"):
                        try:
                            response = requests.put(
                                f"{MONITORING_API}/monitors/{selected_monitor_id}/value"
                            )
                            
                            if response.status_code == 200:
                                st.success("Monitor value updated successfully!")
                                # Clear cache
                                load_compliance_monitors.clear()
                                load_compliance_summary.clear()
                                st.rerun()
                            else:
                                st.error(f"Failed to update monitor value: {response.text}")
                        except Exception as e:
                            st.error(f"Error updating monitor value: {str(e)}")
    else:
        st.info("No monitors found matching the filter criteria")

with tab3:
    st.header("Create New Monitor")
    
    # Tabs for creating individual monitor or standard set
    create_tab1, create_tab2 = st.tabs(["Create Individual Monitor", "Create Standard Monitors"])
    
    with create_tab1:
        with st.form("create_monitor_form"):
            new_name = st.text_input("Monitor Name")
            new_description = st.text_area("Description", height=100)
            new_model = st.text_input("Model/System")
            new_threshold = st.number_input("Threshold Value", min_value=0.0, max_value=1.0, step=0.01, value=0.8)
            new_status = st.selectbox("Status", options=["Active", "Inactive", "Paused"], index=0)
            
            submit_button = st.form_submit_button("Create Monitor")
            
            if submit_button:
                if not new_name or not new_model:
                    st.error("Monitor name and model/system are required")
                else:
                    try:
                        response = requests.post(
                            f"{MONITORING_API}/monitors",
                            json={
                                "name": new_name,
                                "description": new_description,
                                "model_or_system": new_model,
                                "threshold_value": new_threshold,
                                "status": new_status
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success("Monitor created successfully!")
                            # Clear cache
                            load_compliance_monitors.clear()
                            load_compliance_summary.clear()
                            st.rerun()
                        else:
                            st.error(f"Failed to create monitor: {response.text}")
                    except Exception as e:
                        st.error(f"Error creating monitor: {str(e)}")
    
    with create_tab2:
        st.markdown("Create a standard set of compliance monitors for an AI model or system")
        
        with st.form("create_standard_monitors_form"):
            std_model_name = st.text_input("Model/System Name")
            std_model_type = st.selectbox(
                "Model Type",
                options=["all", "classification", "regression", "nlp", "computer_vision", "recommendation", "critical", "high-risk"]
            )
            
            st.markdown("This will create the following standard monitors:")
            st.markdown("- Data Privacy Compliance")
            st.markdown("- Fairness Metric")
            st.markdown("- Explainability Index")
            st.markdown("- Security Control Compliance")
            st.markdown("- Documentation Completeness")
            st.markdown("- Model Performance Stability")
            st.markdown("- Data Drift Detection")
            st.markdown("- Human Oversight Confirmation")
            
            submit_button = st.form_submit_button("Create Standard Monitors")
            
            if submit_button:
                if not std_model_name:
                    st.error("Model/System name is required")
                else:
                    with st.spinner("Creating standard monitors... This may take a moment."):
                        try:
                            response = requests.post(
                                f"{MONITORING_API}/standard-monitors",
                                json={
                                    "model_name": std_model_name,
                                    "model_type": std_model_type
                                }
                            )
                            
                            if response.status_code == 200:
                                created_monitors = response.json().get("created_monitors", [])
                                st.success(f"Successfully created {len(created_monitors)} standard monitors!")
                                
                                # Show created monitors
                                if created_monitors:
                                    st.markdown("### Created Monitors")
                                    for monitor in created_monitors:
                                        st.markdown(f"- {monitor.get('name')}")
                                
                                # Clear cache
                                load_compliance_monitors.clear()
                                load_compliance_summary.clear()
                            else:
                                st.error(f"Failed to create standard monitors: {response.text}")
                        except Exception as e:
                            st.error(f"Error creating standard monitors: {str(e)}")

with tab4:
    st.header("Compliance Monitoring Simulation")
    st.markdown("Simulate changes in compliance metrics to see how the system responds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Run Monitoring Cycle", key="run_monitoring_cycle"):
            with st.spinner("Running monitoring cycle... This may take a moment."):
                try:
                    response = requests.post(f"{MONITORING_API}/simulate-cycle")
                    
                    if response.status_code == 200:
                        updated_monitors = response.json().get("updated_monitors", [])
                        st.success(f"Successfully updated {len(updated_monitors)} monitors!")
                        
                        # Show updated monitors
                        if updated_monitors:
                            # Create a dataframe for the updates
                            update_df = pd.DataFrame([
                                {
                                    "Name": m.get("name"),
                                    "Current Value": f"{m.get('current_value', 0):.2f}",
                                    "Alert Level": m.get("alert_level"),
                                    "Status": m.get("status")
                                }
                                for m in updated_monitors
                            ])
                            
                            st.dataframe(update_df, use_container_width=True, hide_index=True)
                        
                        # Clear cache
                        load_compliance_monitors.clear()
                        load_compliance_summary.clear()
                        
                        # Update the summary display
                        st.markdown("### Updated Compliance Summary")
                        new_summary = load_compliance_summary()
                        
                        if new_summary:
                            st.metric(
                                label="Compliance Rate", 
                                value=f"{new_summary.get('compliance_rate', 0):.1f}%"
                            )
                            
                            st.metric(
                                label="Critical Alerts", 
                                value=new_summary.get('critical_alerts', 0)
                            )
                            
                            if new_summary.get('recommendations', []):
                                st.markdown("### Updated Recommendations")
                                for recommendation in new_summary.get('recommendations', []):
                                    st.info(recommendation)
                    else:
                        st.error(f"Failed to run monitoring cycle: {response.text}")
                except Exception as e:
                    st.error(f"Error running monitoring cycle: {str(e)}")
    
    with col2:
        st.markdown("### Simulation Information")
        st.markdown("""
        The monitoring simulation:
        
        - Updates the current values of all active monitors
        - Recalculates alert levels based on the new values
        - Updates the overall compliance summary
        - Generates new recommendations if needed
        
        This simulates how the system would respond to real-time changes in AI system metrics.
        """)

# Show a refreshed view of monitors if changes were made
if st.button("Refresh Data"):
    load_compliance_monitors.clear()
    load_compliance_summary.clear()
    st.rerun()
