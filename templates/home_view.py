import streamlit as st

def render_home():
    # --- HERO SECTION ---
    st.markdown("""
    <div class="hero-container">
        <span class="hero-badge">🚀 Machine Learning Powered</span>
        <div class="hero-title">PredictApp</div>
        <p class="hero-subtitle">
            Platform cerdas berbasis <strong style="color:#a5b4fc;">Machine Learning</strong> yang memberdayakan Tim HR
            untuk memprediksi kemungkinan karyawan <em>resign</em> — membantu perusahaan mempertahankan
            talenta terbaik mereka melalui tindakan preventif berbasis data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- FEATURE CARDS ---
    st.write("")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card c1 anim-delay-1">
            <span class="feature-icon">📊</span>
            <div class="feature-title">Dashboard Executive</div>
            <div class="feature-desc">
                Eksplor visualisasi distribusi data statistik karyawan berdasarkan demografi, jabatan, lembur, dan gaji.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card c2 anim-delay-2">
            <span class="feature-icon">🧠</span>
            <div class="feature-title">Prediction Engine</div>
            <div class="feature-desc">
                Evaluasi profil karyawan secara presisi menggunakan 10 parameter teratas via form kuis interaktif yang ditenagai algoritma Logistic Regression.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card c3 anim-delay-3">
            <span class="feature-icon">🔭</span>
            <div class="feature-title">MLflow Tracker</div>
            <div class="feature-desc">
                Observatorium eksperimentasi model ML di belakang layar — lacak hyperparameter dan performa akurasi.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- HOW IT WORKS ---
    st.write("")
    st.markdown("""
    <div class="workflow-section">
        <div class="workflow-section-title">Bagaimana Cara Kerjanya?</div>
        <p class="workflow-section-sub">Empat langkah sederhana untuk memprediksi attrisi karyawan</p>
    </div>
    """, unsafe_allow_html=True)
    
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown("""
        <div class="step-card anim-delay-1">
            <div class="step-number">1</div>
            <div class="step-label">Buka Prediction</div>
            <div class="step-sublabel">Navigasi ke halaman prediksi</div>
        </div>
        """, unsafe_allow_html=True)
    with step2:
        st.markdown("""
        <div class="step-card anim-delay-2">
            <div class="step-number">2</div>
            <div class="step-label">Isi Form Kuis</div>
            <div class="step-sublabel">Jawab 10 pertanyaan profil</div>
        </div>
        """, unsafe_allow_html=True)
    with step3:
        st.markdown("""
        <div class="step-card anim-delay-3">
            <div class="step-number">3</div>
            <div class="step-label">Analisis Model</div>
            <div class="step-sublabel">Algoritma memproses data</div>
        </div>
        """, unsafe_allow_html=True)
    with step4:
        st.markdown("""
        <div class="step-card anim-delay-4">
            <div class="step-number">4</div>
            <div class="step-label">Lihat Hasil</div>
            <div class="step-sublabel">Dapatkan prediksi klasifikasi</div>
        </div>
        """, unsafe_allow_html=True)

    # --- MODEL CALLOUT ---
    st.markdown("""
    <div class="model-callout anim-delay-2">
        <span class="callout-icon">💡</span>
        <div class="callout-content">
            <h4>Catatan tentang Model</h4>
            <p>
                Aplikasi <em>deployment</em> web ini sengaja menerapkan teknik <strong>Feature Selection</strong>
                dari Notebook observasi orisinal. Sistem menyaring data dari 34 atribut penuh
                menjadi <strong style="color:#818cf8;">10 Fitur Teratas</strong> — menjaga
                kepraktisan pengisian form tanpa mengurangi ketajaman prediksi.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- TECH STACK ---
    st.markdown("""
    <div style="text-align:center;">
        <p style="color:#64748b; font-size:0.85rem; text-transform:uppercase; letter-spacing:2px; font-weight:600; margin-bottom:0.8rem;">
            Technology Stack
        </p>
        <div class="tech-stack">
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">📊 Streamlit</span>
            <span class="tech-badge">🧪 Scikit-Learn</span>
            <span class="tech-badge">📈 MLflow</span>
            <span class="tech-badge">🐳 Docker</span>
        </div>
        <p style="color:#475569; font-size:0.82rem; margin-top:2rem;">
            Prosus DS Project 1 — Built with ❤️ by Ahmad Fikri Hanif
        </p>
    </div>
    """, unsafe_allow_html=True)
