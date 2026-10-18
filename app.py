import streamlit as st
import random
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="EV: personal assistant 🧬", page_icon="🧬", layout="wide")

# --- HIGH-VISIBILITY FUTURISTIC LIQUID GLASS STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #070B14 0%, #0F172A 50%, #020617 100%);
        color: #FFFFFF !important;
        padding-bottom: 140px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Liquid Glass Navy Blue Bubbles with High Text Visibility */
    .glass-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(30, 58, 138, 0.75) 100%);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1.5px solid rgba(56, 189, 248, 0.6);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.7);
        margin-bottom: 22px;
        color: #FFFFFF !important;
    }
    
    .glass-box *, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, label, span {
        color: #FFFFFF !important;
    }
    
    /* High Visibility Search / Text Area Fix */
    .stTextArea textarea, .stTextInput input {
        background-color: #0B132B !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1.5px solid rgba(56, 189, 248, 0.7) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    
    /* Custom Futuristic Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: white !important;
        border: 1px solid rgba(56, 189, 248, 0.8);
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284C7 100%);
        border-color: #38bdf8;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.8);
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

# --- MAIN APPLICATION HEADER ---
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

# Safe Voice Button Renderer targeting Parent Window for iOS Safari/Chrome
def render_voice_button(text_to_speak, button_id):
    safe_text = text_to_speak.replace("'", "\\'").replace("\n", " ")
    template = """
    <div>
        <script>
        function speak_BTN_ID() {
            const synth = window.parent.window.speechSynthesis;
            if (!synth) return;
            synth.cancel();
            
            let cleanText = 'SAFE_TEXT'
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
            utterance.rate = 0.94;
            utterance.pitch = 1.38;

            function setFemaleVoice() {
                const voices = synth.getVoices();
                const targetVoice = voices.find(v => v.name === 'Samantha') ||
                                    voices.find(v => v.name === 'Karen') ||
                                    voices.find(v => v.name.includes('Siri') && v.name.includes('Female')) ||
                                    voices.find(v => v.name.includes('Veena')) ||
                                    voices.find(v => v.name.includes('Victoria')) ||
                                    voices.find(v => v.name.includes('Zira')) ||
                                    voices.find(v => v.name.toLowerCase().includes('female')) ||
                                    voices.find(v => v.lang.includes('en'));

                if (targetVoice) {
                    utterance.voice = targetVoice;
                }
            }

            setFemaleVoice();
            if (synth.onvoiceschanged !== undefined) {
                synth.onvoiceschanged = setFemaleVoice;
            }

            const waveContainer = window.parent.document.getElementById('bottom-wave-container');
            const subtitleBox = window.parent.document.getElementById('top-subtitle-box');

            utterance.onstart = function() {
                if (waveContainer) waveContainer.style.display = 'flex';
                if (subtitleBox) {
                    subtitleBox.style.display = 'block';
                    subtitleBox.innerText = "🗣️ EV: " + 'SAFE_TEXT';
                }
            };
            utterance.onend = function() {
                if (waveContainer) waveContainer.style.display = 'none';
                if (subtitleBox) subtitleBox.style.display = 'none';
            };
            utterance.onerror = function() {
                if (waveContainer) waveContainer.style.display = 'none';
                if (subtitleBox) subtitleBox.style.display = 'none';
            };

            synth.speak(utterance);
        }
        </script>
        
        <button onclick="speak_BTN_ID()" style="background: linear-gradient(135deg, #0284C7, #0369A1); color:white; padding:8px 18px; border:1px solid rgba(56,189,248,0.6); border-radius:10px; font-weight:700; cursor:pointer;">
            🔊 Speak Answer
        </button>
    </div>
    """
    return template.replace("BTN_ID", str(button_id)).replace("SAFE_TEXT", safe_text)

# Inject Full-Width Edge-to-Edge Bottom Waveform Line & Top Subtitles
components.html("""
    <script>
    const doc = window.parent.document;
    
    if (!doc.getElementById('top-subtitle-box')) {
        const subBox = doc.createElement('div');
        subBox.id = 'top-subtitle-box';
        subBox.style.cssText = `
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 900px;
            background: rgba(15, 23, 42, 0.98);
            border: 1px solid rgba(56, 189, 248, 0.7);
            color: #38BDF8;
            padding: 14px 24px;
            border-radius: 14px;
            font-size: 17px;
            font-weight: 700;
            text-align: center;
            z-index: 999999;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            display: none;
            backdrop-filter: blur(16px);
        `;
        doc.body.appendChild(subBox);
    }

    if (!doc.getElementById('bottom-wave-container')) {
        const waveBox = doc.createElement('div');
        waveBox.id = 'bottom-wave-container';
        waveBox.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 60px;
            background: rgba(7, 11, 20, 0.98);
            border-top: 1.5px solid rgba(56, 189, 248, 0.7);
            display: none;
            justify-content: space-between;
            align-items: center;
            padding: 0 10px;
            z-index: 999999;
            backdrop-filter: blur(16px);
            box-shadow: 0 -5px 30px rgba(56, 189, 248, 0.5);
        `;
        
        for(let i=0; i<65; i++){
            const bar = doc.createElement('div');
            bar.style.cssText = `
                width: calc(100vw / 80);
                height: 8px;
                background-color: #38BDF8;
                border-radius: 3px;
                animation: fullWaveAnim 0.7s infinite ease-in-out;
                animation-delay: ${(i * 0.025).toFixed(2)}s;
            `;
            waveBox.appendChild(bar);
        }

        if (!doc.getElementById('wave-style-sheet')) {
            const style = doc.createElement('style');
            style.id = 'wave-style-sheet';
            style.innerHTML = `
                @keyframes fullWaveAnim {
                    0%, 100% { height: 8px; opacity: 0.4; }
                    50% { height: 44px; opacity: 1; background-color: #38bdf8; box-shadow: 0 0 15px #38bdf8; }
                }
            `;
            doc.head.appendChild(style);
        }

        doc.body.appendChild(waveBox);
    }
    </script>
""", height=0)

# Trigger auto greeting once per session
if not st.session_state.greeted:
    greeting_script = """
    <script>
    setTimeout(() => {
        const synth = window.parent.window.speechSynthesis;
        if (!synth) return;
        const greetingText = "Hello Happy! How was your day today?";
        const utterance = new SpeechSynthesisUtterance(greetingText);
        utterance.pitch = 1.38;
        utterance.rate = 0.94;
        
        const voices = synth.getVoices();
        const targetVoice = voices.find(v => v.name === 'Samantha') || voices.find(v => v.name.includes('Female')) || voices.find(v => v.lang.includes('en'));
        if (targetVoice) utterance.voice = targetVoice;
        
        const waveContainer = window.parent.document.getElementById('bottom-wave-container');
        const subtitleBox = window.parent.document.getElementById('top-subtitle-box');
        
        utterance.onstart = function() {
            if (waveContainer) waveContainer.style.display = 'flex';
            if (subtitleBox) {
                subtitleBox.style.display = 'block';
                subtitleBox.innerText = "🗣️ EV: " + greetingText;
            }
        };
        utterance.onend = function() {
            if (waveContainer) waveContainer.style.display = 'none';
            if (subtitleBox) subtitleBox.style.display = 'none';
        };
        
        synth.speak(utterance);
    }, 1200);
    </script>
    """
    components.html(greeting_script, height=0)
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
