import streamlit as st
import pandas as pd

def render_dashboard(data):
    st.title("📊 Employee Attrition Dashboard")
    st.write("Analisis menyeluruh tentang distribusi data SDM yang terangkum secara statistik.")
    st.write("")
    
    if data:
        metrics = data['metrics']

        # Row 2: Deep Analysis (Looker Studio Embed)
        st.markdown("#### 🔗 Deep Analytics Report")
        st.info("Visualisasi di bawah ini terhubung langsung ke Google Looker Studio untuk analisis data yang lebih mendalam.")
        
        # Looker Studio Embed
        looker_url = "https://lookerstudio.google.com/embed/reporting/9134b251-00e8-4bb2-b76b-8d4bf82515cb/page/uV3qF"
        
        st.components.v1.html(
            f'<iframe width="100%" height="900" src="{looker_url}" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>',
            height=900
        )
            
    else:
        st.error("❌ Gagal memuat data dashboard. Pastikan koneksi internet tersedia atau hubungi administrator sistem.")
