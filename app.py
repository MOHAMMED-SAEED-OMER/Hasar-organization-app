import streamlit as st
from supabase import create_client, Client

# Initialize Supabase connection
@st.cache_resource
def init_supabase() -> Client:
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Updated table name
TABLE_NAME = 'database'

# Fetch column names from the table
def get_column_names():
    try:
        response = supabase.table(TABLE_NAME).select("*").limit(1).execute()
        if response.data:
            return list(response.data[0].keys())
        else:
            return ["transaction type", "value", "date"]  # Fallback if table is empty
    except Exception as e:
        st.error(f"Error fetching column names: {e}")
        return []

# Fetch data
def fetch_data():
    try:
        response = supabase.table(TABLE_NAME).select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Streamlit App
st.title("Financial Data Overview")

# Display existing data
st.header("Current Database Records")
data = fetch_data()

if data:
    st.table(data)
else:
    st.write("No data found in the database.")
