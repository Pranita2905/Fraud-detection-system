import streamlit as nn
import pandas as pd
import numpy as np
import pickle

# Set page configurations
st.set_page_config(
    page_title="Fraud Guard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a highly attractive and modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #2a5298;
    }
    .fraud-alert {
        background-color: #ffeef0;
        border: 2px solid #ff4d4d;
        color: #990000;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .safe-alert {
        background-color: #e6f9ed;
        border: 2px solid #2ecc71;
        color: #196634;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Load the trained KNN model safely
@st.cache_resource
def load_model():
    with open('KNN_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model. Make sure 'KNN_model.pkl' is in the same directory. Details: {e}")
    st.stop()

# Header banner
st.markdown("""
    <div class="header-box">
        <h1>🛡️ Fraud Guard AI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Real-time Transaction Fraud Risk Assessment Engine</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar layout for user input features
st.sidebar.header("📥 Transaction Features")
st.sidebar.markdown("Provide details below to test fraud probability:")

# Input fields grouped nicely in the sidebar
transaction_amount = st.sidebar.number_input("Transaction Amount ($)", min_value=0.0, value=150.0, step=5.0)
hour_of_day = st.sidebar.slider("Hour of Day (0-23)", 0, 23, 14)
customer_age = st.sidebar.number_input("Customer Age", min_value=18, max_value=100, value=35)
num_items = st.sidebar.slider("Number of Items Purchased", 1, 20, 2)
prev_transactions = st.sidebar.number_input("Previous Transactions Count", min_value=0, value=5)
distance_from_home = st.sidebar.number_input("Distance from Home (miles)", min_value=0.0, value=12.5, step=1.0)
velocity_score = st.sidebar.slider("Velocity Score (frequency of transactions)", 0.0, 10.0, 1.2, step=0.1)

st.sidebar.markdown("---")
# Categorical / Binary inputs converted into numerical values matching your model's structure
is_weekend = st.sidebar.selectbox("Is Weekend?", ["No", "Yes"])
is_weekend_val = 1 if is_weekend == "Yes" else 0

is_first_transaction = st.sidebar.selectbox("Is First Transaction?", ["No", "Yes"])
is_first_transaction_val = 1 if is_first_transaction == "Yes" else 0

# Adjust selection boundaries if your model expects explicit dummy/encoded integers
device_type = st.sidebar.number_input("Device Type ID (encoded)", min_value=0, max_value=10, value=1)
network_quality = st.sidebar.number_input("Network Quality Rating (encoded)", min_value=0, max_value=5, value=3)
store_type = st.sidebar.number_input("Store Type ID (encoded)", min_value=0, max_value=10, value=2)


# Main section layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Current Evaluation Overview")
    
    # Showcase metrics beautifully
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"<div class='metric-card'><small>Amount</small><br><b>${transaction_amount:,.2f}</b></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-card'><small>Distance</small><br><b>{distance_from_home} miles</b></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-card'><small>Velocity Index</small><br><b>{velocity_score}</b></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process Inputs into the exact feature order requested
    input_data = pd.DataFrame([{
        'transaction_amount': transaction_amount,
        'hour_of_day': hour_of_day,
        'is_weekend': is_weekend_val,
        'num_items': num_items,
        'customer_age': customer_age,
        'prev_transactions': prev_transactions,
        'distance_from_home': distance_from_home,
        'device_type': device_type,
        'network_quality': network_quality,
        'is_first_transaction': is_first_transaction_val,
        'store_type': store_type,
        'velocity_score': velocity_score
    }])
    
    st.markdown("##### Input Payload Sent to KNN Model")
    st.dataframe(input_data, use_container_width=True)

with col2:
    st.subheader("🔍 Prediction Results")
    st.write("Click 'Analyze Transaction' to prompt the evaluation model.")
    
    if st.button("🚀 Analyze Transaction", use_container_width=True):
        # Predict class
        prediction = model.predict(input_data)[0]
        
        # Check if the model supports prediction probability
        has_proba = hasattr(model, "predict_proba")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if prediction == 1:
            st.markdown("""
                <div class="fraud-alert">
                    🚨 HIGH RISK DETECTED<br>
                    <span style="font-size: 14px; font-weight: normal;">This transaction aligns heavily with known fraudulent patterns.</span>
                </div>
            """, unsafe_allow_html=True)
            if has_proba:
                prob = model.predict_proba(input_data)[0][1] * 100
                st.error(f"Model Confidence: **{prob:.2f}% Probability of Fraud**")
        else:
            st.markdown("""
                <div class="safe-alert">
                    ✅ TRANSACTION APPROVED<br>
                    <span style="font-size: 14px; font-weight: normal;">Low risk assessment. Safe to proceed.</span>
                </div>
            """, unsafe_allow_html=True)
            if has_proba:
                prob = model.predict_proba(input_data)[0][0] * 100
                st.success(f"Model Confidence: **{prob:.2f}% Probability of Legitimacy**")
