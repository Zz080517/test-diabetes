from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("diabetes_model.pkl")  # 加载模型

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json  # 获取用户输入
    features = [[float(data["Age"]), float(data["BMI"]), float(data["Glucose"])]]
    prediction = model.predict(features)
    result = "可能有糖尿病" if prediction[0] == 1 else "可能没有糖尿病"
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)