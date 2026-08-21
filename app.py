from administrator import administrator_dashboard
import streamlit as st
from database import *
from auth import login_page
from super_admin import super_admin_dashboard
from student import student_dashboard
from customer_support import customer_support_dashboard
from administrator import administrator_dashboard


st.set_page_config(
    page_title="Gyan Pustak",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --primary: #1a3a5c;
        --accent: #e8a030;
        --bg: #f8f5f0;
        --card: #ffffff;
        --text: #1e1e1e;
        --muted: #6b7280;
        --success: #16a34a;
        --warning: #d97706;
        --danger: #dc2626;
        --border: #e5e7eb;
    }
            
    label, .stTextInput label, .stSelectbox label, .stDateInput label {
        color: #1a3a5c !important;
        font-weight: 600;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    h1, h2, h3 { font-family: 'Playfair Display', serif; color: var(--primary); }

    .stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover { background-color: #0f2840; transform: translateY(-1px); }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1.5px solid var(--border);
        font-family: 'DM Sans', sans-serif;
    }

    .card {
        background: #1F2937; /* dark gray */
       border-radius: 10px;
       padding: 1rem 1.2rem;
       font-size: 1.25rem;
       color: #E5E7EB; /* light text */
       border: 1px solid #374151;
       margin-bottom: 0.8rem;
       box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }

    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-pending { background: #fef3c7; color: #92400e; }
    .badge-assigned { background: #dbeafe; color: #1e40af; }
    .badge-solved { background: #d1fae5; color: #065f46; }
    .badge-notassigned { background: #f3f4f6; color: #374151; }

    .sidebar-brand {
        text-align: center;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        background-color: var(--primary) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.15);
        color: white;
        width: 100%;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.25); }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid var(--accent);
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: var(--primary); }
    .metric-label { color: var(--muted); font-size: 0.85rem; margin-top: 0.2rem; }

    .page-header {
        background: linear-gradient(135deg, var(--primary) 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .page-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .page-header p { color: rgba(255,255,255,0.8); margin: 0.3rem 0 0; }

    div[data-testid="stForm"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    .stDataFrame { border-radius: 8px; overflow: hidden; }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-family: 'DM Sans', sans-serif;
    }

    .book-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid var(--border);
        height: 100%;
        transition: box-shadow 0.2s;
    }
    .book-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .book-title { font-weight: 600; font-size: 1rem; color: var(--primary); }
    .book-author { color: var(--muted); font-size: 0.85rem; margin: 0.2rem 0; }
    .book-cat { font-size: 1rem; background: #eff6ff; color: #1d4ed8; padding: 0.15rem 0.5rem; border-radius:5px; }

    .ticket-card {
      background: #1F2937; /* dark gray */
      border-radius: 10px;
      padding: 1rem 1.2rem;
      color: #E5E7EB; /* light text */
      border: 1px solid #374151;
      margin-bottom: 0.8rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

def main():

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_page()
    else:
        user = st.session_state.user
        if "role" in user:
            role = user["role"]
        else:
            role = "student"

        if role == "super_admin":
             super_admin_dashboard(user)
        elif role == "student":
             student_dashboard(user)
        elif role == "customer_support":
             customer_support_dashboard(user)
        elif role == "administrator":
             administrator_dashboard(user)

if __name__ == "__main__":
    main()
