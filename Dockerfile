# Gunakan base image Python 3.10 versi ringan (slim)
FROM python:3.10-slim

# Set working directory di dalam container
WORKDIR /app

# Install system dependencies (jika diperlukan oleh pandas/scikit-learn)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements terlebih dahulu untuk memanfaatkan Docker cache layer
COPY requirements.txt .

# Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code project ke dalam container
COPY . .

# Beri tahu Docker bahwa aplikasi ini berjalan di port 8501 (Streamlit Default)
EXPOSE 8501

# Non-aktifkan buffer log agar print() Python langsung ter-record di Docker logs
ENV PYTHONUNBUFFERED=1

# Perintah yang dijalankan ketika container hidup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
