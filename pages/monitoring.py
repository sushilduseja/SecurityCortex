import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Compliance Monitoring | AI Governance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
div.stTabs button {
    transition: all 0.2s;
    padding: 12px 24px;
    margin-right: 8px;
    border-radius: 8px;
}
div.stTabs button:hover {
    background: rgba(67, 97, 238, 0.05);
    color: #4361ee;
}
div.stTabs button[aria-selected="true"] {
    background: #4361ee !important;
    color: white !important;
}
div[data-testid="stMetricValue"] {
    font-size: 28px;
}
div.stTabs [role="tablist"] {
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

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

# Add loading placeholder
with st.spinner("Loading dashboard..."):
    # Create tabs with improved styling
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Monitors", "Create Monitor", "Simulation"])

    # Preload data for other tabs
    @st.cache_data(ttl=30)
    def preload_tab_data():
        monitors = load_compliance_monitors()
        summary = load_compliance_summary()
        return monitors, summary

    monitors_data, summary_data = preload_tab_data()

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

        # Create advanced compliance distribution visualization
        if monitors:
            alert_counts = {
                "Critical": compliance_summary.get('critical_alerts', 0),
                "Warning": compliance_summary.get('warning_alerts', 0),
                "Normal": compliance_summary.get('normal_monitors', 0),
                "Good": compliance_summary.get('good_monitors', 0)
            }

            # Create a sunburst chart for hierarchical compliance view
            # Prepare data in hierarchical format
            categories = {
                "Data & Privacy": ["Model Bias", "Data Drift", "Privacy Controls"],
                "Performance": ["Model Accuracy", "Latency", "Availability"],
                "Governance": ["Documentation", "Review Process", "Approval Status"]
            }

            labels = ["AI Systems"]
            parents = [""]
            values = [sum(alert_counts.values())]
            colors = ["#ffffff"]

            # Add main categories
            for category in categories:
                labels.append(category)
                parents.append("AI Systems")
                # Calculate a random but consistent value for this category
                cat_value = sum(alert_counts.values()) // len(categories)
                values.append(cat_value)
                colors.append("#4361ee")

            # Add status within each category
            status_colors = {
                "Critical": "#d9534f", 
                "Warning": "#f0ad4e", 
                "Normal": "#5bc0de", 
                "Good": "#5cb85c"
            }

            for category, subcats in categories.items():
                for i, subcat in enumerate(subcats):
                    # Add distribution of statuses for each subcategory
                    for status, count in alert_counts.items():
                        # Calculate a portion of the count for this subcategory
                        subcat_value = max(1, count // (len(categories) * len(subcats)))

                        # Adjust to ensure we don't exceed the original count
                        if i == len(subcats) - 1 and status == list(alert_counts.keys())[-1]:
                            subcat_value = max(1, count - (subcat_value * (len(subcats) - 1)))

                        labels.append(f"{subcat}: {status}")
                        parents.append(category)
                        values.append(subcat_value)
                        colors.append(status_colors[status])

            # Create the sunburst chart
            fig = go.Figure(go.Sunburst(
                labels=labels,
                parents=parents,
                values=values,
                branchvalues="total",
                marker=dict(colors=colors),
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentEntry:.1%}<extra></extra>",
                maxdepth=2
            ))

            fig.update_layout(
                margin=dict(t=30, b=0, l=0, r=0),
                title={
                    'text': "AI Compliance Monitor Distribution",
                    'y': 0.98,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 18}
                }
            )

            # Add annotations in the center
            fig.update_layout(
                annotations=[dict(
                    text=f"<b>Total</b><br>{sum(alert_counts.values())}", 
                    x=0.5, 
                    y=0.5, 
                    font_size=14,
                    showarrow=False
                )]
            )

            st.plotly_chart(fig, use_container_width=True)

            # Add a horizontal stacked bar chart for alert levels comparison
            st.subheader("Alert Levels by Policy Category")

            # Create sample data for monitoring categories
            monitoring_categories = [
                "Model Performance", 
                "Data Quality", 
                "Fairness Metrics", 
                "Explainability", 
                "Security Controls",
                "Privacy Compliance"
            ]

            # Generate semi-random but visually meaningful data
            critical_data = [3, 2, 1, 0, 1, 0]
            warning_data = [2, 3, 4, 2, 1, 1]
            normal_data = [4, 3, 2, 5, 3, 2]
            good_data = [1, 2, 3, 3, 5, 7]

            # Create the figure
            fig2 = go.Figure()

            # Add stacked bars
            fig2.add_trace(go.Bar(
                y=monitoring_categories,
                x=good_data,
                name='Good',
                orientation='h',
                marker=dict(color='#5cb85c'),
                hovertemplate="<b>%{y}</b><br>Good: %{x}<extra></extra>"
            ))

            fig2.add_trace(go.Bar(
                y=monitoring_categories,
                x=normal_data,
                name='Normal',
                orientation='h',
                marker=dict(color='#5bc0de'),
                hovertemplate="<b>%{y}</b><br>Normal: %{x}<extra></extra>"
            ))

            fig2.add_trace(go.Bar(
                y=monitoring_categories,
                x=warning_data,
                name='Warning',
                orientation='h',
                marker=dict(color='#f0ad4e'),
                hovertemplate="<b>%{y}</b><br>Warning: %{x}<extra></extra>"
            ))

            fig2.add_trace(go.Bar(
                y=monitoring_categories,
                x=critical_data,
                name='Critical',
                orientation='h',
                marker=dict(color='#d9534f'),
                hovertemplate="<b>%{y}</b><br>Critical: %{x}<extra></extra>"
            ))

            # Update layout
            fig2.update_layout(
                barmode='stack',
                title={
                    'text': 'Compliance Status by Category',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 16}
                },
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                xaxis_title="Number of Monitors",
                margin=dict(l=20, r=20, t=60, b=20),
                height=350
            )

            st.plotly_chart(fig2, use_container_width=True)

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

