import streamlit as st
from supabase import create_client
import httpx

# 1. MUST BE FIRST - Page configuration
st.set_page_config(
    page_title="Finance Debugger",
    page_icon="🐞",
    layout="wide",
    menu_items={
        'About': "# Diagnostic Version\n⚠️ Remove debug sections after testing"
    }
)

# 2. Supabase initialization with enhanced error handling
@st.cache_resource
def init_supabase():
    try:
        st.write("## 🔌 Initializing Supabase Connection")
        SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
        SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
        
        # Configure HTTP transport for better debugging
        transport = httpx.HTTPTransport(
            retries=5,
            verify=False  # Temporarily disable SSL verification for testing
        )
        
        client = create_client(SUPABASE_URL, SUPABASE_KEY, transport=transport)
        st.success("Supabase client created")
        return client
        
    except KeyError as e:
        st.error(f"❌ Missing secret: {e}")
        st.error("Check Streamlit Secrets configuration!")
        st.stop()
    except Exception as e:
        st.error(f"🔥 Critical Connection Error: {str(e)}")
        st.stop()

supabase = init_supabase()

# 3. Connection Test Suite
st.header("🔍 Connection Tests")

# Test 1: Basic API Ping
try:
    st.write("### 🧪 Test 1: API Health Check")
    health = supabase.health()
    st.success(f"✅ API Responsive | Version: {health.version}")
except Exception as e:
    st.error(f"❌ API Unreachable: {str(e)}")
    st.stop()

# Test 2: Table Existence Check
try:
    st.write("### 🧪 Test 2: Table Verification")
    tables = supabase.get_tables()
    if "database" not in tables:
        st.error(f"❌ Table 'database' not found! Existing tables: {tables}")
        st.stop()
    st.success("✅ 'database' table exists")
except Exception as e:
    st.error(f"❌ Table Check Failed: {str(e)}")
    st.stop()

# Test 3: Column Structure Validation
try:
    st.write("### 🧪 Test 3: Column Check")
    expected_columns = {"transaction type", "value", "date"}
    actual_columns = set(supabase.table("database").columns)
    
    if not expected_columns.issubset(actual_columns):
        st.error(f"❌ Column mismatch!\nExpected: {expected_columns}\nFound: {actual_columns}")
        st.stop()
    st.success("✅ Table columns match expectations")
except Exception as e:
    st.error(f"❌ Column Check Failed: {str(e)}")
    st.stop()

# 4. Data Fetching Debug
st.header("📦 Data Retrieval Diagnostics")
try:
    st.write("### 🔄 Attempting Data Fetch")
    response = supabase.table("database").select("*").execute()
    st.success(f"✅ Query executed | Status: {response.status}")
    
    st.write("### 🗄️ Raw Response Data")
    st.json(response)
    
    data = response.data
    st.write(f"### 📊 Records Found: {len(data)}")
    st.dataframe(data)
    
except Exception as e:
    st.error(f"❌ Data Fetch Failed: {str(e)}")
    st.stop()

# 5. Temporary RLS Policy Check (Remove after testing)
st.header("🔓 Temporary RLS Check")
try:
    st.write("### 🛡️ Current Security Policies")
    policies = supabase.table("pg_policies").select("*").execute().data
    if not policies:
        st.warning("⚠️ No RLS Policies Found - Data may be unprotected!")
    else:
        st.dataframe(policies)
except Exception as e:
    st.error(f"❌ Policy Check Failed: {str(e)}")

# 6. Main Application Interface
st.header("📈 Production Interface")
if data:
    st.write("### 💳 Transactions Overview")
    st.dataframe(
        data,
        column_config={
            "transaction type": "Type",
            "value": st.column_config.NumberColumn("Amount", format="$%.2f"),
            "date": "Date"
        },
        use_container_width=True
    )
else:
    st.warning("No transactions found")

# 7. Add Data Form
with st.form("add_transaction"):
    st.write("### ➕ Add Transaction")
    col1, col2 = st.columns(2)
    
    with col1:
        trans_type = st.text_input("Transaction Type*")
        amount = st.number_input("Amount*", step=0.01)
    
    with col2:
        trans_date = st.date_input("Date*")
    
    if st.form_submit_button("Submit"):
        if not all([trans_type, amount, trans_date]):
            st.error("Missing required fields!")
        else:
            try:
                supabase.table("database").insert({
                    "transaction type": trans_type,
                    "value": amount,
                    "date": trans_date.isoformat()
                }).execute()
                st.success("Transaction added!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Insert failed: {str(e)}")

# 8. Connection Troubleshooting Guide
st.header("🔧 Troubleshooting Guide")
with st.expander("Common Fixes"):
    st.markdown("""
    1. **RLS Policies**: Enable SELECT/INSERT permissions in Supabase
    2. **CORS Settings**: Add your Streamlit URL to Supabase's CORS config
    3. **API Keys**: Regenerate keys if compromised
    4. **Network Issues**: Check firewall/network restrictions
    5. **Table Name**: Verify exact case sensitivity ('database')
    """)

st.write("---")
st.caption("🔒 Remove debug sections before production deployment")
