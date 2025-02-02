import streamlit as st
from supabase import create_client, Client

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Finance Tracker", 
    page_icon="💰", 
    layout="wide",
    menu_items={
        'About': "### Financial Transactions Manager\nSecure interface for managing organizational finances"
    }
)

# Initialize Supabase connection with error handling
@st.cache_resource
def init_supabase():
    try:
        SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
        SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except KeyError as e:
        st.error(f"Missing secret: {e}. Check your Streamlit secrets configuration!")
        st.stop()
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.stop()

supabase = init_supabase()

def fetch_data():
    try:
        response = supabase.table("database").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

# Main app
st.title("💰 Financial Transactions Manager")
st.markdown("---")

# Rest of your code remains the same...
# [Keep the existing display and form code here]
