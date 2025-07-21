# pages/2_Deep_Dive_Insights.py - FINAL CSV VERSION

import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Deep Dive Insights", page_icon="💡", layout="wide")

# --- CSV DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    data_path = 'data/'
    influencers = pd.read_csv(data_path + 'influencers.csv')
    posts = pd.read_csv(data_path + 'posts.csv')
    tracking = pd.read_csv(data_path + 'tracking_data.csv')
    payouts = pd.read_csv(data_path + 'payouts.csv')
    posts['date'] = pd.to_datetime(posts['date'])
    tracking['date'] = pd.to_datetime(tracking['date'])
    return influencers, posts, tracking, payouts

# --- LOAD DATA ---
try:
    influencers_df, posts_df, tracking_df, payouts_df = load_data()
except FileNotFoundError:
    st.error("Data files not found."); st.stop()

# --- SIDEBAR FILTERS ---
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

# --- FILTERING LOGIC ---
filtered_influencer_ids = influencers_df[(influencers_df['platform'].isin(selected_platforms)) & (influencers_df['persona'].isin(selected_personas))]['influencer_id'].tolist()
payouts_filtered_df = payouts_df[payouts_df['influencer_id'].isin(filtered_influencer_ids)]
tracking_filtered_df = tracking_df[(tracking_df['date'] >= pd.to_datetime(start_date)) & (tracking_df['date'] <= pd.to_datetime(end_date))]
influencer_tracking_filtered_df = tracking_filtered_df[tracking_filtered_df['influencer_id'].isin(filtered_influencer_ids)]

# --- PAGE CONTENT ---
st.title("💡 Deep Dive Insights")
st.markdown("Analyze the performance of individual influencers and personas based on the selected filters.")

if payouts_filtered_df.empty:
    st.warning("No data available for the selected filters."); st.stop()

# --- PREPARE DATA FOR CHARTS ---
revenue_per_influencer = influencer_tracking_filtered_df.groupby('influencer_id')['revenue'].sum().reset_index()
revenue_per_influencer.rename(columns={'revenue': 'attributed_revenue'}, inplace=True)
influencer_performance = pd.merge(payouts_filtered_df, influencers_df, on='influencer_id')
influencer_performance = pd.merge(influencer_performance, revenue_per_influencer, on='influencer_id', how='left')
influencer_performance['attributed_revenue'] = influencer_performance['attributed_revenue'].fillna(0)
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

# --- DISPLAY CHARTS ---
st.markdown("---")
st.subheader("Top & Bottom 5 Influencers")
top_5 = influencer_performance.nlargest(5, 'incremental_roas')
bottom_5 = influencer_performance.nsmallest(5, 'incremental_roas')
top_bottom_df = pd.concat([top_5, bottom_5]).sort_values('incremental_roas', ascending=False)
fig_influencers = px.bar(
    top_bottom_df, x='name', y='incremental_roas', color='incremental_roas',
    color_continuous_scale=px.colors.diverging.RdYlGn, color_continuous_midpoint=0,
    labels={'name': 'Influencer', 'incremental_roas': 'Incremental ROAS (x)'}, height=500
)
fig_influencers.update_layout(yaxis_title="Incremental ROAS (x)", xaxis_title=None)
st.plotly_chart(fig_influencers, use_container_width=True)

st.subheader("Persona Performance")
persona_performance = influencer_performance.groupby('persona')['incremental_roas'].mean().reset_index()
persona_performance = persona_performance.sort_values('incremental_roas', ascending=False)
fig_personas = px.bar(
    persona_performance, x='persona', y='incremental_roas', color='incremental_roas',
    color_continuous_scale=px.colors.diverging.RdYlGn, color_continuous_midpoint=0,
    labels={'persona': 'Persona', 'incremental_roas': 'Average Incremental ROAS (x)'}, height=500
)
fig_personas.update_layout(yaxis_title="Avg. Incremental ROAS (x)", xaxis_title=None)
st.plotly_chart(fig_personas, use_container_width=True)