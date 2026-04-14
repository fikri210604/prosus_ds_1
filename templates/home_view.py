import streamlit as st

def render_home():
    st.title("Welcome to PredictApp 🔮")
    st.markdown("### Employee Attrition Prediction System")
    st.write("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        PredictApp adalah platform cerdas berbasis Machine Learning yang dirancang untuk memberdayakan Tim HR (Human Resources). 
        Aplikasi ini memprediksi secara akurat kemungkinan karyawan untuk berhenti kerja (**Attrition**), 
        membantu perusahaan melakukan tindakan preventif lebih awal demi mempertahankan talenta terbaik mereka.
        """)
        
        st.info("💡 **Catatan Model**: Aplikasi *deployment* web ini sengaja menerapkan teknik *Feature Selection* dari *Notebook* observasi (*Jupyter*) orisinal. Sistem menyaring data dari 34 atribut penuh menjadi **10 Fitur Teratas (Top 10 Features)** demi menjaga kepraktisan pengisian *form* oleh *User* / HR tanpa mengurangi ketajaman prediksi secara drastis.")

        st.write("")
        st.markdown("""
        **Fitur Utama Platform:**
        - 📊 **Dashboard Executive**: Eksplor visualisasi distribusi data statistik karyawan berdasarkan demografi, jabatan, lembur, dan gaji.
        - 🧠 **Prediction Engine**: Evaluasi profil presisi (10 Parameter) menggunakan *Logistic Regression* yang dikerjakan via Form Kuis canggih.
        - 🔭 **MLflow Tracker**: Observatorium eksperimentasi model machine learning di belakan layar.
        """)
    
    with col2:
        try:
            st.image("https://img.freepik.com/free-vector/human-resources-concept-idea-recruitment-employment-human-resources-manager-interviews-employee-candidate-headhunter-looking-job-applicant-flat-vector-illustration_613284-3079.jpg?w=826")
        except:
            st.info("Visual representation failed to load.")
