# 🛡️ Fraud Guard AI - Transaction Fraud Detection System

## 📌 Overview

Fraud Guard AI is a Machine Learning-powered web application that analyzes transaction details and predicts whether a transaction is fraudulent or legitimate.

The application uses a trained K-Nearest Neighbors (KNN) classification model to evaluate transaction risk based on multiple behavioral and transactional features.

---

## 🚀 Live Demo

🌐 Live Application:
https://fraud-detection-system-bts4.onrender.com

Try the Fraud Guard AI system to analyze transaction risk and detect potential fraudulent activities in real time.

---

## 🎯 Problem Statement

Online transactions are increasing rapidly, making fraud detection a critical challenge for businesses and financial institutions.

This project helps identify potentially fraudulent transactions by analyzing transaction patterns and customer behavior using Machine Learning.

---

## ✨ Features

* Real-time Fraud Detection
* Interactive Web Interface
* KNN Classification Model
* Fraud Risk Assessment
* Confidence Probability Score
* Modern Bootstrap 5 UI
* Fast Prediction Response

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Backend

* Flask

### Machine Learning

* Scikit-Learn
* K-Nearest Neighbors (KNN)

### Data Processing

* Pandas
* NumPy

### Deployment

* Gunicorn
* Render / Railway / PythonAnywhere

---

## 📊 Input Features

The model evaluates the following transaction attributes:

| Feature               | Description                      |
| --------------------- | -------------------------------- |
| Transaction Amount    | Transaction value                |
| Hour of Day           | Time of transaction              |
| Is Weekend            | Weekend transaction indicator    |
| Number of Items       | Number of purchased items        |
| Customer Age          | Age of customer                  |
| Previous Transactions | Historical transaction count     |
| Distance From Home    | Distance from registered address |
| Device Type           | Encoded device identifier        |
| Network Quality       | Network trust score              |
| Is First Transaction  | New customer indicator           |
| Store Type            | Encoded merchant category        |
| Velocity Score        | Transaction frequency score      |

---

## 🤖 Machine Learning Model

### Algorithm Used

K-Nearest Neighbors (KNN) Classifier

### Why KNN?

* Simple and effective
* Non-parametric algorithm
* Suitable for classification problems
* Works well with pattern recognition

---

## 📂 Project Structure

```bash
Fraud-Detection-System/
│
├── app.py
├── KNN_model.pkl
├── requirements.txt
├── README.md
│
└── static/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/fraud-detection-system.git
```

```bash
cd fraud-detection-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
python app.py
```

Application will start at:

```text
http://127.0.0.1:5000
```

---

## 📦 Requirements

```txt
Flask
pandas
numpy
scikit-learn
gunicorn
```

---

## 📈 Prediction Output

### Legitimate Transaction

```text
✅ TRANSACTION APPROVED
Low risk evaluation. Safe to proceed with settlement.
```

### Fraudulent Transaction

```text
🚨 HIGH RISK DETECTED
This transaction aligns closely with signature fraudulent patterns.
```

---

## 📊 Model Workflow

1. Data Collection
2. Data Cleaning
3. Feature Engineering
4. Exploratory Data Analysis (EDA)
5. Model Training
6. KNN Classification
7. Model Evaluation
8. Model Serialization (Pickle)
9. Flask Deployment

---

## 🔮 Future Enhancements

* Random Forest Model
* XGBoost Integration
* Deep Learning Fraud Detection
* Real-Time Transaction Streaming
* Fraud Analytics Dashboard
* API Integration
* Cloud Deployment

---

## 👩‍💻 Author

Pranita Mothe
Data Analyst | Machine Learning Enthusiast
Email: mothepranita@gmail.com

