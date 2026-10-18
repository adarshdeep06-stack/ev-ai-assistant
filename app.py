import streamlit as st
import datetime
import random

# Page Configuration
st.set_page_config(page_title="EV: personal assistant 🧬", page_icon="🧬", layout="wide")

# Initialize Session State for Password and Tracking
if "master_password" not in st.session_state:
    st.session_state.master_password = "brandnewday"  # Default password

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0

if "sleep_hours" not in st.session_state:
    st.session_state.sleep_hours = 0

# --- PASSWORD AUTHENTICATION WALL ---
if not st.session_state.authenticated:
    st.title("🔒 EV: personal assistant 🧬")
    st.subheader("Security Lock")
    
    input_pwd = st.text_input("Enter Passcode to Access EV:", type="password")
    if st.button("Unlock EV"):
        if input_pwd == st.session_state.master_password:
            st.session_state.authenticated = True
            st.success("Access Granted! Welcome, Happy!")
            st.rerun()
        else:
            st.error("Incorrect Passcode! Try again.")
    st.stop()

# --- MAIN APPLICATION (AFTER LOGIN) ---
st.title("EV: personal assistant 🧬")

# Sidebar Settings & Change Password
with st.sidebar:
    st.header("⚙️ EV Settings")
    
    # Change Password Feature
    st.subheader("🔑 Security")
    with st.expander("Change Password"):
        current_p = st.text_input("Current Password", type="password")
        new_p = st.text_input("New Password", type="password")
        confirm_p = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Password"):
            if current_p != st.session_state.master_password:
                st.error("Current password does not match!")
            elif new_p != confirm_p:
                st.error("New passwords do not match!")
            elif not new_p:
                st.error("Password cannot be empty!")
            else:
                st.session_state.master_password = new_p
                st.success("Password updated successfully!")

    st.divider()
    if st.button("🔒 Lock EV"):
        st.session_state.authenticated = False
        st.rerun()

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat & Tutor", "📊 Daily Trackers", "📸 Image Analysis"])

# Tab 1: Chat & Tutor
with tab1:
    st.subheader("EV AI Assistant")
    hinglish_quotes = [
        "Har mushkil ka hal nikal sakta hai, bas thoda focus chahiye! 💡",
        "Aaj ka kaam kal par mat chhodo, Happy bhai! 🚀",
        "Believing in yourself is the first step to success! ✨",
        "Physics aur Math toh bas mind-games hain, hum milkar crack karenge! 🧠"
    ]
    st.info(f"✨ **EV's Thought:** {random.choice(hinglish_quotes)}")
    
    user_input = st.text_area("Ask EV anything (Physics, Math, Biology, Python, or General Guidance):")
    if st.button("Ask EV"):
        if user_input:
            st.write(f"**Happy:** {user_input}")
            st.write(f"**EV:** That's a great question! Let's break down '{user_input}' step by step...")
        else:
            st.warning("Please enter a question first.")

# Tab 2: Trackers
with tab2:
    st.subheader("💧 Daily Health & Prep Meter")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Hydration Tracker")
        if st.button("➕ Add 1 Glass Water (250ml)"):
            st.session_state.water_intake += 250
        st.metric(label="Total Water Intake Today", value=f"{st.session_state.water_intake} ml")
        
    with col2:
        st.write("### Sleep Tracker")
        st.session_state.sleep_hours = st.number_input("Hours slept last night:", min_value=0.0, max_value=24.0, value=float(st.session_state.sleep_hours), step=0.5)
        st.metric(label="Sleep Duration", value=f"{st.session_state.sleep_hours} hrs")

# Tab 3: Image Analysis
with tab3:
    st.subheader("📷 Upload Problem / Diagram")
    uploaded_file = st.file_uploader("Upload an image of your question or diagram:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Diagram/Problem", use_column_width=True)
        st.success("Image received! EV is processing the problem visual...")
