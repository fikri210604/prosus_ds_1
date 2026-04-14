import streamlit as st
import time
import pandas as pd
from model.modeling import predict_single_data

def render_prediction():
    st.title("🔮 Prediction Assistant")
    st.write("Jawab kuis profil karyawan berikut tahap demi tahap untuk menganalisis probabilitas pengunduran diri (**Attrition**).")
    
    st.info("💡 **Catatan Optimasi Panel**: Mengikuti *best-practice UX*, pengisian kuis ini telah disederhanakan dari **34 Atribut Orisinal Notebook** menjadi **10 Parameter Utama** saja melalui algoritma *Feature Selection*. Hal ini menjamin akurasi maksimum dengan kelelahan pengisian *form* yang minimum bagi Divisi HR Anda.")


    # ---------------------------------------------------------
    # UI STATE: WIZARD & WIDGET TRACKING
    # ---------------------------------------------------------
    if 'step' not in st.session_state:
        st.session_state.step = 1

    defaults = {
        'JobRole': "Pilih Role",
        'OverTime': "Pilih Status",
        'BusinessTravel': "Pilih Status",
        'EducationField': "Pilih Bidang",
        'MaritalStatus': "Pilih Status",
        'EnvironmentSatisfaction': "Pilih Skala",
        'JobSatisfaction': "Pilih Skala",
        'JobInvolvement': "Pilih Skala",
        'WorkLifeBalance': "Pilih Skala",
        'DistanceFromHome': -1
    }
    if 'form_data' not in st.session_state:
        st.session_state.form_data = defaults.copy()
    else:
        # Sinkronisasi kunci jika ada fitur baru yang baru ditambahkan
        for key in defaults:
            if key not in st.session_state.form_data:
                st.session_state.form_data[key] = defaults[key]


    def calculate_progress():
        completed = 0
        for key in defaults:
            if st.session_state.form_data[key] != defaults[key]:
                completed += 1
        return completed / len(defaults)

    # Progress bar di paling atas (Navbar-ish area untuk Prediction)
    progress = calculate_progress()
    st.markdown(f"**Progress Kelengkapan Kuis: {int(progress * 100)}%**")
    st.progress(progress)
    st.divider()

    # Navigasi Step
    def next_step():
        if st.session_state.step < 4:
            st.session_state.step += 1
    
    def prev_step():
        if st.session_state.step > 1:
            st.session_state.step -= 1

    # ==============================
    # WIZARD: STEP 1
    # ==============================
    if st.session_state.step == 1:
        st.markdown("### Tahap 1: Profil Demografi Umum")
        
        # Marital Status
        opts_marital = ["Pilih Status", "Single", "Married", "Divorced"]
        st.session_state.form_data['MaritalStatus'] = st.selectbox(
            "Marital Status", 
            opts_marital,
            index=opts_marital.index(st.session_state.form_data['MaritalStatus']) if st.session_state.form_data['MaritalStatus'] in opts_marital else 0,
            help="Status Pernikahan Karyawan."
        )
        
        # Education Field
        opts_edu = ["Pilih Bidang", "Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources"]
        st.session_state.form_data['EducationField'] = st.selectbox(
            "Education Field", 
            opts_edu,
            index=opts_edu.index(st.session_state.form_data['EducationField']) if st.session_state.form_data['EducationField'] in opts_edu else 0,
            help="Bidang Pendidikan (Field of Education)."
        )

        st.write("")
        if st.button("Lanjutkan ➡️ "):
            next_step()
            st.rerun()

    # ==============================
    # WIZARD: STEP 2
    # ==============================
    elif st.session_state.step == 2:
        st.markdown("### Tahap 2: Beban Kerja & Komitmen Jarak")

        # Job Role
        opts_role = ["Pilih Role", "Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"]
        st.session_state.form_data['JobRole'] = st.selectbox(
            "Job Role", 
            opts_role,
            index=opts_role.index(st.session_state.form_data['JobRole']) if st.session_state.form_data['JobRole'] in opts_role else 0,
            help="Peran pekerjaan (Job Roles)."
        )

        # Distance From Home
        dist_val = st.session_state.form_data['DistanceFromHome']
        dist_input = st.number_input(
            "Distance From Home (Jarak dari Tempat Kerja ke Rumah)", 
            min_value=0, max_value=150,
            value=dist_val if dist_val != -1 else 0,
            help="Jarak dari tempat kerja ke rumah (dalam km)."
        )
        if dist_input != 0 or dist_val != -1: 
             st.session_state.form_data['DistanceFromHome'] = dist_input

        # OverTime
        opts_ot = ["Pilih Status", "No", "Yes"]
        st.session_state.form_data['OverTime'] = st.selectbox(
            "OverTime", 
            opts_ot,
            index=opts_ot.index(st.session_state.form_data['OverTime']) if st.session_state.form_data['OverTime'] in opts_ot else 0,
            help="Apakah karyawan sering bekerja lembur?"
        )

        # Business Travel
        opts_travel = ["Pilih Status", "Travel_Rarely", "Travel_Frequently", "Non-Travel"]
        st.session_state.form_data['BusinessTravel'] = st.selectbox(
            "Business Travel", 
            opts_travel,
            index=opts_travel.index(st.session_state.form_data['BusinessTravel']) if st.session_state.form_data['BusinessTravel'] in opts_travel else 0,
            help="Komitmen karyawan untuk bepergian dalam urusan pekerjaan (Travel commitments for the job)."
        )

        st.write("")
        col_b, col_n = st.columns([2, 10])
        with col_b:
            if st.button("⬅️ Kembali"):
                prev_step()
                st.rerun()
        with col_n:
            if st.button("Selanjutnya ➡️ "):
                next_step()
                st.rerun()

    # ==============================
    # WIZARD: STEP 3
    # ==============================
    elif st.session_state.step == 3:
        st.markdown("### Tahap 3: Skala Kepuasan Survei HR")
        
        opts_4scale = ["Pilih Skala", "1 - Low", "2 - Medium", "3 - High", "4 - Very High"]
        opts_4scale_wlb = ["Pilih Skala", "1 - Low", "2 - Good", "3 - Excellent", "4 - Outstanding"]

        # Environment Satisfaction
        st.session_state.form_data['EnvironmentSatisfaction'] = st.selectbox(
            "Environment Satisfaction", 
            opts_4scale,
            index=opts_4scale.index(st.session_state.form_data['EnvironmentSatisfaction']) if st.session_state.form_data['EnvironmentSatisfaction'] in opts_4scale else 0,
            help="Kepuasan terhadap lingkungan fisik tempat bekerja: 1-Low, 2-Medium, 3-High, 4-Very High"
        )
        # Job Satisfaction
        st.session_state.form_data['JobSatisfaction'] = st.selectbox(
            "Job Satisfaction", 
            opts_4scale,
            index=opts_4scale.index(st.session_state.form_data['JobSatisfaction']) if st.session_state.form_data['JobSatisfaction'] in opts_4scale else 0,
            help="Kepuasan terhadap pekerjaan yang dilakukan: 1-Low, 2-Medium, 3-High, 4-Very High"
        )
        # Job Involvement
        st.session_state.form_data['JobInvolvement'] = st.selectbox(
            "Job Involvement", 
            opts_4scale,
            index=opts_4scale.index(st.session_state.form_data['JobInvolvement']) if st.session_state.form_data['JobInvolvement'] in opts_4scale else 0,
            help="Tingkat keterlibatan emosional/psikologis dalam tugas: 1-Low, 2-Medium, 3-High, 4-Very High"
        )
        # Work Life Balance
        st.session_state.form_data['WorkLifeBalance'] = st.selectbox(
            "Work Life Balance", 
            opts_4scale_wlb,
            index=opts_4scale_wlb.index(st.session_state.form_data['WorkLifeBalance']) if st.session_state.form_data['WorkLifeBalance'] in opts_4scale_wlb else 0,
            help="Keseimbangan kehidupan kerja dan personal: 1-Low, 2-Good, 3-Excellent, 4-Outstanding"
        )

        st.write("")
        col_b, col_n = st.columns([2, 10])
        with col_b:
            if st.button("⬅️ Kembali"):
                prev_step()
                st.rerun()
        with col_n:
            if st.button("Ke Ringkasan Akhir ➡️ "):
                next_step()
                st.rerun()

    # ==============================
    # WIZARD: STEP 4 (REVIEW & SUBMIT)
    # ==============================
    elif st.session_state.step == 4:
        st.markdown("### Tahap 4: Tinjauan Akhir & Analisis")
        
        is_ready = progress >= 1.0

        if not is_ready:
            st.warning("⚠️ Masih ada data yang belum lengkap pada tahap-tahap sebelumnya. Harap lengkapi kuis hingga progress mencapai 100%.")
            if st.button("⬅️ Kembali untuk Melengkapi Isian"):
                prev_step()
                st.rerun()
        else:
            st.success("Seluruh input telah dikumpulkan. Silakan panggil mesin ML untuk melihat hasilnya.")
            
            with st.expander("📝 Tampilkan Rangkuman Jawaban Saya", expanded=False):
                summary_df = pd.DataFrame(
                    list(st.session_state.form_data.items()), 
                    columns=["Parameter", "Jawaban"]
                )
                st.table(summary_df)

            st.write("")
            col_b, col_n = st.columns([2, 5])
            with col_b:
                if st.button("⬅️ Revisi Data"):
                    prev_step()
                    st.rerun()
            with col_n:
                submit = st.button("🔮 Evaluasi Prediksi Attrition Sekarang", use_container_width=True)
            
            if submit:
                # Preprocessing
                form_payload = st.session_state.form_data.copy()
                form_payload['EnvironmentSatisfaction'] = int(form_payload['EnvironmentSatisfaction'].split(" ")[0])
                form_payload['JobSatisfaction'] = int(form_payload['JobSatisfaction'].split(" ")[0])
                form_payload['JobInvolvement'] = int(form_payload['JobInvolvement'].split(" ")[0])
                form_payload['WorkLifeBalance'] = int(form_payload['WorkLifeBalance'].split(" ")[0])

                status_box = st.status("🛸 Menginisialisasi sistem prediksi...", expanded=True)
                time.sleep(0.6)
                status_box.write("📥 Memuat model Logistic Regression & MLflow Artifacts...")
                time.sleep(0.8)
                status_box.write("⚙️ Melakukan preprocessing data kuis...")
                time.sleep(0.7)
                status_box.write("🧠 Menghitung probabilitas (Confidence Score) Attrition...")
                time.sleep(0.5)
                status_box.update(label="✅ Analisa Selesai!", state="complete", expanded=False)

                result = predict_single_data(form_payload)
                
                if "error" in result:
                    st.error(f"❌ Kesalahan sistem: {result['error']}")
                else:
                    is_resign = "RESIGN" in result['prediction']
                    if is_resign: st.snow()
                    else: st.balloons()

                    st.markdown(f"""
                    <div class="result-box fade-in" style="background: rgba(30, 41, 59, 0.8); border: 2px solid {'#f59e0b' if is_resign else '#10b981'}; border-radius: 16px; padding: 2rem; margin-top: 1.5rem;">
                        <h2 style="margin-top:0; color: {'#f59e0b' if is_resign else '#10b981'};">Hasil Analisa Attrition</h2>
                        <div style="display: flex; gap: 2rem; align-items: center;">
                            <div style="flex: 1;">
                                <p style="font-size: 1.1rem; color: #f8fafc; line-height: 1.6;">
                                    Berdasarkan profil input, sistem memprediksi bahwa: <br>
                                    <span style="font-size: 1.8rem; font-weight: 700; color: white;">{result['prediction']}</span>
                                </p>
                                <hr style="border-color: rgba(255,255,255,0.1);">
                                <p style="color: #a8b2d1;">
                                    {'Karyawan ini memiliki probabilitas besar untuk keluar (Resign). Sangat disarankan untuk segera menjadwalkan <i>One-on-one session</i> agar potensi masalah dapat dimitigasi sejak dini.' if is_resign else 'Karyawan menunjukkan probabilitas loyalitas yang solid terhadap kondisi pekerjaannya saat ini. Tidak ada kebutuhan intervensi langsung yang mendesak bagi divisi HR.'}
                                </p>
                            </div>
                            <div style="text-align: center; background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                                <span style="display: block; color: #a8b2d1; font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase;">Confidence Score</span>
                                <span style="font-size: 2.5rem; font-weight: 700; color: {'#f59e0b' if is_resign else '#10b981'};">{result['confidence']}</span>
                            </div>
                        </div>
                        <div style="margin-top: 1.5rem;">
                            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden;">
                                <div style="width: {result['confidence']}; background: {'linear-gradient(90deg, #f59e0b, #ef4444)' if is_resign else 'linear-gradient(90deg, #10b981, #34d399)'}; height: 100%;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
