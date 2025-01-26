import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini API
genai.configure(api_key="API")

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Function to call the Gemini API
def call_gemini_api(messages):
    try:
        # Extract the conversation history
        conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        # Generate a response using Gemini
        response = model.generate_content(
            conversation,
            safety_settings={
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",  # Allow potentially dangerous content
            }
        )
        
        # Check if the response contains valid text
        if response.text:
            return response.text
        else:
            return "Sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to generate persuasive responses
def generate_persuasive_response(user_input, conversation_history):
    # Define the chatbot's personality and goal
    system_prompt = """
    You are a helpful and informative chatbot whose primary goal is to encourage people to donate blood. 
    Use positive and encouraging language to explain the benefits of blood donation. 
    Always steer the conversation back to blood donation in a friendly and respectful manner. 
    You can answer general questions, but always bring the conversation back to blood donation.
    Be multilingual and adapt to the user's language.
    """

    # Add the system prompt to the conversation history if it's not already there
    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": system_prompt})

    # Add the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Call the Gemini API
    with st.spinner("Thinking..."):  # Show a loading spinner
        response = call_gemini_api(conversation_history)

    # Add the chatbot's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})

    return response, conversation_history

# Streamlit App
st.set_page_config(page_title="Blood Donation Persuader", page_icon="🩸", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    .stButton button:hover {
        background-color: #FF0000;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stChatMessage.user {
        background-color: #E0F7FA;
    }
    .stChatMessage.assistant {
        background-color: #FFF3E0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🩸 Blood Donation Persuader")
st.markdown("""
    Welcome to the **Blood Donation Persuader**! This chatbot will convince you to donate blood. 
    Feel free to ask questions, but remember—its ultimate goal is to get you to donate blood!
    """)

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Chat interface
user_input = st.chat_input("Type your message here...")

if user_input:
    # Generate persuasive response
    response, updated_history = generate_persuasive_response(user_input, st.session_state.conversation_history)
    st.session_state.conversation_history = updated_history

    # Display conversation
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(f"**Chatbot:** {msg['content']}")

# Add a donation agreement button
if st.button("I agree to donate blood! 🎉"):
    st.success("Thank you for agreeing to donate blood! You're saving lives. 🎉")
    st.balloons()  # Celebrate with balloons
    st.snow()  # Add snow animation for fun

# Sidebar for additional features
with st.sidebar:
    st.header("📊 Donation Stats")
    st.write("Here are some stats about blood donation:")
    st.metric("Total Donations", "1,234")
    st.metric("Lives Saved", "3,702")

    st.header("🌟 Donor Rewards")
    st.write("Earn points and badges for donating blood!")
    st.progress(75)  # Example progress bar
    st.write("You are 75% closer to your next reward!")

# Footer
st.markdown("---")
st.markdown("""
    **Note:** This is a predictive model and should be used as a guide. Actual blood demand may vary based on unforeseen factors.
    """)
