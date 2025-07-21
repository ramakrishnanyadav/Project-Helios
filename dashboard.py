# dashboard.py - FINAL VERSION

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Helios: Executive Summary",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SNOWFLAKE DATA LOADING FUNCTION ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data_from_snowflake():
    """
    Connects to Snowflake using Streamlit's secrets management,
    queries all necessary tables, and returns them as pandas DataFrames.
    """
    # Establish the connection using the secrets file
    conn = st.connection("snowflake")

    # Define the SQL queries with fully-qualified table names for clarity
    query_influencers = "SELECT * FROM HEALTHKART_DB.RAW.INFLUENCERS;"
    query_posts = "SELECT * FROM HEALTHKART_DB.RAW.POSTS;"
    query_tracking = "SELECT * FROM HEALTHKART_DB.RAW.TRACKING_DATA;"
    query_payouts = "SELECT * FROM HEALTHKART_DB.RAW.PAYOUTS;"
    
    # Run queries and load into pandas DataFrames
    influencers = conn.query(query_influencers, ttl=600)
    posts = conn.query(query_posts, ttl=600)
    tracking = conn.query(query_tracking, ttl=600)
    payouts = conn.query(query_payouts, ttl=600)
    
    # Snowflake column names are often uppercase. Convert them to lowercase for consistency.
    influencers.columns = influencers.columns.str.lower()
    posts.columns = posts.columns.str.lower()
    tracking.columns = tracking.columns.str.lower()
    payouts.columns = payouts.columns.str.lower()

    # Convert date columns to the correct datetime format
    posts['date'] = pd.to_datetime(posts['date'])
    tracking['date'] = pd.to_datetime(tracking['date'])
    
    return influencers, posts, tracking, payouts

# --- LOAD DATA AND HANDLE ERRORS ---
# Use a try-except block to gracefully handle connection errors.
try:
    influencers_df, posts_df, tracking_df, payouts_df = load_data_from_snowflake()
except Exception as e:
    st.error(
        f"""
        **An error occurred while connecting to Snowflake.**
        
        This could be due to incorrect credentials in your secrets file or a permissions issue.
        Please check your secrets on Streamlit Cloud and the grants in your Snowflake account.
        
        *Error details: {e}*
        """
    )
    st.stop()


# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

all_platforms = influencers_df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect(
    "Select Platform(s)",
    options=all_platforms,
    default=all_platforms
)

all_personas = sorted(influencers_df['persona'].unique().tolist())
selected_personas = st.sidebar.multiselect(
    "Select Influencer Persona(s)",
    options=all_personas,
    default=all_personas
)

min_date = tracking_df['date'].min()
max_date = tracking_df['date'].max()
selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) != 2:
    st.warning("Please select a valid date range (start and end date).")
    st.stop()
start_date, end_date = selected_date_range

# --- FILTERING LOGIC ---
filtered_influencer_ids = influencers_df[
    (influencers_df['platform'].isin(selected_platforms)) &
    (influencers_df['persona'].isin(selected_personas))
]['influencer_id'].tolist()

payouts_filtered_df = payouts_df[payouts_df['influencer_id'].isin(filtered_influencer_ids)]

tracking_filtered_df = tracking_df[
    (tracking_df['date'] >= pd.to_datetime(start_date)) &
    (tracking_df['date'] <= pd.to_datetime(end_date))
]

influencer_tracking_filtered_df = tracking_filtered_df[
    tracking_filtered_df['influencer_id'].isin(filtered_influencer_ids)
]


# --- MAIN DASHBOARD CONTENT ---
st.title("☀️ Helios: HealthKart Influencer ROI Hub")
st.markdown("This is the executive summary of overall campaign performance. Use the sidebar to navigate to other pages for a deeper analysis.")

# --- CALCULATE CORE KPIS ---
total_spend = payouts_filtered_df['total_payout'].sum()
attributed_revenue = influencer_tracking_filtered_df['revenue'].sum()

if total_spend > 0:
    simple_roas = attributed_revenue / total_spend
else:
    simple_roas = 0
    
# --- INCREMENTAL ROAS CALCULATION ---
non_influencer_df = tracking_filtered_df[tracking_filtered_df['source'] != 'influencer_campaign']
total_days_in_range = (end_date - start_date).days + 1

if not non_influencer_df.empty and total_days_in_range > 0:
    baseline_daily_revenue = non_influencer_df['revenue'].sum() / total_days_in_range
else:
    baseline_daily_revenue = 0

expected_baseline_revenue = baseline_daily_revenue * total_days_in_range
incremental_revenue = attributed_revenue - expected_baseline_revenue

if total_spend > 0:
    incremental_roas = incremental_revenue / total_spend
else:
    incremental_roas = 0


# --- DISPLAY KPIS ---
st.markdown("### Overall Campaign Performance")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Campaign Spend", f"₹{total_spend:,.0f}")
col2.metric("Attributed Revenue", f"₹{attributed_revenue:,.0f}")
col3.metric("Simple ROAS", f"{simple_roas:.2f}x")
col4.metric(
    "Incremental ROAS", 
    f"{incremental_roas:.2f}x",
    help="This is the return on investment considering only the revenue *above* the organic baseline. A positive value indicates the campaign generated more revenue than would be expected without it."
)

st.markdown("---")

# --- VISUALIZATION ---
st.subheader("Attributed Revenue Over Time")
revenue_over_time = influencer_tracking_filtered_df.groupby('date')['revenue'].sum()
st.line_chart(revenue_over_time)

st.info("Use the pages in the sidebar to explore more detailed insights.", icon="👈")