import streamlit as st
import pandas as pd
from model.modeling import predict_single_data, get_dashboard_data

# Konfigurasi Halaman
st.set_page_config(
    page_title="PredictApp — Employee Attrition",
    page_icon="🔮",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Prediction"])

if page == "Home":
    st.title("Welcome to PredictApp 🔮")
    st.markdown("""
    ### Employee Attrition Prediction System
    PredictApp adalah platform berbasis Machine Learning yang dirancang untuk membantu divisi HR dalam 
    menganalisis dan memprediksi kemungkinan karyawan untuk berhenti kerja (**Attrition**).
    
    **Fitur Utama:**
    - **Dashboard**: Visualisasi data statistik karyawan berdasarkan departemen, peran, dan pendapatan.
    - **Prediction**: Form input untuk memprediksi probabilitas resign seorang karyawan berdasarkan 10 fitur utama.
    
    ---
    *Pilih navigasi di sebelah kiri untuk memulai.*
    """)

elif page == "Dashboard":
    st.title("📊 Employee Attrition Dashboard")
    
    data = get_dashboard_data()
    
    if data:
        metrics = data['metrics']
        
        # Row 1: Key Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Employees", metrics['total_employees'])
        col2.metric("Attrition Count", metrics['attrition_count'])
        col3.metric("Attrition Rate", f"{metrics['attrition_rate']}%")
        
        st.divider()
        
        # Row 2: Charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Attrition by Department")
            dept_df = pd.DataFrame({
                'Department': data['chart_dept']['labels'],
                'Count': data['chart_dept']['data']
            })
            st.bar_chart(dept_df.set_index('Department'))
            
        with col_right:
            st.subheader("Avg Income by Attrition")
            income_df = pd.DataFrame({
                'Status': data['chart_income']['labels'],
                'Avg Income': data['chart_income']['data']
            })
            st.bar_chart(income_df.set_index('Status'))
            
        st.subheader("Attrition by Job Role")
        role_df = pd.DataFrame({
            'Job Role': data['chart_role']['labels'],
            'Count': data['chart_role']['data']
        })
        st.bar_chart(role_df.set_index('Job Role'))
    else:
        st.error("Gagal memuat data dashboard.")

elif page == "Prediction":
    st.title("🔮 Prediction Form")
    st.write("Masukkan data karyawan di bawah untuk memprediksi probabilitas **Attrition** (Resign).")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            overtime = st.selectbox("OverTime (Kerja Lembur)", ["No", "Yes"])
            travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
            marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            education = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources"])
            role = st.selectbox("Job Role", ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"])

        with col2:
            env_sat = st.slider("Environment Satisfaction", 1, 4, 3)
            job_sat = st.slider("Job Satisfaction", 1, 4, 3)
            job_inv = st.slider("Job Involvement", 1, 4, 3)
            wlb = st.slider("Work Life Balance", 1, 4, 3)
            dist = st.number_input("Distance From Home (miles)", 1, 50, 10)
            
        submit = st.form_submit_button("🔮 Predict Attrition")
        
        if submit:
            input_data = {
                'OverTime': overtime,
                'BusinessTravel': travel,
                'MaritalStatus': marital,
                'JobRole': role,
                'EnvironmentSatisfaction': env_sat,
                'JobSatisfaction': job_sat,
                'JobInvolvement': job_inv,
                'WorkLifeBalance': wlb,
                'EducationField': education,
                'DistanceFromHome': dist,
            }
            
            with st.spinner("Calculating..."):
                result = predict_single_data(input_data)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.divider()
                st.subheader("Prediction Result")
                
                if "RESIGN" in result['prediction']:
                    st.warning(f"Hasil: **{result['prediction']}**")
                else:
                    st.success(f"Hasil: **{result['prediction']}**")
                    
                st.info(f"Confidence / Probability: **{result['confidence']}**")

# Footer
st.sidebar.divider()
st.sidebar.info("Prosus DS Project 1 — Ahmad Fikri Hanif")
