@echo off
title PredictApp Startup
echo Menjalankan layanan Flask Web Server dan MLflow UI...
echo ====================================================

:: Cek apakah folder virtual environment ('env') tersedia
if not exist "env\Scripts\activate" (
    echo Error: Folder 'env' tidak ditemukan. Harap buat virtual environment terlebih dahulu!
    pause
    exit
)

:: Menjalankan MLflow UI di background window
echo [->] Menyalakan Server MLflow di port 5001 (Jendela Baru)...
start "MLflow UI (Port 5001)" cmd /c ".\env\Scripts\activate && cd "%cd%" && mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001"

:: Menjalankan Streamlit Application di window saat ini
echo [->] Menyalakan Server Streamlit App di port 8501...
call .\env\Scripts\activate
streamlit run app.py

pause
