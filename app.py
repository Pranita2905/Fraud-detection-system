from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load Model
with open("KNN_model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        features = pd.DataFrame({
            'transaction_amount': [float(request.form['transaction_amount'])],
            'hour_of_day': [float(request.form['hour_of_day'])],
            'is_weekend': [float(request.form['is_weekend'])],
            'num_items': [float(request.form['num_items'])],
            'customer_age': [float(request.form['customer_age'])],
            'prev_transactions': [float(request.form['prev_transactions'])],
            'distance_from_home': [float(request.form['distance_from_home'])],
            'device_type': [float(request.form['device_type'])],
            'network_quality': [float(request.form['network_quality'])],
            'is_first_transaction': [float(request.form['is_first_transaction'])],
            'store_type': [float(request.form['store_type'])],
            'velocity_score': [float(request.form['velocity_score'])]
        })

        prediction = model.predict(features)[0]

        if prediction == 1:
            result = "⚠️ Fraudulent Transaction Detected"
        else:
            result = "✅ Legitimate Transaction"

        return render_template(
            "index.html",
            prediction_text=result
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {e}"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
