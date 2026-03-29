from flask import Flask, render_template, request
from model.modeling import predict_single_data, get_dashboard_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    data = get_dashboard_data()
    return render_template("dashboard.html", data=data)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None
    if request.method == "POST":
        # Ambil data dari form input 
        # (Top 10 features yang digunakan dalam script modeling.py)
        # Type casting angka harus dilakukan agar input cocok untuk dataframe
        try:
            input_data = {
                'OverTime': request.form.get("OverTime"),
                'BusinessTravel': request.form.get("BusinessTravel"),
                'MaritalStatus': request.form.get("MaritalStatus"),
                'JobRole': request.form.get("JobRole"),
                'EnvironmentSatisfaction': int(request.form.get("EnvironmentSatisfaction") or 0),
                'JobSatisfaction': int(request.form.get("JobSatisfaction") or 0),
                'JobInvolvement': int(request.form.get("JobInvolvement") or 0),
                'WorkLifeBalance': int(request.form.get("WorkLifeBalance") or 0),
                'EducationField': request.form.get("EducationField"),
                'DistanceFromHome': int(request.form.get("DistanceFromHome") or 0),
            }
            
            # Panggil logic prediksi
            result = predict_single_data(input_data)
        except Exception as e:
            result = {"error": f"Kesalahan parsing input data: {str(e)}"}

    return render_template("form_prediction.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
