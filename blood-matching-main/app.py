import streamlit as st
import pandas as pd
import joblib

# Function to parse CSV files
def parse_csv(filepath):
    with open(filepath, 'r') as file:
        content = file.read().strip()

    # Split lines and handle potential quote issues
    lines = content.replace('"', '').split('\n')

    # First line is headers
    headers = [header.strip().lower() for header in lines[0].split(',')]  # Normalize headers

    # Prepare data
    data = [line.split(',') for line in lines[1:]]

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

# Load the saved model
model = joblib.load('donor_matching_model (2).pkl')

# Function to check blood group compatibility
def is_compatible(donor_blood, recipient_blood):
    d = donor_blood.upper().replace('VE','')
    r = recipient_blood.upper().replace('VE','')

    if d == "O-":
        return True
    if d == r:
        return True
    if d == "O+" and "+" in r:
        return True

    return False

# Function to recommend donors
def recommend_donors(recipient, donors_df, model, top_n=3):
    features = []
    donor_names = []

    for _, donor in donors_df.iterrows():
        try:
            feature = [
                1 if is_compatible(donor['blood group'], recipient['blood group needed']) else 0,
                abs(float(donor['age']) - float(recipient['age'])) if 'age' in donor.keys() and 'age' in recipient.keys() else 0,
                1 if donor['location'].lower() == recipient['location'].lower() else 0,
                float(donor['number of times donated']) if 'number of times donated' in donor.keys() else 0,
                float(recipient['urgency']) if 'urgency' in recipient.keys() else 0
            ]

            features.append(feature)
            donor_names.append(donor['name'])
        except KeyError as e:
            st.error(f"Error: Column '{e.args[0]}' not found in the donor dataset. Please check the CSV file.")
            return []

    # Predict probabilities
    probabilities = model.predict_proba(features)[:, 1]

    # Rank donors
    ranked_donors = sorted(
        zip(donor_names, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_donors[:top_n]

# Streamlit UI
st.set_page_config(page_title="Blood Donor Matching System", page_icon="🩸", layout="centered")

# Title and description
st.title("🩸 Blood Donor Matching System")
st.markdown("""
    Welcome to the **Blood Donor Matching System**! This app helps you find compatible blood donors based on your requirements.
    Enter the recipient details in the sidebar and click **Find Donors** to get recommendations.
""")

# Load donor data
try:
    donors_df = parse_csv('donor.csv')
except Exception as e:
    st.error(f"Error loading donor data: {e}")
    st.stop()

# Sidebar for recipient details
st.sidebar.header("Recipient Details")
recipient_name = st.sidebar.text_input("Recipient Name")
blood_group_needed = st.sidebar.selectbox("Blood Group Needed", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
age = st.sidebar.number_input("Age", min_value=0, max_value=100)
location = st.sidebar.text_input("Location")
urgency = st.sidebar.number_input("Urgency Level (1-10)", min_value=1, max_value=10)

# Create recipient dictionary
recipient = {
    'name': recipient_name,
    'blood group needed': blood_group_needed,
    'age': age,
    'location': location,
    'urgency': urgency
}

# Recommend donors
if st.sidebar.button("Find Donors"):
    with st.spinner("Finding the best donors..."):  # Show a loading spinner
        top_donors = recommend_donors(recipient, donors_df, model)
        if top_donors:
            st.success("Donors found! Here are the top matches:")
            st.subheader(f"Top Donors for {recipient_name}:")
            for donor, score in top_donors:
                st.markdown(f"""
                    **Donor Name:** {donor}  
                    **Match Score:** {score:.2f}  
                    ---
                """)
        else:
            st.warning("No donors found. Please check the input data.")