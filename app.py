import streamlit as st
from supabase import create_client

# Initialize Supabase connection
@st.cache_resource
def init_supabase():
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

def fetch_data():
    response = supabase.table("database").select("*").execute()
    return response.data

# Streamlit app
st.title("Financial Transactions App")

# Display existing data
st.header("Existing Transactions")
data = fetch_data()

if data:
    # Convert to DataFrame for better display
    df = st.dataframe(
        data,
        use_container_width=True,
        column_order=("transaction type", "value", "date"),
        column_config={
            "transaction type": "Transaction Type",
            "value": st.column_config.NumberColumn(
                "Amount",
                format="$%.2f"
            ),
            "date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD"
            )
        }
    )
else:
    st.write("No transactions found in the database.")

# Form to add new transactions
st.header("Add New Transaction")
with st.form("new_transaction_form"):
    transaction_type = st.text_input("Transaction Type*", help="Primary key (must be unique)")
    amount = st.number_input("Amount*", step=0.01, format="%.2f")
    date = st.date_input("Date*")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not transaction_type or not amount or not date:
            st.error("All fields marked with * are required!")
        else:
            try:
                supabase.table("database").insert({
                    "transaction type": transaction_type,
                    "value": float(amount),
                    "date": date.isoformat()
                }).execute()
                st.success("Transaction added successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {str(e)} (Possible duplicate transaction type?)")
