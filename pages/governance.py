import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# Set page config
st.set_page_config(page_title="Governance | AI Governance Dashboard",
                   page_icon="🛡️",
                   layout="wide")

# API endpoints
API_URL = "http://localhost:8000"
GOVERNANCE_API = f"{API_URL}/governance"

# Page title
st.title("AI Governance Management")
st.markdown("Manage AI governance policies and regulations with AI assistance")


# Function to load data from API
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_policies():
    try:
        response = requests.get(f"{GOVERNANCE_API}/policies")
        if response.status_code == 200:
            return response.json()["items"]
        else:
            st.error(f"Error loading policies: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_categories():
    try:
        response = requests.get(f"{GOVERNANCE_API}/categories")
        if response.status_code == 200:
            return response.json()["categories"]
        else:
            st.error(f"Error loading categories: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []


@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_recommendations():
    try:
        response = requests.get(f"{GOVERNANCE_API}/recommendations")
        if response.status_code == 200:
            return response.json()["recommendations"]
        else:
            st.error(f"Error loading recommendations: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []


# Load data
policies = load_policies()
categories = load_categories()
recommendations = load_recommendations()

# Create tabs for different governance functions
tab1, tab2, tab3, tab4 = st.tabs(
    ["Policies", "Create Policy", "Generate Policy", "Recommendations"])

with tab1:
    st.header("Governance Policies")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category",
                                       options=["All"] + categories,
                                       index=0)

    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            options=["All", "Draft", "Active", "Under Review", "Deprecated"],
            index=0)

    # Apply filters
    filtered_policies = policies
    if filter_category != "All":
        filtered_policies = [
            p for p in filtered_policies
            if p.get("category") == filter_category
        ]
    if filter_status != "All":
        filtered_policies = [
            p for p in filtered_policies if p.get("status") == filter_status
        ]

    # Create a dataframe for display
    if filtered_policies:
        policy_df = pd.DataFrame([{
            "ID":
            p.get("id"),
            "Title":
            p.get("title"),
            "Category":
            p.get("category"),
            "Status":
            p.get("status"),
            "Created":
            p.get("created_at").split("T")[0]
            if p.get("created_at") else "Unknown",
        } for p in filtered_policies])

        # Display policies table
        st.dataframe(policy_df, use_container_width=True, hide_index=True)

        # Policy viewer
        st.subheader("Policy Viewer")
        selected_policy_id = st.selectbox(
            "Select a policy to view",
            options=[p.get("id") for p in filtered_policies],
            format_func=lambda x: next((p.get("title")
                                        for p in filtered_policies
                                        if p.get("id") == x), "Unknown"))

        # Display selected policy
        selected_policy = next(
            (p
             for p in filtered_policies if p.get("id") == selected_policy_id),
            None)
        if selected_policy:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown(f"**Category:** {selected_policy.get('category')}")
            with col2:
                st.markdown(f"**Status:** {selected_policy.get('status')}")
            with col3:
                st.markdown(
                    f"**Last Updated:** {selected_policy.get('updated_at').split('T')[0] if selected_policy.get('updated_at') else 'Unknown'}"
                )

            st.markdown("### Description")
            st.markdown(
                selected_policy.get("description", "No description available"))

            st.markdown("### Policy Content")
            st.markdown(selected_policy.get("content", "No content available"))

            # Edit button
            edit_col1, edit_col2 = st.columns([1, 6])
            with edit_col1:
                if st.button("Edit Policy", key="edit_policy"):
                    st.session_state.edit_policy_id = selected_policy_id
                    st.session_state.edit_policy_data = selected_policy
                    st.rerun()

            # If in edit mode, show edit form
            if hasattr(
                    st.session_state, "edit_policy_id"
            ) and st.session_state.edit_policy_id == selected_policy_id:
                st.subheader("Edit Policy")
                edit_title = st.text_input("Title",
                                           value=selected_policy.get(
                                               "title", ""))
                edit_category = st.selectbox(
                    "Category",
                    options=categories,
                    index=categories.index(selected_policy.get("category"))
                    if selected_policy.get("category") in categories else 0)
                edit_status = st.selectbox(
                    "Status",
                    options=["Draft", "Active", "Under Review", "Deprecated"],
                    index=["Draft", "Active", "Under Review", "Deprecated"
                           ].index(selected_policy.get("status"))
                    if selected_policy.get("status") in [
                        "Draft", "Active", "Under Review", "Deprecated"
                    ] else 0)
                edit_description = st.text_area("Description",
                                                value=selected_policy.get(
                                                    "description", ""),
                                                height=100)
                edit_content = st.text_area("Content",
                                            value=selected_policy.get(
                                                "content", ""),
                                            height=300)

                save_col1, save_col2 = st.columns([1, 6])
                with save_col1:
                    if st.button("Save Changes"):
                        try:
                            response = requests.put(
                                f"{GOVERNANCE_API}/policies/{selected_policy_id}",
                                json={
                                    "title": edit_title,
                                    "category": edit_category,
                                    "status": edit_status,
                                    "description": edit_description,
                                    "content": edit_content
                                })

                            if response.status_code == 200:
                                st.success("Policy updated successfully!")
                                # Clear cache to reload data
                                load_policies.clear()
                                if hasattr(st.session_state, "edit_policy_id"):
                                    del st.session_state.edit_policy_id
                                if hasattr(st.session_state,
                                           "edit_policy_data"):
                                    del st.session_state.edit_policy_data
                                st.rerun()
                            else:
                                st.error(
                                    f"Failed to update policy: {response.text}"
                                )
                        except Exception as e:
                            st.error(f"Error updating policy: {str(e)}")
    else:
        st.info("No policies found matching the filter criteria")

with tab2:
    st.header("Create New Policy")

    # Policy creation form
    with st.form("create_policy_form"):
        new_title = st.text_input("Policy Title")
        new_category = st.selectbox("Category", options=categories)
        new_description = st.text_area("Description", height=100)
        new_content = st.text_area("Policy Content", height=300)
        new_status = st.selectbox("Status",
                                  options=["Draft", "Active", "Under Review"])

        submit_button = st.form_submit_button("Create Policy")

        if submit_button:
            if not new_title:
                st.error("Policy title is required")
            else:
                try:
                    response = requests.post(f"{GOVERNANCE_API}/policies",
                                             json={
                                                 "title": new_title,
                                                 "category": new_category,
                                                 "description":
                                                 new_description,
                                                 "content": new_content,
                                                 "status": new_status
                                             })

                    if response.status_code == 200:
                        st.success("Policy created successfully!")
                        # Clear cache to reload data
                        load_policies.clear()
                        # Clear form
                        st.session_state.policy_title = ""
                        st.session_state.policy_description = ""
                        st.session_state.policy_content = ""
                        st.rerun()
                    else:
                        st.error(f"Failed to create policy: {response.text}")
                except Exception as e:
                    st.error(f"Error creating policy: {str(e)}")

with tab3:
    st.header("Generate Policy with AI")
    st.markdown(
        "Let the AI agent generate a governance policy for you based on a selected category."
    )

    generate_category = st.selectbox("Select Policy Category",
                                     options=categories)

    if st.button("Generate Policy", key="generate_policy_button"):
        with st.spinner("Generating policy... This may take a moment."):
            try:
                response = requests.post(
                    f"{GOVERNANCE_API}/generate",
                    params={"category": generate_category})

                if response.status_code == 200:
                    policy = response.json()
                    st.success("Policy generated successfully!")

                    # Display generated policy
                    st.subheader(policy.get("title", "Generated Policy"))

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Category:** {policy.get('category')}")
                    with col2:
                        st.markdown(f"**Status:** {policy.get('status')}")

                    st.markdown("### Description")
                    st.markdown(
                        policy.get("description", "No description available"))

                    st.markdown("### Policy Content")
                    st.markdown(policy.get("content", "No content available"))

                    # Option to edit
                    if st.button("Edit Generated Policy"):
                        st.session_state.edit_policy_id = policy.get("id")
                        st.session_state.edit_policy_data = policy
                        st.rerun()

                    # Clear cache to reload data
                    load_policies.clear()
                else:
                    st.error(f"Failed to generate policy: {response.text}")
            except Exception as e:
                st.error(f"Error generating policy: {str(e)}")

with tab4:
    st.header("Policy Recommendations")
    st.markdown(
        "The AI governance agent analyzes your existing policies and identifies gaps and improvement opportunities."
    )

    # Display recommendations
    if recommendations:
        for i, rec in enumerate(recommendations):
            with st.expander(
                    f"{rec.get('title', 'Policy Recommendation')} ({rec.get('priority', 'Medium')})"
            ):
                st.markdown(f"**Category:** {rec.get('category')}")
                st.markdown(f"**Description:** {rec.get('description')}")
                st.markdown(f"**Priority:** {rec.get('priority')}")

                # Button to generate this policy
                if st.button("Generate This Policy", key=f"generate_rec_{i}"):
                    with st.spinner("Generating policy..."):
                        try:
                            response = requests.post(
                                f"{GOVERNANCE_API}/generate",
                                params={"category": rec.get("category")})

                            if response.status_code == 200:
                                st.success("Policy generated successfully!")
                                # Clear cache to reload data
                                load_policies.clear()
                                load_recommendations.clear()
                                st.rerun()
                            else:
                                st.error(
                                    f"Failed to generate policy: {response.text}"
                                )
                        except Exception as e:
                            st.error(f"Error generating policy: {str(e)}")
    else:
        st.info(
            "No policy recommendations found. This may indicate that your governance framework is already comprehensive!"
        )

    # Button to refresh recommendations
    if st.button("Refresh Recommendations"):
        load_recommendations.clear()
        st.rerun()

# Show a refreshed view of policies if changes were made
if st.button("Refresh Data"):
    load_policies.clear()
    load_recommendations.clear()
    st.rerun()
