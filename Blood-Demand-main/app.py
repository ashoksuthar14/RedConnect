import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the saved model
model = joblib.load("blood_demand_model.pkl")

# Streamlit UI
st.set_page_config(page_title="Blood Demand Prediction System", page_icon="🩸", layout="wide")

# Title and description
st.title("🩸 Blood Demand Prediction System")
st.markdown("""
    Welcome to the **Blood Demand Prediction System**! This app helps medical institutions forecast their monthly blood demand based on various factors.
    Enter the details in the sidebar and click **Predict** to get the blood demand forecast.
""")

# Sidebar for input features
st.sidebar.header("Input Features")

# Input fields
hospital_size = st.sidebar.selectbox("Hospital Size", ["Small", "Medium", "Large"])
region = st.sidebar.selectbox("Region", ["North", "South", "East", "West"])
department = st.sidebar.selectbox("Department", ["Surgery", "Emergency", "ICU", "Oncology", "Pediatrics"])
blood_type = st.sidebar.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
blood_product = st.sidebar.selectbox("Blood Product", ["Red Blood Cells", "Platelets", "Plasma"])
month = st.sidebar.number_input("Month", min_value=1, max_value=12)
antibody_screens = st.sidebar.number_input("Antibody Screens", min_value=0)
historical_donations = st.sidebar.number_input("Historical Donations", min_value=0)
historical_transfusions = st.sidebar.number_input("Historical Transfusions", min_value=0)
holiday = st.sidebar.selectbox("Holiday Month?", [0, 1])
disease_outbreak = st.sidebar.selectbox("Disease Outbreak?", [0, 1])

# Create input DataFrame
input_data = pd.DataFrame({
    "Hospital_Size": [hospital_size],
    "Region": [region],
    "Department": [department],
    "Blood_Type": [blood_type],
    "Blood_Product": [blood_product],
    "Month": [month],
    "Antibody_Screens": [antibody_screens],
    "Historical_Donations": [historical_donations],
    "Historical_Transfusions": [historical_transfusions],
    "Holiday": [holiday],
    "Disease_Outbreak": [disease_outbreak],
})

# Predict
if st.sidebar.button("Predict"):
    # Make prediction
    prediction = model.predict(input_data)

    # Display prediction
    st.subheader("Predicted Blood Demand")
    st.success(f"**{prediction[0]:.2f} units**")

    # Confidence interval (example: ±10%)
    confidence_interval = prediction[0] * 0.10
    st.write(f"**Confidence Interval:** {prediction[0] - confidence_interval:.2f} to {prediction[0] + confidence_interval:.2f} units")

    # Display input data summary
    st.subheader("Input Data Summary")
    st.write(input_data)

    # Feature importance (if using Random Forest)
    if hasattr(model.named_steps["regressor"], "feature_importances_"):
        st.subheader("Feature Importance")
        feature_importance = model.named_steps["regressor"].feature_importances_
        feature_names = model.named_steps["preprocessor"].get_feature_names_out()
        importance_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importance})
        importance_df = importance_df.sort_values(by="Importance", ascending=False)

        # Plot feature importance
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax)
        ax.set_title("Feature Importance")
        st.pyplot(fig)

    # Historical trends (example visualization)
    st.subheader("Historical Trends")
    st.markdown("""
        Below is an example visualization of historical blood demand trends. You can replace this with actual historical data from your institution.
    """)
    historical_data = pd.DataFrame({
        "Month": range(1, 13),
        "Blood_Demand": np.random.randint(100, 500, size=12),  # Replace with real data
    })
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="Month", y="Blood_Demand", data=historical_data, marker="o", ax=ax)
    ax.set_title("Monthly Blood Demand Trends")
    ax.set_xlabel("Month")
    ax.set_ylabel("Blood Demand (units)")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("""
    **Note:** This is a predictive model and should be used as a guide. Actual blood demand may vary based on unforeseen factors.
""")