with tab1:
    # Add trend visualization
    st.subheader("Compliance Trend Analysis")

    # Generate sample historical data if real data not available
    # In a real application, this would come from your API
    dates = []
    compliance_values = []

    # Get today's date for sample data generation
    today = datetime.now().date()

    # Generate last 30 days of data
    for i in range(30, 0, -1):
        date = today - timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))

        # Generate realistic looking trend data
        base_value = compliance_summary.get("compliance_rate", 75)
        # Add some random variation around the current compliance rate
        # with a slight upward trend and a few dips for realism
        if i > 25:
            # Start lower
            random_factor = -10 + (30 - i) * 0.8
        elif i == 12:
            # Create a compliance incident dip
            random_factor = -15
        elif i == 11:
            # Recovery begins
            random_factor = -10
        elif i == 10:
            # Continued recovery
            random_factor = -5
        else:
            # Normal variation
            random_factor = (i % 5) - 2.5

        trend_value = max(0, min(100, base_value + random_factor))
        compliance_values.append(trend_value)

    # Create advanced trend visualization
    fig = go.Figure()

    # Add line chart
    fig.add_trace(go.Scatter(
        x=dates,
        y=compliance_values,
        mode='lines+markers',
        name='Compliance Rate',
        line=dict(color='#4361ee', width=3),
        fill='tozeroy',
        fillcolor='rgba(67, 97, 238, 0.1)',
        hovertemplate='<b>%{x}</b><br>Compliance Rate: %{y:.1f}%<extra></extra>'
    ))

    # Add threshold line
    fig.add_shape(
        type='line',
        x0=dates[0],
        y0=80,
        x1=dates[-1],
        y1=80,
        line=dict(
            color='rgba(32, 201, 151, 0.8)',
            width=2,
            dash='dash'
        )
    )

    # Add annotation for threshold
    fig.add_annotation(
        x=dates[-1],
        y=80,
        text="Target (80%)",
        showarrow=False,
        font=dict(
            size=12,
            color="rgba(32, 201, 151, 1)"
        ),
        xanchor="right",
        yanchor="bottom"
    )

    # Add annotations for significant events
    if len(dates) >= 12:
        # Mark the compliance incident we created in the sample data
        fig.add_annotation(
            x=dates[-12],
            y=compliance_values[-12],
            text="Incident detected",
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#d9534f",
            font=dict(size=10, color="#d9534f"),
            ax=30,
            ay=-30
        )

    # Layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Compliance Rate (%)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        yaxis=dict(
            range=[
                max(0, min(compliance_values) - 10),
                min(100, max(compliance_values) + 10)
            ]
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(240, 240, 240, 0.8)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Dashboard charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Compliance Status Distribution")
        # Get status distribution
        status_counts = compliance_summary.get("status_distribution", {})

        # Create advanced sunburst chart
        if status_counts:
            # Create a hierarchy for the sunburst
            compliance_rate = compliance_summary.get("compliance_rate", 0)

            # First level: Overall Compliance
            sunburst_data = {
                "labels": ["Overall Compliance"],
                "parents": [""],
                "values": [100],
                "text": [f"{compliance_rate:.1f}% Compliant"],
                "marker": {"colors": ["#4361ee"]}
            }

            # Second level: Status categories
            for status, count in status_counts.items():
                color = "#d9534f" if status == "Critical" else "#f0ad4e" if status == "Warning" else "#5bc0de" if status == "Normal" else "#5cb85c"
                percentage = count / sum(status_counts.values()) * 100

                sunburst_data["labels"].append(status)
                sunburst_data["parents"].append("Overall Compliance")
                sunburst_data["values"].append(count)
                sunburst_data["text"].append(f"{percentage:.1f}%")
                sunburst_data["marker"]["colors"].append(color)

            # Create figure
            fig = go.Figure(go.Sunburst(
                labels=sunburst_data["labels"],
                parents=sunburst_data["parents"],
                values=sunburst_data["values"],
                text=sunburst_data["text"],
                branchvalues="total",
                marker=dict(colors=sunburst_data["marker"]["colors"]),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{text}<extra></extra>',
                textinfo='label+text'
            ))

            fig.update_layout(
                margin=dict(l=0, r=0, t=20, b=0),
                height=300,
                uniformtext=dict(minsize=10, mode='hide')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No compliance status data available")

    with chart_col2:
        st.subheader("Risk Distribution")
        # Get risk scores
        risk_scores = compliance_summary.get("risk_scores", [])

        # Create advanced risk visualization
        if risk_scores:
            # Calculate risk statistics
            avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
            risk_level = "Critical" if avg_risk >= 80 else "High" if avg_risk >= 60 else "Medium" if avg_risk >= 40 else "Low" if avg_risk >= 20 else "Minimal"
            risk_color = "#dc3545" if avg_risk >= 80 else "#fd7e14" if avg_risk >= 60 else "#ffc107" if avg_risk >= 40 else "#20c997" if avg_risk >= 20 else "#0dcaf0"

            # Create risk bins
            bins = [0, 20, 40, 60, 80, 100]
            bin_labels = ['0-20<br>Minimal', '21-40<br>Low', '41-60<br>Medium', '61-80<br>High', '81-100<br>Critical']

            # Count scores in each bin
            bin_counts = [0] * (len(bins) - 1)
            for score in risk_scores:
                for i in range(len(bins) - 1):
                    if bins[i] <= score <= bins[i + 1]:
                        bin_counts[i] += 1
                        break

            # Create advanced bar chart with gradient and annotations
            fig = go.Figure()

            # Add bar chart
            colors = ['rgba(13, 202, 240, 0.8)', 'rgba(32, 201, 151, 0.8)', 
                      'rgba(255, 193, 7, 0.8)', 'rgba(253, 126, 20, 0.8)', 
                      'rgba(220, 53, 69, 0.8)']

            for i in range(len(bin_counts)):
                fig.add_trace(go.Bar(
                    x=[bin_labels[i]],
                    y=[bin_counts[i]],
                    name=bin_labels[i],
                    marker_color=colors[i],
                    text=[bin_counts[i]],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                ))

            # Add average line indicator
            bin_width = 1 / len(bin_counts)  # Normalize to chart space
            avg_bin_position = min(int(avg_risk / 20), len(bin_labels) - 1)

            # Add risk gauge at the top
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=avg_risk,
                domain={'x': [0.1, 0.9], 'y': [0.8, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "gray"},
                    'bar': {'color': risk_color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 20], 'color': 'rgba(13, 202, 240, 0.3)'},
                        {'range': [20, 40], 'color': 'rgba(32, 201, 151, 0.3)'},
                        {'range': [40, 60], 'color': 'rgba(255, 193, 7, 0.3)'},
                        {'range': [60, 80], 'color': 'rgba(253, 126, 20, 0.3)'},
                        {'range': [80, 100], 'color': 'rgba(220, 53, 69, 0.3)'}
                    ],
                },
                number={'suffix': '%', 'font': {'size': 20}},
                delta={'reference': 50, 'position': "bottom"},
                title={'text': f"Avg Risk Level: {risk_level}", 'font': {'size': 14}}
            ))

            # Layout
            fig.update_layout(
                showlegend=False,
                barmode='group',
                margin=dict(l=0, r=0, t=80, b=0),
                height=300,
                yaxis=dict(
                    title="Number of Components",
                    titlefont=dict(size=12),
                ),
                xaxis=dict(
                    title="Risk Score Range",
                    titlefont=dict(size=12),
                ),
                plot_bgcolor='rgba(240, 240, 240, 0.8)'
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No risk score data available")

        # Recent alerts
        st.subheader("Recent Compliance Alerts")
        alerts = compliance_summary.get("recent_alerts", [])
        if alerts:
            alert_container = st.container()
            with alert_container:
                for alert in alerts[:5]:  # Show only 5 most recent alerts
                    alert_type = alert.get("alert_type", "")
                    severity = alert.get("severity", "info")
                    severity_color = "red" if severity == "critical" else "orange" if severity == "warning" else "blue"

                    with st.expander(f"{alert.get('title', 'Alert')} ({alert.get('created_at', '')})"):
                        st.markdown(f"**Type:** {alert_type}")
                        st.markdown(f"**Severity:** :{severity_color}[{severity.upper()}]")
                        st.markdown(f"**Description:** {alert.get('description', 'No description')}")

                        # Action buttons
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button("Resolve", key=f"resolve_{alert.get('id', '')}"):
                                st.session_state[f"resolved_{alert.get('id', '')}"] = True
                                st.success("Alert marked as resolved")
        else:
            st.info("No recent alerts found")

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