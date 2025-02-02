import streamlit as st
from supabase import create_client, Client

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

# Streamlit app layout
st.set_page_config(page_title="Finance Tracker", page_icon="💰", layout="wide")

# Main app
st.title("💰 Financial Transactions Manager")
st.markdown("---")

# Display existing data
st.header("📋 Existing Transactions")
data = fetch_data()

if data:
    st.data_editor(
        data,
        column_config={
            "transaction type": st.column_config.TextColumn(
                "Transaction Type",
                help="Primary key (unique identifier)",
                disabled=True
            ),
            "value": st.column_config.NumberColumn(
                "Amount",
                format="$%.2f",
                help="Transaction value"
            ),
            "date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
                help="Transaction date"
            )
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.warning("No transactions found in the database.")

# Add new transaction form
st.markdown("---")
st.header("➕ Add New Transaction")

with st.form("add_transaction", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        transaction_type = st.text_input(
            "Transaction Type*",
            placeholder="e.g., 'Office Supplies'",
            help="Must be unique"
        )
    
    with col2:
        amount = st.number_input(
            "Amount*",
            min_value=0.0,
            step=10.0,
            format="%.2f",
            help="Enter positive value"
        )
    
    with col3:
        date = st.date_input("Transaction Date*")
    
    submitted = st.form_submit_button("Submit Transaction", type="primary")

    if submitted:
        if not all([transaction_type, amount, date]):
            st.error("All fields marked with * are required!")
        else:
            try:
                supabase.table("database").insert({
                    "transaction type": transaction_type.strip(),
                    "value": float(amount),
                    "date": date.isoformat()
                }).execute()
                st.success("Transaction added successfully!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}. Possible duplicate transaction type or database connection issue.")

# Footer
st.markdown("---")
st.markdown("🔒 **Security Note:** All data is stored in secure Supabase database with encrypted connections.")
