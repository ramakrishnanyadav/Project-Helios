# dashboard.py - DIRECT CONNECTION DEBUGGING

import streamlit as st
import pandas as pd
import snowflake.connector # Import the library directly

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Helios: Direct Debugging", page_icon="🔧", layout="wide"
)

st.title("🔧 Direct Snowflake Connection Test")

# --- Function to get a direct connection ---
@st.cache_resource # Use cache_resource for connection objects
def get_snowflake_connection():
    st.info("Attempting to establish a direct connection...")
    
    # Use the connector directly with your credentials
    conn = snowflake.connector.connect(
        user="RAMAKRISHNAYADAV",
        password="Your-New-Password-Goes-Here",
        account="ud57115.ap-southeast-1",
        warehouse="HELIOS_WH",
        database="HEALTHKART_DB",
        schema="RAW",
        role="SYSADMIN"
    )
    
    st.success("Direct connection to Snowflake was successful!")
    return conn

# --- Main app logic ---
try:
    # Get the connection object
    conn = get_snowflake_connection()
    
    # Create a cursor object to execute queries
    cur = conn.cursor()
    
    # Execute a simple query
    query = "SELECT * FROM HEALTHKART_DB.RAW.INFLUENCERS LIMIT 10;"
    st.info(f"Executing query: {query}")
    cur.execute(query)
    
    # Fetch the results into a pandas DataFrame
    df = cur.fetch_pandas_all()
    
    st.success("Query executed and data fetched successfully!")
    st.dataframe(df)

except Exception as e:
    st.error(f"""
        **The direct connection or query failed.**
        This points to an issue with credentials or Snowflake permissions.

        **Error details:**
        {e}
    """)
finally:
    # Ensure the connection is closed
    if 'conn' in locals() and conn is not None:
        conn.close()
        st.info("Connection closed.")