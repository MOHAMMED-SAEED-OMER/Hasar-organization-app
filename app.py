import streamlit as st
from supabase import create_client

# Initialize Supabase connection
@st.cache_resource
def init_supabase():
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Fetch column names from the table
def get_column_names():
    # Fetch a single row to infer columns
    response = supabase.table("Finance database").select("*").limit(1).execute()
    if response.data:
        return list(response.data[0].keys())
    else:
        # If the table is empty, fetch columns via SQL query
        query = '''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'Finance database'
        '''
        result = supabase.execute(query).data
        return [col["column_name"] for col in result]

# Fetch data and columns
columns = get_column_names()
data = supabase.table("Finance database").select("*").execute().data

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
        if col == "id": continue  
        input_values[col] = st.text_input(f"Enter {col}")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Insert new record
        supabase.table("Finance database").insert(input_values).execute()
        st.success("Record added!")
        st.experimental_rerun()
