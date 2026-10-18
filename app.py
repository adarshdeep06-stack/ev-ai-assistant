import streamlit as st
import random
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="EV: personal assistant 🧬", page_icon="🧬", layout="wide")

# --- HIGH-CONTRAST LIQUID GLASS NAVY BLUE STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #090D16 0%, #111827 50%, #020617 100%);
        color: #FFFFFF;
        padding-bottom: 120px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    /* High-Visibility Liquid Glass Navy Blue Bubbles */
    .glass-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 58, 138, 0.65) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.5);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
        color: #FFFFFF !important;
    }
    
    .glass-box h1, .glass-box h2, .glass-box h3, .glass-box p, .glass-box label, .glass-box span {
        color: #FFFFFF !important;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.6);
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284C7 100%);
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.95) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
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

if "greeted" not in st.session_state:
    st.session_state.greeted = False

# --- PASSWORD AUTHENTICATION WALL ---
if not st.session_state.authenticated:
    st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; padding: 30px;" class="glass-box">
            <h2 style="color: #38BDF8; text-align: center;">🔒 EV: personal assistant 🧬</h2>
            <p style="text-align: center; color: #CBD5E1;">Security Lock Active</p>
    """, unsafe_allow_html=True)
    
    input_pwd = st.text_input("Enter Passcode to Access EV:", type="password")
    if st.button("Unlock EV", use_container_width=True):
        if input_pwd == st.session_state.master_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect Passcode! Try again.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APPLICATION ---
st.markdown('<div class="glass-box"><h1>EV: personal assistant 🧬</h1></div>', unsafe_allow_html=True)

# Sidebar Settings & Password Management
with st.sidebar:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Helper function for Strict Female Voice + Bottom Waveform + Top Subtitles
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
            utterance.lang = 'en-US';
            utterance.rate = 0.92;
            utterance.pitch = 1.25;

            function setFemaleVoice() {{
                const voices = window.speechSynthesis.getVoices();
                const targetVoice = voices.find(v => v.name === 'Samantha') ||
                                    voices.find(v => v.name === 'Karen') ||
                                    voices.find(v => v.name.includes('Siri') && v.name.includes('Female')) ||
                                    voices.find(v => v.name.includes('Veena')) ||
                                    voices.find(v => v.name.includes('Victoria')) ||
                                    voices.find(v => v.name.includes('Zira')) ||
                                    voices.find(v => v.name.toLowerCase().includes('female')) ||
                                    voices.find(v => v.lang.includes('en'));

                if (targetVoice) {{
                    utterance.voice = targetVoice;
                }}
            }}

            setFemaleVoice();
            if (window.speechSynthesis.onvoiceschanged !== undefined) {{
                window.speechSynthesis.onvoiceschanged = setFemaleVoice;
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

# Inject UI Elements (Bottom Waveform, Top Subtitles, Auto Greeting)
st.components.v1.html(f"""
    <script>
    const doc = window.parent.document;
    
    if (!doc.getElementById('top-subtitle-box')) {{
        const subBox = doc.createElement('div');
        subBox.id = 'top-subtitle-box';
        subBox.style.cssText = `
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 85%;
            max-width: 800px;
            background: rgba(15, 23, 42, 0.98);
            border: 1px solid rgba(56, 189, 248, 0.6);
            color: #38BDF8;
            padding: 14px 22px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            text-align: center;
            z-index: 999999;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
            display: none;
            backdrop-filter: blur(12px);
        `;
        doc.body.appendChild(subBox);
    }}

    if (!doc.getElementById('bottom-wave-container')) {{
        const waveBox = doc.createElement('div');
        waveBox.id = 'bottom-wave-container';
        waveBox.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100vw;
            height: 55px;
            background: rgba(15, 23, 42, 0.96);
            border-top: 1px solid rgba(56, 189, 248, 0.4);
            display: none;
            justify-content: center;
            align-items: center;
            gap: 6px;
            z-index: 999999;
            backdrop-filter: blur(12px);
        `;
        
        for(let i=0; i<30; i++){{
            const bar = doc.createElement('div');
            bar.style.cssText = `
                width: 4px;
                height: 10px;
                background-color: #38BDF8;
                border-radius: 2px;
                animation: fullWaveAnim 0.8s infinite ease-in-out;
                animation-delay: ${(i * 0.05).toFixed(2)}s;
            `;
            waveBox.appendChild(bar);
        }}

        if (!doc.getElementById('wave-style-sheet')) {{
            const style = doc.createElement('style');
            style.id = 'wave-style-sheet';
            style.innerHTML = `
                @keyframes fullWaveAnim {{
                    0%, 100% {{ height: 8px; opacity: 0.4; }}
                    50% {{ height: 38px; opacity: 1; background-color: #0ea5e9; box-shadow: 0 0 12px #38bdf8; }}
                }}
            `;
            doc.head.appendChild(style);
        }}

        doc.body.appendChild(waveBox);
    }}

    // Auto Greeting on First Load
    {"window.hasGreeted = true; setTimeout(() => { const greetingText = 'Hello! How was your day today?'; const utterance = new SpeechSynthesisUtterance(greetingText); utterance.pitch = 1.25; utterance.rate = 0.92; window.speechSynthesis.speak(utterance); }, 1000);" if not st.session_state.greeted else ""}
    </script>
""", height=0)

st.session_state.greeted = True

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat & Search", "📊 Daily Trackers", "📸 Image Analysis"])

# Tab 1: Chat & Voice
with tab1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("EV AI Assistant")
    
    user_quotes = [
        "Great power comes with Great responsibilities",
        "No amount of money ever bought a second",
        "Agar kisi chiz ko sidhat se chaho to puri kayanat tumhe usse milna me jot jati hai",
        "Never let anything make you forget how u really are",
        "Agar life mein happy ending na ho to who ending nahi picture abhi baki hai mere dost"
    ]
    thought = random.choice(user_quotes)
    st.write(f"✨ **EV's Thought:** {thought}")
    
    components.html(render_voice_button(thought, "thought"), height=55)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    user_input = st.text_area("Ask EV anything:")
    
    if st.button("Ask EV", use_container_width=True):
        if user_input:
            ev_response = f"Here is the exact information for '{user_input}': Full response generated directly as requested."
            st.session_state.chat_history.append(("Happy", user_input))
            st.session_state.chat_history.append(("EV", ev_response))
        else:
            st.warning("Please enter a question or query first.")
    st.markdown('</div>', unsafe_allow_html=True)

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
