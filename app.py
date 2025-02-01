import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    url = "https://your-supabase-url.supabase.co"  # Replace with your Supabase URL
    key = "your-anon-key"  # Replace with your Supabase API key
    return create_client(url, key)

supabase = init_supabase()

# Fetch data from Supabase table
def fetch_data():
    response = supabase.table("financial_data").select("*").execute()
    return response.data

# Display data in Streamlit
st.title("Financial Data App")
st.write("Here's the data from your Supabase table:")

data = fetch_data()
st.table(data)
