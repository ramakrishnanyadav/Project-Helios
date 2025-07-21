# pages/3_Data_Explorer.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Explorer", page_icon="💾", layout="wide")

# --- DATA LOADING AND FILTERING (Copied from other pages) ---
@st.cache_data
def load_data():
    data_path = 'data/'
    influencers = pd.read_csv(data_path + 'influencers.csv')
    tracking = pd.read_csv(data_path + 'tracking_data.csv')
    payouts = pd.read_csv(data_path + 'payouts.csv')
    tracking['date'] = pd.to_datetime(tracking['date'])
    return influencers, tracking, payouts

influencers_df, tracking_df, payouts_df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")
all_platforms = influencers_df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform(s)", options=all_platforms, default=all_platforms)
all_personas = sorted(influencers_df['persona'].unique().tolist())
selected_personas = st.sidebar.multiselect("Select Influencer Persona(s)", options=all_personas, default=all_personas)
min_date = tracking_df['date'].min()
max_date = tracking_df['date'].max()
selected_date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if len(selected_date_range) != 2:
    st.warning("Please select a valid date range."); st.stop()
start_date, end_date = selected_date_range

# Filtering logic
filtered_influencer_ids = influencers_df[(influencers_df['platform'].isin(selected_platforms)) & (influencers_df['persona'].isin(selected_personas))]['influencer_id'].tolist()
payouts_filtered_df = payouts_df[payouts_df['influencer_id'].isin(filtered_influencer_ids)]
tracking_filtered_df = tracking_df[(tracking_df['date'] >= pd.to_datetime(start_date)) & (tracking_df['date'] <= pd.to_datetime(end_date))]
influencer_tracking_filtered_df = tracking_filtered_df[tracking_filtered_df['influencer_id'].isin(filtered_influencer_ids)]

st.title("💾 Data Explorer")
st.markdown("View, filter, and download the detailed influencer performance data.")

if payouts_filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- Re-create the full influencer_performance_df ---
revenue_per_influencer = influencer_tracking_filtered_df.groupby('influencer_id')['revenue'].sum().reset_index()
revenue_per_influencer.rename(columns={'revenue': 'attributed_revenue'}, inplace=True)
influencer_performance = pd.merge(payouts_filtered_df, influencers_df, on='influencer_id')
influencer_performance = pd.merge(influencer_performance, revenue_per_influencer, on='influencer_id', how='left').fillna(0)

total_campaign_spend = influencer_performance['total_payout'].sum()
non_influencer_df = tracking_filtered_df[tracking_filtered_df['source'] != 'influencer_campaign']
total_days_in_range = (end_date - start_date).days + 1
baseline_daily_revenue = non_influencer_df['revenue'].sum() / total_days_in_range if not non_influencer_df.empty and total_days_in_range > 0 else 0
expected_baseline_revenue = baseline_daily_revenue * total_days_in_range

if total_campaign_spend > 0:
    influencer_performance['baseline_share'] = (influencer_performance['total_payout'] / total_campaign_spend) * expected_baseline_revenue
    influencer_performance['incremental_revenue'] = influencer_performance['attributed_revenue'] - influencer_performance['baseline_share']
    influencer_performance['incremental_roas'] = influencer_performance.apply(
        lambda row: row['incremental_revenue'] / row['total_payout'] if row['total_payout'] > 0 else 0, axis=1)
else:
    influencer_performance['incremental_roas'] = 0

# --- DISPLAY THE DATAFRAME ---
# Use st.dataframe to show the interactive table
st.dataframe(influencer_performance.style.format({
    'total_payout': '₹{:,.2f}',
    'attributed_revenue': '₹{:,.2f}',
    'incremental_revenue': '₹{:,.2f}',
    'incremental_roas': '{:.2f}x'
}))


# --- DOWNLOAD BUTTON ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(influencer_performance)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='influencer_performance_data.csv',
    mime='text/csv',
)