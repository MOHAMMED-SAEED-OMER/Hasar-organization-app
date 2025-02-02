import streamlit as st
from supabase import create_client, Client

# Initialize Supabase connection
@st.cache_resource
def init_supabase() -> Client:
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Use the exact table name
TABLE_NAME = 'finance database'

# Fetch column names from the table
def get_column_names():
    try:
        # Fetch a single row to infer columns
        response = supabase.table(TABLE_NAME).select("*").limit(1).execute()
        if response.data:
            return list(response.data[0].keys())
        else:
            # Querying information_schema to fetch column names
            result = supabase.table('information_schema.columns') \
                             .select('column_name') \
                             .eq('table_name', 'finance database') \
                             .execute()
            return [col["column_name"] for col in result.data]
    except Exception as e:
        st.error(f"Error fetching column names: {e}")
        return []

# Fetch data and columns
columns = get_column_names()

try:
    data_response = supabase.table(TABLE_NAME).select("*").execute()
    data = data_response.data
except Exception as e:
    st.error(f"Error fetching data: {e}")
    data = []

# Streamlit app
st.title("Financial Data App")

# Display existing data
st.header("Existing Records")
if data:
    st.table(data)
else:
    st.write("No data found.")

# Form to add new data
st.header("Add New Record")
with st.form("new_record_form"):
    input_values = {}
    for col in columns:
        if col == "id":  # Skip auto-generated ID
            continue
        input_values[col] = st.text_input(f"Enter {col}")

    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            # Insert new record
            supabase.table(TABLE_NAME).insert(input_values).execute()
            st.success("Record added successfully!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error adding record: {e}")
