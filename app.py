import streamlit as st
from model.modeling import get_dashboard_data
from templates.home_view import render_home
from templates.dashboard_view import render_dashboard
from templates.prediction_view import render_prediction

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="PredictApp — Employee Attrition",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("static/styles.css")

# 3. Chaching Data Dashboard
@st.cache_data(ttl=3600)
def fetch_cached_dashboard_data():
    return get_dashboard_data()

# 4. Sidebar & Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103322.png", width=60)
    st.title("Navigation")
    
    options = ["🏠 Home", "📊 Dashboard", "🔮 Prediction"]
    selected_page = st.radio("Go to", options, label_visibility="collapsed")
    page = selected_page.split(" ")[1]
    
    st.divider()
    st.markdown("### 🔬 MLOps Tracking")
    st.info("Akses Dashboard MLflow untuk meninjau hasil eksperimen training.")
    st.markdown(
        '<a href="http://localhost:5001" target="_blank" style="text-decoration:none;">'
        '<button style="width:100%; padding:10px; border-radius:8px; border:1px solid #06b6d4; background:transparent; color:#06b6d4; cursor:pointer; font-weight:bold; transition:0.3s;">'
        '📈 Buka MLflow UI'
        '</button></a>', unsafe_allow_html=True
    )
    st.divider()
    st.caption("Prosus DS Project 1 | Ahmad Fikri Hanif")

# 5. Routing (Memanggil Modul yang Terpisah di /templates)
if page == "Home":
    render_home()
elif page == "Dashboard":
    data = fetch_cached_dashboard_data()
    render_dashboard(data)
elif page == "Prediction":
    render_prediction()
