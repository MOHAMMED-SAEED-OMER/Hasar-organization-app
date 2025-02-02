import streamlit as st
from supabase import create_client, Client

# Initialize Supabase connection
def init_supabase() -> Client:
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Fetch column names from the table
def get_column_names():
    # Fetch a single row to infer columns
    response = supabase.table("finance_database").select("*").limit(1).execute()
    if response.data:
        return list(response.data[0].keys())
    else:
        # Return default column names if no data exists
        return ["id", "date", "amount", "category", "description"]  # Replace with actual columns

# Fetch data and columns
columns = get_column_names()
data_response = supabase.table("finance_database").select("*").execute()
data = data_response.data

# Streamlit app
st.title("Financial Data App")

# Display existing data
st.header("Existing Records")
if data:
    st.table(data)
else:
    st.write("No data found.")

# Form to add new data (automatically uses column names)
st.header("Add New Record")
with st.form("new_record_form"):
    input_values = {}
    for col in columns:
        # Skip "id" (auto-generated)
        if col == "id": 
            continue  
        input_values[col] = st.text_input(f"Enter {col}")

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Insert new record
        insert_response = supabase.table("finance_database").insert(input_values).execute()
        if insert_response.status_code == 201:
            st.success("Record added!")
        else:
            st.error(f"Failed to add record: {insert_response.error_message}")
        st.experimental_rerun()
