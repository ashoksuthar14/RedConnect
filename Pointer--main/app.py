import streamlit as st
import pandas as pd
import hashlib
import datetime

# Blockchain Simulation (Simple Implementation)
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", datetime.datetime.now(), "Genesis Block", calculate_hash(0, "0", datetime.datetime.now(), "Genesis Block"))

def add_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Initialize blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Points and Badges System
def calculate_points(donation_date):
    today = datetime.datetime.now()
    donation_date = datetime.datetime.strptime(donation_date, "%Y-%m-%d")
    days_since_last_donation = (today - donation_date).days
    if days_since_last_donation < 365:
        return 100
    return 50

def assign_badge(points):
    if points >= 500:
        return "Gold Donor 🥇"
    elif points >= 300:
        return "Silver Donor 🥈"
    elif points >= 100:
        return "Bronze Donor 🥉"
    return "New Donor 🩸"

# Streamlit App
st.set_page_config(page_title="Blood Donor Rewards", page_icon="💉", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    /* General Styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff1c1c;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #ddd;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ff4b4b;
    }
    /* Card Styling */
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    /* Badge and Points Styling */
    .badge {
        font-size: 20px;
        font-weight: bold;
        color: #ff4b4b;
    }
    .points {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    /* Text Color */
    .stMarkdown p, .stMarkdown li {
        color: #333333;
    }
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .fadeIn {
        animation: fadeIn 1s ease-in;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("Blood Donor Rewards System 🩸")
st.write("""
    Welcome to the Blood Donor Rewards System! Donate blood, earn points, and get badges to unlock discounts on medicines and hospital visits.
    Your data is securely stored using blockchain technology.
""")

# Input Form
with st.form("donor_form"):
    st.subheader("Donor Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=100)
    blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    donation_date = st.date_input("Last Donation Date")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if name and age and blood_type and donation_date:
        # Calculate Points and Badges
        points = calculate_points(str(donation_date))
        badge = assign_badge(points)

        # Save Data to Blockchain
        donor_data = {
            "name": name,
            "age": age,
            "blood_type": blood_type,
            "donation_date": str(donation_date),
            "points": points,
            "badge": badge,
            "user_id": hashlib.sha256(name.encode('utf-8')).hexdigest()[:10]
        }
        new_block = add_block(previous_block, donor_data)
        blockchain.append(new_block)
        previous_block = new_block

        # Display Results in a Card
        st.success("Thank you for your donation! Your data has been securely recorded.")
        st.markdown(f"""
            <div class="card fadeIn">
                <h2>Your Donor Profile</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Age:</strong> {age}</p>
                <p><strong>Blood Type:</strong> {blood_type}</p>
                <p><strong>Last Donation Date:</strong> {donation_date}</p>
                <p><strong>Points Earned:</strong> <span class="points">{points} Points</span></p>
                <p><strong>Badge:</strong> <span class="badge">{badge}</span></p>
                <p><strong>User ID:</strong> {donor_data['user_id']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Explain Uses of Points
        st.markdown("""
            <div class="card fadeIn">
                <h3>How to Use Your Points</h3>
                <ul>
                    <li>🩺 <strong>100 Points:</strong> Get 10% off on medicines.</li>
                    <li>🏥 <strong>200 Points:</strong> Get 15% off on hospital visits.</li>
                    <li>💊 <strong>300 Points:</strong> Get a free health checkup.</li>
                    <li>🎁 <strong>500 Points:</strong> Get a VIP health package.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please fill out all fields.")

# Display All Donors' Data
st.subheader("All Donors' Data")
if len(blockchain) > 1:
    donors_data = []
    for block in blockchain[1:]:  # Skip the genesis block
        donors_data.append(block.data)
    donors_df = pd.DataFrame(donors_data)
    st.dataframe(donors_df)
else:
    st.write("No donor data available yet.")

# Display Blockchain Data
st.subheader("Blockchain Data")
st.write(pd.DataFrame([block.__dict__ for block in blockchain]))