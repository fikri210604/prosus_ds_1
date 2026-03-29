import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Tentukan path untuk menyimpan model
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, 'attrition_model.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.joblib')
ENCODER_PATH = os.path.join(MODEL_DIR, 'encoders.joblib')

# Top 10 Fitur Paling Berpengaruh berdasarkan Analisis Notebook
TOP_FEATURES = [
    'OverTime', 
    'BusinessTravel', 
    'MaritalStatus', 
    'JobRole', 
    'EnvironmentSatisfaction', 
    'JobSatisfaction', 
    'JobInvolvement', 
    'WorkLifeBalance', 
    'EducationField', 
    'DistanceFromHome'
]

def train_model():
    """
    Melatih model Logistic Regression untuk Employee Attrition menggunakan top 10 features, 
    serta tracking performa ke MLflow.
    """
    print("Mulai mengambil data...")
    # Load dataset
    df = pd.read_csv("https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/employee/employee_data.csv")
    df.dropna(inplace=True)

    # Hapus fitur dengan nilai konstan/berulang (jaga-jaga jika masih ada dalam filter kita)
    kolom_konstan = [col for col in df.columns if df[col].nunique() == 1]
    kolom_berulang = [col for col in df.columns if df[col].nunique() == len(df)]
    df.drop(columns=kolom_konstan + kolom_berulang, inplace=True, errors='ignore')

    # Siapkan X dan Y
    X = df[TOP_FEATURES]
    y = df['Attrition']

    # Identifikasi kolom kategorikal
    cat_cols = X.select_dtypes(include=['object']).columns

    # Inisialisasi encoder dictionary untuk menyimpan setiap kolom cat_cols
    encoders = {}

    for col in cat_cols:
        le = LabelEncoder()
        X.loc[:, col] = le.fit_transform(X[col])
        encoders[col] = le

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scaller
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # --- MLFLOW INTEGRATION ---
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Employee_Attrition_Prediction")

    with mlflow.start_run():
        print("Sedang melatih model Logistic Regression...")
        # Train model
        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train, y_train)

        # Prediksi
        y_pred = lr.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        # MLflow Logging
        mlflow.log_param("max_iter", 1000)
        mlflow.log_param("features", TOP_FEATURES)
        mlflow.log_metric("accuracy", acc)
        
        # Log model ke MLflow
        mlflow.sklearn.log_model(lr, "logistic_regression_model")

        print(f"Akurasi Model: {acc:.4f}")
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

        # Simpan artifact secara lokal
        joblib.dump(lr, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        joblib.dump(encoders, ENCODER_PATH)

        print(f"Model, scaler, dan encoder berhasil disimpan ke folder {MODEL_DIR}")


def load_model_artifacts():
    """
    Memuat model, scaler, dan encoders dari disk.
    """
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(ENCODER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoders = joblib.load(ENCODER_PATH)
        return model, scaler, encoders
    return None, None, None


def predict_single_data(input_data):
    """
    Melakukan prediksi terhadap data baru.
    input_data harus berupa dictionary dengan keys sesuai TOP_FEATURES.
    """
    model, scaler, encoders = load_model_artifacts()
    
    if not model or not scaler or not encoders:
        return {"error": "Model artifact tidak ditemukan. Silakan jalankan training terlebih dahulu."}

    try:
        # Konversi dictionary ke DataFrame satuan
        df_input = pd.DataFrame([input_data])

        # Pastikan kolom sesuai urutan fitur model
        df_input = df_input[TOP_FEATURES]

        # Encoding: loop pada dictionary encoder untuk memproses kolom kategorikal
        for col, le in encoders.items():
            if col in df_input.columns:
                # Menghindari error unseen label dengan mencoba memetakan ke label pertama jika tak dikenali
                df_input[col] = df_input[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                df_input[col] = le.transform(df_input[col])

        # Scaling
        X_scaled = scaler.transform(df_input)

        # Prediksi (0 -> Tetap, 1 -> Resign atau 'No'/'Yes')
        pred = model.predict(X_scaled)[0]
        
        # Dapatkan index untuk numpy probability array
        classes = list(model.classes_)
        pred_idx = classes.index(pred)
        
        prob = model.predict_proba(X_scaled)[0][pred_idx]

        if pred == 'Yes' or pred == 1:
            hasil = "Karyawan kemungkinan besar akan RESIGN."
        else:
            hasil = "Karyawan kemungkinan besar akan BERTAHAN."

        return {
            "prediction": hasil,
            "confidence": f"{prob * 100:.2f}%"
        }

    except Exception as e:
        return {"error": str(e)}

def get_dashboard_data():
    """
    Mengambil dan memproses data dari dataset untuk ditampilkan di dashboard.
    Mengembalikan dictionary berisi data agregasi untuk Chart.js dan metric cards.
    """
    try:
        # Load dataset asli
        df = pd.read_csv("https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/employee/employee_data.csv")
        df.dropna(inplace=True)
        
        # --- 1. Summary Metrics ---
        total_employees = len(df)
        attrition_yes = len(df[df['Attrition'] == 1])
        attrition_rate = round((attrition_yes / total_employees) * 100, 2) if total_employees > 0 else 0
        
        metrics = {
            "total_employees": total_employees,
            "attrition_count": attrition_yes,
            "attrition_rate": attrition_rate
        }
        
        # --- 2. Data Chart 1: Attrition by Department (Pie) ---
        dept_attr = df[df['Attrition'] == 1]['Department'].value_counts()
        chart_dept = {
            "labels": dept_attr.index.tolist(),
            "data": dept_attr.values.tolist()
        }
        
        # --- 3. Data Chart 2: Attrition by Job Role (Bar) ---
        role_attr = df[df['Attrition'] == 1]['JobRole'].value_counts()
        chart_role = {
            "labels": role_attr.index.tolist(),
            "data": role_attr.values.tolist()
        }
        
        # --- 4. Data Chart 3: Avg Income by Attrition (Bar) ---
        income_attr = df.groupby('Attrition')['MonthlyIncome'].mean().round(2)
        # Mapping 0 -> 'Tetap', 1 -> 'Resign'
        labels = ["Tetap" if x == 0 else "Resign" for x in income_attr.index]
        chart_income = {
            "labels": labels,
            "data": income_attr.values.tolist()
        }
        
        return {
            "metrics": metrics,
            "chart_dept": chart_dept,
            "chart_role": chart_role,
            "chart_income": chart_income
        }
    except Exception as e:
        print(f"Error loading dashboard data: {e}")
        return None

if __name__ == "__main__":
    train_model()
