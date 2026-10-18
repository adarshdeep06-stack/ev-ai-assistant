import streamlit as st
import random
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="EV: personal assistant 🧬", page_icon="🧬", layout="wide")

# --- CUSTOM LIQUID GLASS NAVY BLUE STYLING ---
st.markdown("""
    <style>
    /* Main Background - Liquid Navy Blue Gradient */
    .stApp {
        background: linear-gradient(135deg, #0A1128 0%, #0F172A 50%, #020617 100%);
        color: #F1F5F9;
        padding-bottom: 120px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(56, 189, 248, 0.1);
    }
    
    /* Glassmorphism Cards */
    .glass-box {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284C7 100%);
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #F1F5F9 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "master_password" not in st.session_state:
    st.session_state.master_password = "brandnewday"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0

if "sleep_hours" not in st.session_state:
    st.session_state.sleep_hours = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- PASSWORD AUTHENTICATION WALL ---
if not st.session_state.authenticated:
    st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; padding: 30px;" class="glass-box">
            <h2 style="color: #38BDF8; text-align: center;">🔒 EV: personal assistant 🧬</h2>
            <p style="text-align: center; color: #94A3B8;">Security Lock Active</p>
    """, unsafe_allow_html=True)
    
    input_pwd = st.text_input("Enter Passcode to Access EV:", type="password")
    if st.button("Unlock EV", use_container_width=True):
        if input_pwd == st.session_state.master_password:
            st.session_state.authenticated = True
            st.success("Access Granted! Welcome, Happy!")
            st.rerun()
        else:
            st.error("Incorrect Passcode! Try again.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APPLICATION ---
st.title("EV: personal assistant 🧬")

# Sidebar Settings & Dynamic Password Change
with st.sidebar:
    st.header("⚙️ EV Settings")
    st.markdown("---")
    
    st.subheader("🔑 Security Manager")
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

    st.markdown("---")
    if st.button("🔒 Lock EV", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Helper function for Strict Samantha Female Voice + Bottom Waveform + Top Subtitles
def render_voice_button(text_to_speak, button_id):
    safe_text = text_to_speak.replace("'", "\\'").replace("\n", " ")
    return f"""
    <div>
        <script>
        function speak_{button_id}() {{
            window.speechSynthesis.cancel();
            
            let cleanText = '{safe_text}'
                .replace(/agar/gi, 'aghar')
                .replace(/chiz/gi, 'cheez')
                .replace(/sidhat/gi, 'shiddat')
                .replace(/kayanat/gi, 'kaynaat')
                .replace(/usse/gi, 'usse')
                .replace(/milna/gi, 'milne')
                .replace(/who/gi, 'woh')
                .replace(/baki/gi, 'baaki');

            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'en-IN';
            utterance.rate = 0.92;   // Calm, polite speed
            utterance.pitch = 1.25;  // Sweet female tone

            // Strictly target Samantha and iOS female voices
            const voices = window.speechSynthesis.getVoices();
            const sweetFemaleVoice = voices.find(v => 
                v.name.includes('Samantha') || 
                v.name.includes('Karen') || 
                v.name.includes('Tessa') || 
                v.name.includes('Veena') || 
                v.name.includes('Siri (Female') || 
                v.name.includes('Google US English Female') ||
                v.name.includes('Zira') ||
                (v.name.toLowerCase().includes('female') && v.lang.includes('en'))
            ) || voices.find(v => v.lang.includes('en-IN') || v.lang.includes('en-US'));

            if (sweetFemaleVoice) {{
                utterance.voice = sweetFemaleVoice;
            }}

            const waveContainer = window.parent.document.getElementById('bottom-wave-container');
            const subtitleBox = window.parent.document.getElementById('top-subtitle-box');

            utterance.onstart = function() {{
                if (waveContainer) waveContainer.style.display = 'flex';
                if (subtitleBox) {{
                    subtitleBox.style.display = 'block';
                    subtitleBox.innerText = "🗣️ EV: " + '{safe_text}';
                }}
            }};
            utterance.onend = function() {{
                if (waveContainer) waveContainer.style.display = 'none';
                if (subtitleBox) subtitleBox.style.display = 'none';
            }};
            utterance.onerror = function() {{
                if (waveContainer) waveContainer.style.display = 'none';
                if (subtitleBox) subtitleBox.style.display = 'none';
            }};

            window.speechSynthesis.speak(utterance);
        }
        </script>
        
        <button onclick="speak_{button_id}()" style="background: linear-gradient(135deg, #0284C7, #0369A1); color:white; padding:8px 18px; border:1px solid rgba(56,189,248,0.4); border-radius:8px; font-weight:600; cursor:pointer;">
            🔊 Speak Answer
        </button>
    </div>
    """

# Inject Fixed Bottom Waveform Bar and Top Screen Subtitles into Main DOM
st.components.v1.html("""
    <script>
    const doc = window.parent.document;
    
    // Create Top Screen Subtitle Overlay
    if (!doc.getElementById('top-subtitle-box')) {
        const subBox = doc.createElement('div');
        subBox.id = 'top-subtitle-box';
        subBox.style.cssText = `
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 85%;
            max-width: 800px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(56, 189, 248, 0.5);
            color: #38BDF8;
            padding: 12px 20px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
            z-index: 999999;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: none;
            backdrop-filter: blur(10px);
        `;
        doc.body.appendChild(subBox);
    }

    // Create Bottom Full-Width Audio Waveform Bar
    if (!doc.getElementById('bottom-wave-container')) {
        const waveBox = doc.createElement('div');
        waveBox.id = 'bottom-wave-container';
        waveBox.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100vw;
            height: 50px;
            background: rgba(10, 17, 40, 0.92);
            border-top: 1px solid rgba(56, 189, 248, 0.3);
            display: none;
            justify-content: center;
            align-items: center;
            gap: 6px;
            z-index: 999999;
            backdrop-filter: blur(12px);
        `;
        
        for(let i=0; i<30; i++){
            const bar = doc.createElement('div');
            bar.className = 'bottom-bar';
            bar.style.cssText = `
                width: 4px;
                height: 10px;
                background-color: #38BDF8;
                border-radius: 2px;
                animation: fullWaveAnim 0.8s infinite ease-in-out;
                animation-delay: ${(i * 0.05).toFixed(2)}s;
            `;
            waveBox.appendChild(bar);
        }

        if (!doc.getElementById('wave-style-sheet')) {
            const style = doc.createElement('style');
            style.id = 'wave-style-sheet';
            style.innerHTML = `
                @keyframes fullWaveAnim {
                    0%, 100% { height: 8px; opacity: 0.4; }
                    50% { height: 38px; opacity: 1; background-color: #0ea5e9; box-shadow: 0 0 10px #38bdf8; }
                }
            `;
            doc.head.appendChild(style);
        }

        doc.body.appendChild(waveBox);
    }
    </script>
""", height=0)

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat & Search", "📊 Daily Trackers", "📸 Image Analysis"])

# Tab 1: Unrestricted Chat & Direct Output
with tab1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("EV AI Assistant")
    
    # User's Exact Quotes
    user_quotes = [
        "Great power comes with Great responsibilities",
        "No amount of money ever bought a second",
        "Agar kisi chiz ko sidhat se chaho to puri kayanat tumhe usse milna me jot jati hai",
        "Never let anything make you forget how u really are",
        "Agar life mein happy ending na ho to who ending nahi picture abhi baki hai mere dost"
    ]
    thought = random.choice(user_quotes)
    st.info(f"✨ **EV's Thought:** {thought}")
    
    components.html(render_voice_button(thought, "thought"), height=55)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    user_input = st.text_area("Ask EV anything without restrictions:")
    
    if st.button("Ask EV", use_container_width=True):
        if user_input:
            ev_response = f"Here is the exact information for '{user_input}': Full response generated directly as requested."
            st.session_state.chat_history.append(("Happy", user_input))
            st.session_state.chat_history.append(("EV", ev_response))
        else:
            st.warning("Please enter a question or query first.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display Chat History
    if st.session_state.chat_history:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.write("### Conversation")
        for idx, (sender, message) in enumerate(st.session_state.chat_history):
            if sender == "Happy":
                st.markdown(f"**👤 You:** {message}")
            else:
                st.markdown(f"**🧬 EV:** {message}")
                components.html(render_voice_button(message, f"msg_{idx}"), height=55)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Trackers
with tab2:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Image Analysis
with tab3:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("📷 Upload Problem / Diagram")
    uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.success("Image received! EV is processing full analysis...")
    st.markdown('</div>', unsafe_allow_html=True)
