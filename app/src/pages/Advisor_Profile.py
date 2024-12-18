import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Set page configuration
st.set_page_config(layout='wide', page_title="Advisor Dashboard", page_icon="🌟")

# Sidebar Navigation
SideBarLinks()

# API Base URL
API_BASE_URL = "http://api:4000/ad"

# Helper function to fetch data from API
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []
    
def fetch_advisor_details(advisor_id):
    try:
        response = requests.get(f"{API_BASE_URL}/{advisor_id}")
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return advisor details as a dictionary
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching advisor details: {e}")
        return {}

# Fetch advisor details (replace `25` with the actual ID if dynamic)
advisor_id = 25
advisor_details = fetch_advisor_details(advisor_id)

# Profile Section
st.markdown("---")
col1, col2 = st.columns([1, 6])

with col1:
    st.image("./assets/profile_photo.png", width=100)  # Replace with actual path to profile image

with col2:
    st.markdown("<h3 style='text-align: left;'>Advisor Profile</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        <p style='font-size: 14px;'>
        <strong>Name:</strong> {advisor_details.get("Preferred_Name", advisor_details.get("First_Name", "Not Available"))} {advisor_details.get("Last_Name", "Not Available")}<br>
        <strong>College:</strong> {advisor_details.get("College_Name", "Not Assigned")}
        </p>
    """, unsafe_allow_html=True)

# Fetch students data
st.markdown("### Students Overview")
students_data = fetch_data(f"students/{advisor_id}")
if students_data:
    students_df = pd.DataFrame(students_data)
    students_df.rename(
        columns={
            "First_Name": "First Name",
            "Last_Name": "Last Name",
            "GPA": "GPA",
            "Hired": "Hired",
            "Eligibility": "Eligibility",
            "Total_Applications": "Applications",
            "Latest_Application": "Latest Application Date",
            "Latest_Status": "Latest Status",
        },
        inplace=True,
    )
    st.dataframe(students_df)
else:
    st.warning("No students data available.")

# Fetch term summary
st.markdown("### Term Summary")
term_summary = fetch_data(f"term-summary/{advisor_id}")
if term_summary:
    placement_stats = term_summary.get("placement_statistics", [])
    industry_distribution = term_summary.get("industry_distribution", [])

    # Display placement statistics
    if placement_stats:
        st.subheader("Placement Statistics")
        placement_df = pd.DataFrame(placement_stats)
        st.dataframe(placement_df)

    # Display industry distribution
    if industry_distribution:
        st.subheader("Industry Distribution")
        industry_df = pd.DataFrame(industry_distribution)
        st.dataframe(industry_df)
else:
    st.warning("No term summary data available.")

# Fetch filled positions
st.markdown("### Filled Positions")
filled_positions = fetch_data(f"positions/filled/{advisor_id}")
if filled_positions:
    filled_positions_df = pd.DataFrame(filled_positions)
    filled_positions_df.rename(
        columns={
            "Name": "Position Name",
            "Title": "Job Title",
            "Company_Name": "Company",
            "Date_Start": "Start Date",
            "Date_End": "End Date",
            "Total_Applications": "Applications Received",
            "Accepted_Applications": "Accepted Offers",
        },
        inplace=True,
    )
    st.dataframe(filled_positions_df)
else:
    st.warning("No filled positions data available.")
