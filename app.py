from flask import Flask, request, render_template_string
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained KNN model
with open("KNN_model.pkl", "rb") as file:
    model = pickle.load(file)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Fraud Detection System</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background: #f5f7fa;
            margin: 0;
            padding: 0;
        }

        .container{
            max-width: 800px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
        }

        h1{
            text-align:center;
            color:#1f4e79;
        }

        .row{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:15px;
        }

        input{
            padding:10px;
            width:100%;
            border:1px solid #ccc;
            border-radius:8px;
        }

        button{
            width:100%;
            padding:12px;
            background:#1f4e79;
            color:white;
            border:none;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
            margin-top:15px;
        }

        button:hover{
            background:#163b5c;
        }

        .result{
            margin-top:20px;
            text-align:center;
            font-size:22px;
            font-weight:bold;
        }

        .fraud{
            color:red;
        }

        .safe{
            color:green;
        }
    </style>
</head>

<body>

<div class="container">

<h1>Fraud Detection System</h1>

<form method="POST">

<div class="row">

<input type="number" step="any" name="transaction_amount" placeholder="Transaction Amount" required>

<input type="number" step="any" name="hour_of_day" placeholder="Hour Of Day" required>

<input type="number" step="any" name="is_weekend" placeholder="Is Weekend (0/1)" required>

<input type="number" step="any" name="num_items" placeholder="Number Of Items" required>

<input type="number" step="any" name="customer_age" placeholder="Customer Age" required>

<input type="number" step="any" name="prev_transactions" placeholder="Previous Transactions" required>

<input type="number" step="any" name="distance_from_home" placeholder="Distance From Home" required>

<input type="number" step="any" name="device_type" placeholder="Device Type" required>

<input type="number" step="any" name="network_quality" placeholder="Network Quality" required>

<input type="number" step="any" name="is_first_transaction" placeholder="First Transaction (0/1)" required>

<input type="number" step="any" name="store_type" placeholder="Store Type" required>

<input type="number" step="any" name="velocity_score" placeholder="Velocity Score" required>

</div>

<button type="submit">Predict Fraud</button>

</form>

{% if prediction %}
<div class="result {{ css_class }}">
    {{ prediction }}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    css_class = ""

    if request.method == "POST":
        try:

            data = pd.DataFrame({
                'transaction_amount':[float(request.form['transaction_amount'])],
                'hour_of_day':[float(request.form['hour_of_day'])],
                'is_weekend':[float(request.form['is_weekend'])],
                'num_items':[float(request.form['num_items'])],
                'customer_age':[float(request.form['customer_age'])],
                'prev_transactions':[float(request.form['prev_transactions'])],
                'distance_from_home':[float(request.form['distance_from_home'])],
                'device_type':[float(request.form['device_type'])],
                'network_quality':[float(request.form['network_quality'])],
                'is_first_transaction':[float(request.form['is_first_transaction'])],
                'store_type':[float(request.form['store_type'])],
                'velocity_score':[float(request.form['velocity_score'])]
            })

            result = model.predict(data)[0]

            if result == 1:
                prediction = "⚠ Fraudulent Transaction Detected"
                css_class = "fraud"
            else:
                prediction = "✅ Legitimate Transaction"
                css_class = "safe"

        except Exception as e:
            prediction = f"Error: {str(e)}"
            css_class = "fraud"

    return render_template_string(
        HTML,
        prediction=prediction,
        css_class=css_class
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
