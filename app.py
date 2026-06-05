import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Set page configuration for a professional look
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for custom styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    h1 { color: #1e293b; font-family: 'Helvetica Neue', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Load the trained KNN model safely
@st.cache_resource
def load_model():
    try:
        with open('KNN_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Error: 'KNN_model.pkl' file not found. Please ensure it is in the same directory.")
        return None

model = load_model()

# Header layout
st.title("🛡️ FraudShield AI Detection Dashboard")
st.markdown("Enter transaction attributes below to evaluate the likelihood of fraudulent activity.")
st.write("---")

# Organized layout using columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💳 Transaction Info")
    transaction_amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=0.01, value=50.0)
    num_items = st.number_input("Number of Items Purchased", min_value=1, step=1, value=1)
    velocity_score = st.number_input("Velocity Score (Tx frequency metric)", min_value=0.0, step=0.1, value=1.0)

with col2:
    st.subheader("👤 Customer & History")
    customer_age = st.number_input("Customer Age", min_value=0, max_value=120, step=1, value=30)
    prev_transactions = st.number_input("Previous Successful Transactions", min_value=0, step=1, value=5)
    distance_from_home = st.number_input("Distance from Home (miles)", min_value=0.0, step=0.1, value=2.5)

with col3:
    st.subheader("🌐 Context & Device")
    hour_of_day = st.slider("Hour of Day", min_value=0, max_value=23, value=12)
    
    # Categorical/Binary features converted visually into select boxes
    is_weekend = st.selectbox("Is Weekend?", ["No", "Yes"])
    is_first_transaction = st.selectbox("Is First Transaction?", ["No", "Yes"])
    
    # Placeholders for encoded values (adjust choices if your original dataset mapping differs)
    device_type = st.number_input("Device Type (Encoded)", min_value=0, step=1, value=0)
    network_quality = st.number_input("Network Quality (Encoded)", min_value=0, step=1, value=0)
    store_type = st.number_input("Store Type (Encoded)", min_value=0, step=1, value=0)

st.write("---")

# Predict button
if st.button("🚨 Analyze Transaction"):
    if model is not None:
        # Convert user inputs to numerical mappings corresponding to model format
        is_weekend_val = 1 if is_weekend == "Yes" else 0
        is_first_transaction_val = 1 if is_first_transaction == "Yes" else 0
        
        # Mapping inputs to matches feature array columns:
        # ['transaction_amount', 'hour_of_day', 'is_weekend', 'num_items', 'customer_age', 
        #  'prev_transactions', 'distance_from_home', 'device_type', 'network_quality', 
        #  'is_first_transaction', 'store_type', 'velocity_score']
        input_data = pd.DataFrame([[
            transaction_amount, hour_of_day, is_weekend_val, num_items, customer_age,
            prev_transactions, distance_from_home, device_type, network_quality,
            is_first_transaction_val, store_type, velocity_score
        ]], columns=[
            'transaction_amount', 'hour_of_day', 'is_weekend', 'num_items', 'customer_age',
            'prev_transactions', 'distance_from_home', 'device_type', 'network_quality',
            'is_first_transaction', 'store_type', 'velocity_score'
        ])
        
        # Run prediction
        prediction = model.predict(input_data)[0]
        
        # Display Results Beautifully
        st.subheader("🔍 Analysis Result:")
        if prediction == 1:
            st.error("### ⚠️ ALERT: High Risk of Fraud Detected!")
            st.write("This transaction mirrors patterns historically associated with fraudulent activities. Consider flagging for internal manual review.")
        else:
            st.success("### ✅ Clear: Transaction Appears Safe.")
            st.write("The transaction features fall comfortably into standard consumer behavior metrics.")
