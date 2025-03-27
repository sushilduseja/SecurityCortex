import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Risk Assessment | AI Governance Dashboard",
    page_icon="🔍",
    layout="wide"
)

# API endpoints
API_URL = "http://localhost:8000"
RISK_API = f"{API_URL}/risk"

# Page title
st.title("AI Risk Assessment")
st.markdown("Assess and manage risks in AI systems with NLP-powered analysis")

# Function to load data from API
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_risk_assessments():
    try:
        response = requests.get(f"{RISK_API}/assessments")
        if response.status_code == 200:
            return response.json()["items"]
        else:
            st.error(f"Error loading risk assessments: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_risk_categories():
    try:
        response = requests.get(f"{RISK_API}/categories")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading risk categories: {response.text}")
            return {"categories": [], "descriptions": {}}
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return {"categories": [], "descriptions": {}}

# Load data
assessments = load_risk_assessments()
risk_categories_data = load_risk_categories()
risk_categories = risk_categories_data.get("categories", [])
category_descriptions = risk_categories_data.get("descriptions", {})

# Create tabs for different risk assessment functions
tab1, tab2, tab3, tab4 = st.tabs(["Assessments", "Assess from Documentation", "Assess from Metadata", "High-Risk Models"])

with tab1:
    st.header("Risk Assessments")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_model = st.text_input("Filter by Model Name")
    
    with col2:
        min_risk = st.slider("Minimum Risk Score", 0, 100, 0)
    
    with col3:
        max_risk = st.slider("Maximum Risk Score", 0, 100, 100)
    
    # Create a dataframe for display
    if assessments:
        # Apply filters
        filtered_assessments = assessments
        if filter_model:
            filtered_assessments = [a for a in filtered_assessments if filter_model.lower() in a.get("model_name", "").lower()]
        filtered_assessments = [a for a in filtered_assessments if a.get("risk_score", 0) >= min_risk and a.get("risk_score", 0) <= max_risk]
        
        if filtered_assessments:
            assessment_df = pd.DataFrame([
                {
                    "ID": a.get("id"),
                    "Title": a.get("title"),
                    "Model": a.get("model_name"),
                    "Risk Score": f"{a.get('risk_score', 0):.1f}",
                    "Status": a.get("status"),
                    "Date": a.get("created_at").split("T")[0] if a.get("created_at") else "Unknown",
                }
                for a in filtered_assessments
            ])
            
            # Display assessments table
            st.dataframe(assessment_df, use_container_width=True, hide_index=True)
            
            # Risk assessment viewer
            st.subheader("Risk Assessment Viewer")
            selected_assessment_id = st.selectbox(
                "Select an assessment to view",
                options=[a.get("id") for a in filtered_assessments],
                format_func=lambda x: next((f"{a.get('model_name')} - {a.get('title')}" for a in filtered_assessments if a.get("id") == x), "Unknown")
            )
            
            # Display selected assessment
            selected_assessment = next((a for a in filtered_assessments if a.get("id") == selected_assessment_id), None)
            if selected_assessment:
                # Risk score display with color coding
                risk_score = selected_assessment.get("risk_score", 0)
                risk_color = "red" if risk_score >= 75 else "orange" if risk_score >= 50 else "green"
                
                st.markdown(f"### {selected_assessment.get('title')}")
                st.markdown(f"**Model:** {selected_assessment.get('model_name')}")
                st.markdown(f"**Status:** {selected_assessment.get('status')}")
                st.markdown(f"**Date:** {selected_assessment.get('created_at').split('T')[0] if selected_assessment.get('created_at') else 'Unknown'}")
                
                # Risk score as a progress bar
                st.markdown(f"**Risk Score:** <span style='color:{risk_color};font-weight:bold;'>{risk_score:.1f}/100</span>", unsafe_allow_html=True)
                st.progress(risk_score/100)
                
                # Findings and recommendations in expanders
                with st.expander("Findings", expanded=True):
                    findings = selected_assessment.get("findings", "No findings available")
                    st.markdown(findings)
                
                with st.expander("Recommendations", expanded=True):
                    recommendations = selected_assessment.get("recommendations", "No recommendations available")
                    st.markdown(recommendations)
        else:
            st.info("No assessments found matching the filter criteria")
    else:
        st.info("No risk assessments found. Create one using the tabs above.")

with tab2:
    st.header("Assess from Documentation")
    st.markdown("Upload or paste AI model documentation for risk assessment")
    
    with st.form("assess_documentation_form"):
        doc_title = st.text_input("Assessment Title")
        doc_model_name = st.text_input("Model Name")
        doc_content = st.text_area("Model Documentation", height=300, help="Paste the model documentation, whitepaper, or description here")
        
        submit_button = st.form_submit_button("Run Assessment")
        
        if submit_button:
            if not doc_title or not doc_model_name or not doc_content:
                st.error("All fields are required")
            else:
                with st.spinner("Analyzing documentation... This may take a moment."):
                    try:
                        response = requests.post(
                            f"{RISK_API}/assess-from-documentation",
                            json={
                                "title": doc_title,
                                "model_name": doc_model_name,
                                "documentation": doc_content
                            }
                        )
                        
                        if response.status_code == 200:
                            assessment = response.json()
                            st.success("Risk assessment completed successfully!")
                            
                            # Display risk assessment results
                            risk_score = assessment.get("risk_score", 0)
                            risk_color = "red" if risk_score >= 75 else "orange" if risk_score >= 50 else "green"
                            
                            st.markdown("### Assessment Results")
                            st.markdown(f"**Risk Score:** <span style='color:{risk_color};font-weight:bold;'>{risk_score:.1f}/100</span>", unsafe_allow_html=True)
                            st.progress(risk_score/100)
                            
                            with st.expander("Findings", expanded=True):
                                findings = assessment.get("findings", "No findings available")
                                st.markdown(findings)
                            
                            with st.expander("Recommendations", expanded=True):
                                recommendations = assessment.get("recommendations", "No recommendations available")
                                st.markdown(recommendations)
                            
                            # Clear cache to reload data
                            load_risk_assessments.clear()
                        else:
                            st.error(f"Failed to complete risk assessment: {response.text}")
                    except Exception as e:
                        st.error(f"Error running risk assessment: {str(e)}")

with tab3:
    st.header("Assess from Metadata")
    st.markdown("Provide structured metadata for your AI model for risk assessment")
    
    with st.form("assess_metadata_form"):
        meta_model_name = st.text_input("Model Name")
        meta_model_type = st.selectbox("Model Type", options=["classification", "regression", "nlp", "computer_vision", "recommendation", "reinforcement_learning", "other"])
        meta_description = st.text_area("Model Description", height=100)
        meta_purpose = st.text_input("Purpose")
        meta_training_data = st.text_area("Training Data Description", height=100)
        meta_limitations = st.text_area("Known Limitations", height=100)
        meta_ethical = st.text_area("Ethical Considerations", height=100)
        
        # Additional metadata
        st.subheader("Additional Metadata (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            meta_key1 = st.text_input("Key 1")
            meta_key2 = st.text_input("Key 2")
        with col2:
            meta_value1 = st.text_input("Value 1")
            meta_value2 = st.text_input("Value 2")
        
        submit_button = st.form_submit_button("Run Assessment")
        
        if submit_button:
            if not meta_model_name or not meta_model_type or not meta_description:
                st.error("Model name, type, and description are required")
            else:
                with st.spinner("Analyzing metadata... This may take a moment."):
                    try:
                        # Build additional metadata dict
                        additional_metadata = {}
                        if meta_key1 and meta_value1:
                            additional_metadata[meta_key1] = meta_value1
                        if meta_key2 and meta_value2:
                            additional_metadata[meta_key2] = meta_value2
                        
                        response = requests.post(
                            f"{RISK_API}/assess-from-metadata",
                            json={
                                "model_name": meta_model_name,
                                "model_type": meta_model_type,
                                "description": meta_description,
                                "purpose": meta_purpose,
                                "training_data": meta_training_data,
                                "limitations": meta_limitations,
                                "ethical_considerations": meta_ethical,
                                "additional_metadata": additional_metadata
                            }
                        )
                        
                        if response.status_code == 200:
                            assessment = response.json()
                            st.success("Risk assessment completed successfully!")
                            
                            # Display risk assessment results
                            risk_score = assessment.get("risk_score", 0)
                            risk_color = "red" if risk_score >= 75 else "orange" if risk_score >= 50 else "green"
                            
                            st.markdown("### Assessment Results")
                            st.markdown(f"**Risk Score:** <span style='color:{risk_color};font-weight:bold;'>{risk_score:.1f}/100</span>", unsafe_allow_html=True)
                            st.progress(risk_score/100)
                            
                            with st.expander("Findings", expanded=True):
                                findings = assessment.get("findings", "No findings available")
                                st.markdown(findings)
                            
                            with st.expander("Recommendations", expanded=True):
                                recommendations = assessment.get("recommendations", "No recommendations available")
                                st.markdown(recommendations)
                            
                            # Clear cache to reload data
                            load_risk_assessments.clear()
                        else:
                            st.error(f"Failed to complete risk assessment: {response.text}")
                    except Exception as e:
                        st.error(f"Error running risk assessment: {str(e)}")

with tab4:
    st.header("High-Risk Models")
    st.markdown("View and manage high-risk AI models requiring immediate attention")
    
    # Set threshold for high-risk classification
    threshold = st.slider("High-Risk Threshold", 50, 95, 75)
    
    if st.button("Load High-Risk Models"):
        with st.spinner("Loading high-risk models..."):
            try:
                response = requests.get(f"{RISK_API}/high-risk", params={"threshold": threshold})
                
                if response.status_code == 200:
                    high_risk_models = response.json()["items"]
                    
                    if high_risk_models:
                        st.warning(f"Found {len(high_risk_models)} high-risk models with risk score >= {threshold}")
                        
                        # Create a dataframe for display
                        high_risk_df = pd.DataFrame([
                            {
                                "ID": a.get("id"),
                                "Model": a.get("model_name"),
                                "Risk Score": f"{a.get('risk_score', 0):.1f}",
                                "Title": a.get("title"),
                                "Date": a.get("created_at").split("T")[0] if a.get("created_at") else "Unknown",
                            }
                            for a in high_risk_models
                        ]).sort_values(by="Risk Score", ascending=False)
                        
                        st.dataframe(high_risk_df, use_container_width=True, hide_index=True)
                        
                        # Select model to view details
                        if len(high_risk_models) > 0:
                            selected_id = st.selectbox(
                                "Select a model to view details",
                                options=[a.get("id") for a in high_risk_models],
                                format_func=lambda x: next((f"{a.get('model_name')} (Risk: {a.get('risk_score', 0):.1f})" for a in high_risk_models if a.get("id") == x), "Unknown")
                            )
                            
                            selected_model = next((a for a in high_risk_models if a.get("id") == selected_id), None)
                            if selected_model:
                                st.markdown(f"### {selected_model.get('title')}")
                                st.markdown(f"**Model:** {selected_model.get('model_name')}")
                                
                                # Risk score as a progress bar
                                risk_score = selected_model.get("risk_score", 0)
                                st.markdown(f"**Risk Score:** <span style='color:red;font-weight:bold;'>{risk_score:.1f}/100</span>", unsafe_allow_html=True)
                                st.progress(risk_score/100)
                                
                                # Key findings and recommendations
                                with st.expander("Key Findings", expanded=True):
                                    findings = selected_model.get("findings", "No findings available")
                                    st.markdown(findings)
                                
                                with st.expander("Recommendations", expanded=True):
                                    recommendations = selected_model.get("recommendations", "No recommendations available")
                                    st.markdown(recommendations)
                    else:
                        st.success(f"No models found with risk score >= {threshold}")
                else:
                    st.error(f"Failed to load high-risk models: {response.text}")
            except Exception as e:
                st.error(f"Error loading high-risk models: {str(e)}")

# Display risk categories information
with st.expander("Risk Categories Information"):
    st.markdown("### Risk Categories")
    st.markdown("The AI Risk Assessment uses the following risk categories:")
    
    for category in risk_categories:
        st.markdown(f"**{category}**: {category_descriptions.get(category, 'No description available')}")

# Show a refreshed view of assessments if changes were made
if st.button("Refresh Data"):
    load_risk_assessments.clear()
    st.rerun()
