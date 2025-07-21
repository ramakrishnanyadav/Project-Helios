# dashboard.py - DEBUGGING VERSION

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Helios: Debugging", page_icon="🐞", layout="wide"
)

st.title("🐞 Debugging Snowflake Connection")

# --- FUNCTION DEFINITION WITH HARDCODED SECRETS FOR TESTING ---
@st.cache_data(ttl=30) # Use a short cache for debugging
def load_data_from_snowflake_debug():
    st.info("Attempting to connect to Snowflake with hardcoded credentials...")
    
    # Bypassing secrets.toml by putting credentials directly here
    conn = st.connection(
        "snowflake",
        type="snowflake", # Explicitly define the connection type
        user="RAMAKRISHNAYADAV",
        password="Your-New-Password-Goes-Here",
        account="ud57115.ap-southeast-1",
        warehouse="HELIOS_WH",
        database="HEALTHKART_DB",
        schema="RAW",
        role="SYSADMIN"
    )
    
    st.success("st.connection() call was successful!")
    
    query_influencers = "SELECT * FROM HEALTHKART_DB.RAW.INFLUENCERS LIMIT 10;"
    st.info(f"Running query: {query_influencers}")
    
    influencers = conn.query(query_influencers)
    
    st.success("Query was successful! Data received from Snowflake.")
    st.dataframe(influencers)
    
    return influencers

# --- Call the debug function ---
try:
    load_data_from_snowflake_debug()
except Exception as e:
    st.error(f"""
        **The connection attempt failed.**
        This means there is an issue with the credentials below, or with permissions in Snowflake.

        - **User:** RAMAKRISHNAYADAV
        - **Account:** ud57115.ap-southeast-1
        - **Warehouse:** HELIOS_WH
        - **Database:** HEALTHKART_DB
        
        **Error from Snowflake:**
        {e}
    """)