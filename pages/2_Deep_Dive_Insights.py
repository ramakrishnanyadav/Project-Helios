# pages/2_Deep_Dive_Insights.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration. This should be the first Streamlit command.
st.set_page_config(page_title="Deep Dive Insights", page_icon="💡", layout="wide")

# --- STEP 1: LOAD DATA ---
# This function is cached so the data is only loaded once from the CSV files.
@st.cache_data
def load_data():
    data_path = 'data/'
    influencers = pd.read_csv(data_path + 'influencers.csv')
    tracking = pd.read_csv(data_path + 'tracking_data.csv')
    payouts = pd.read_csv(data_path + 'payouts.csv')
    tracking['date'] = pd.to_datetime(tracking['date'])
    return influencers, tracking, payouts

influencers_df, tracking_df, payouts_df = load_data()

# --- STEP 2: SIDEBAR FILTERS ---
# These filters are displayed in the sidebar for user interaction.
st.sidebar.header("Dashboard Filters")
all_platforms = influencers_df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform(s)", options=all_platforms, default=all_platforms)

all_personas = sorted(influencers_df['persona'].unique().tolist())
selected_personas = st.sidebar.multiselect("Select Influencer Persona(s)", options=all_personas, default=all_personas)

min_date = tracking_df['date'].min()
max_date = tracking_df['date'].max()
selected_date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Safety check for the date range
if len(selected_date_range) != 2:
    st.warning("Please select a valid date range (start and end date).")
    st.stop()
start_date, end_date = selected_date_range

# --- STEP 3: FILTERING LOGIC ---
# Apply the user's filter selections to the data.
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

# --- PAGE CONTENT ---
st.title("💡 Deep Dive Insights")
st.markdown("Analyze the performance of individual influencers and personas based on the selected filters.")

# --- STEP 4: PREPARE THE DATA FOR CHARTS ---
# This step is crucial. It merges all data sources to create a single performance table.

# Stop if no data is available for the selected filters to avoid errors.
if payouts_filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections in the sidebar.")
    st.stop()

# Calculate revenue per influencer
revenue_per_influencer = influencer_tracking_filtered_df.groupby('influencer_id')['revenue'].sum().reset_index()
revenue_per_influencer.rename(columns={'revenue': 'attributed_revenue'}, inplace=True)

# Merge all dataframes: payouts -> influencers -> revenue
influencer_performance = pd.merge(payouts_filtered_df, influencers_df, on='influencer_id')
influencer_performance = pd.merge(influencer_performance, revenue_per_influencer, on='influencer_id', how='left')
influencer_performance['attributed_revenue'] = influencer_performance['attributed_revenue'].fillna(0)

# Calculate Incremental ROAS per influencer
total_campaign_spend = influencer_performance['total_payout'].sum()
non_influencer_df = tracking_filtered_df[tracking_filtered_df['source'] != 'influencer_campaign']
total_days_in_range = (end_date - start_date).days + 1
baseline_daily_revenue = non_influencer_df['revenue'].sum() / total_days_in_range if not non_influencer_df.empty and total_days_in_range > 0 else 0
expected_baseline_revenue = baseline_daily_revenue * total_days_in_range

if total_campaign_spend > 0:
    # Assign a portion of the total baseline revenue to each influencer based on their share of the total spend
    influencer_performance['baseline_share'] = (influencer_performance['total_payout'] / total_campaign_spend) * expected_baseline_revenue
    influencer_performance['incremental_revenue'] = influencer_performance['attributed_revenue'] - influencer_performance['baseline_share']
    
    # Calculate incremental ROAS, handling potential division by zero
    influencer_performance['incremental_roas'] = influencer_performance.apply(
        lambda row: row['incremental_revenue'] / row['total_payout'] if row['total_payout'] > 0 else 0, axis=1
    )
else:
    influencer_performance['incremental_roas'] = 0


# --- STEP 5: DISPLAY THE CHARTS ---
st.markdown("---")
# --- STEP 5: DISPLAY THE CHARTS (New, cleaner layout) ---
st.markdown("---")

# --- Chart 1: Top & Bottom 5 Influencers ---
st.subheader("Top & Bottom 5 Influencers")
top_5 = influencer_performance.nlargest(5, 'incremental_roas')
bottom_5 = influencer_performance.nsmallest(5, 'incremental_roas')
top_bottom_df = pd.concat([top_5, bottom_5]).sort_values('incremental_roas', ascending=False)

fig_influencers = px.bar(
    top_bottom_df,
    x='name',
    y='incremental_roas',
    color='incremental_roas',
    color_continuous_scale=px.colors.diverging.RdYlGn,
    color_continuous_midpoint=0,
    labels={'name': 'Influencer', 'incremental_roas': 'Incremental ROAS (x)'},
    height=500  # Give the chart more vertical space
)
fig_influencers.update_layout(
    yaxis_title="Incremental ROAS (x)",
    xaxis_title=None # Remove the x-axis title to save space
)
st.plotly_chart(fig_influencers, use_container_width=True)


# --- Chart 2: Persona Performance ---
st.subheader("Persona Performance")
persona_performance = influencer_performance.groupby('persona')['incremental_roas'].mean().reset_index()
persona_performance = persona_performance.sort_values('incremental_roas', ascending=False)

fig_personas = px.bar(
    persona_performance,
    x='persona',
    y='incremental_roas',
    color='incremental_roas',
    color_continuous_scale=px.colors.diverging.RdYlGn,
    color_continuous_midpoint=0,
    labels={'persona': 'Persona', 'incremental_roas': 'Average Incremental ROAS (x)'},
    height=500 # Give this chart more space too
)
fig_personas.update_layout(
    yaxis_title="Avg. Incremental ROAS (x)",
    xaxis_title=None
)
st.plotly_chart(fig_personas, use_container_width=True)