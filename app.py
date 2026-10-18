import streamlit as st
import streamlit.components.v1 as components
import math
import re
from datetime import date, datetime

# --- 1. PAGE CONFIG & LIQUID NAVY STYLING ---
st.set_page_config(page_title="EV: personal helper 🧬", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0B1528 50%, #02040A 100%);
        color: #E2E8F0;
        font-family: system-ui, -apple-system, sans-serif;
    }
    .glass-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .ev-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .quote-banner {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 10px;
        padding: 10px 15px;
        color: #38BDF8;
        font-style: italic;
        font-size: 0.95rem;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* --- HIGH CONTRAST INPUT BOX FIX --- */
    div[data-baseweb="input"] {
        background-color: #0b1329 !important;
        border-radius: 10px !important;
        border: 2px solid #38BDF8 !important;
    }
    .stTextInput input {
        background-color: #0b1329 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
    }

    .calc-screen {
        background-color: #090d16;
        color: #38BDF8;
        font-size: 1.5rem;
        font-family: monospace;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #38BDF8;
        min-height: 55px;
        margin-bottom: 15px;
        word-break: break-all;
    }
    .step-line {
        background: rgba(2, 6, 23, 0.7);
        border-left: 4px solid #38BDF8;
        padding: 10px 15px;
        margin-top: 6px;
        font-family: monospace;
        font-size: 1rem;
        color: #E2E8F0;
    }
    .grid-row {
        font-family: monospace;
        letter-spacing: 10px;
        font-size: 1.2rem;
        color: #38BDF8;
        background: rgba(0,0,0,0.4);
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "locked" not in st.session_state:
    st.session_state.locked = True
if "password" not in st.session_state:
    st.session_state.password = "brandnewday"
if "math_expr" not in st.session_state:
    st.session_state.math_expr = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "solved_words" not in st.session_state:
    st.session_state.solved_words = []
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# --- 3. LOCK SCREEN ---
if st.session_state.locked:
    st.markdown("<div class='glass-card' style='max-width: 400px; margin: 80px auto; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#38BDF8;'>🔒 EV Security Lock</h2>", unsafe_allow_html=True)
    entered = st.text_input("Enter Passcode:", type="password", key="lock_field")
    if st.button("Unlock EV", use_container_width=True):
        if entered == st.session_state.password:
            st.session_state.locked = False
            st.rerun()
        else:
            st.error("Incorrect passcode!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. EV VOICE (FEMALE SYNTHESIS & MIC) ---
def speak(text):
    clean_t = re.sub(r'[^a-zA-Z0-9\s\.]', '', str(text))
    components.html(f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean_t}');
        msg.rate = 1.0;
        msg.pitch = 1.2;
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)

def render_mic():
    components.html("""
    <div style="text-align: center; margin-bottom: 15px;">
        <button onclick="startListening()" style="background: linear-gradient(90deg, #0284c7, #2563eb); color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 1rem;">
            🎤 Tap to Speak Question to EV
        </button>
        <p id="micStatus" style="color: #94A3B8; font-size: 0.8rem; margin-top: 5px;"></p>
    </div>
    <script>
        function startListening() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                var recognition = new SpeechRecognition();
                recognition.lang = 'en-US';
                document.getElementById('micStatus').innerText = "Listening...";
                recognition.start();
                recognition.onresult = function(event) {
                    var speechResult = event.results[0][0].transcript;
                    document.getElementById('micStatus').innerText = "Heard: " + speechResult;
                    var inputs = window.parent.document.querySelectorAll('input[type="text"]');
                    if (inputs.length > 0) {
                        inputs[0].value = speechResult;
                        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                };
                recognition.onerror = function() {
                    document.getElementById('micStatus').innerText = "Microphone error or permission denied.";
                };
            } else {
                document.getElementById('micStatus').innerText = "Speech recognition not supported in this browser.";
            }
        }
    </script>
    """, height=80)

# --- 5. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>⚙️ EV Controls</h2>", unsafe_allow_html=True)
    if st.button("🔒 Lock EV Now", use_container_width=True):
        st.session_state.locked = True
        st.rerun()
        
    with st.expander("🔑 Change Password"):
        p1 = st.text_input("New Password:", type="password")
        if st.button("Save Password"):
            if p1:
                st.session_state.password = p1
                st.success("Password updated!")

    st.markdown("---")
    st.markdown("<h3 style='color:#38BDF8;'>📜 Search History</h3>", unsafe_allow_html=True)
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.write(f"**{item['q']}**")
            st.caption(f"= {item['r']} ({item['t']})")
            st.markdown("---")
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No past calculations yet.")

# --- 6. MAIN INTERFACE ---
st.markdown("<h1 class='ev-title'>EV: personal helper 🧬</h1>", unsafe_allow_html=True)
st.markdown("<div class='quote-banner'>\"With great powers comes great responsibilities\"</div>", unsafe_allow_html=True)

tab_calc, tab_puzzle = st.tabs(["🧮 Scientific Calculator", "📰 Daily Newspaper Puzzle"])

# --- TAB 1: CALCULATOR & KEYPAD ---
with tab_calc:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    render_mic()
    
    screen_val = st.session_state.math_expr if st.session_state.math_expr else "0"
    st.markdown(f"<div class='calc-screen'>{screen_val}</div>", unsafe_allow_html=True)

    keys = [
        ["sin(", "cos(", "tan(", "sqrt(", "^"],
        ["log(", "ln(", "pi", "e", "("],
        ["7", "8", "9", "/", ")"],
        ["4", "5", "6", "*", "⌫"],
        ["1", "2", "3", "-", "CLEAR"],
        ["0", ".", "+", "=", "🔊 Speak"]
    ]

    for row in keys:
        cols = st.columns(5)
        for i, btn in enumerate(row):
            if cols[i].button(btn, key=f"k_{btn}", use_container_width=True):
                if btn == "CLEAR":
                    st.session_state.math_expr = ""
                elif btn == "⌫":
                    st.session_state.math_expr = st.session_state.math_expr[:-1]
                elif btn not in ["=", "🔊 Speak"]:
                    st.session_state.math_expr += btn
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Step-by-Step Solver
    if st.session_state.math_expr:
        expr = st.session_state.math_expr
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📐 Step-by-Step Downward Solution")
        
        steps = [f"Step 1: Input expression -> {expr}"]
        parsed = expr.replace("^", "**").replace("pi", "math.pi").replace("e", "math.e")
        parsed = re.sub(r'sqrt\(', 'math.sqrt(', parsed)
        parsed = re.sub(r'sin\(', 'math.sin(math.radians(', parsed)
        parsed = re.sub(r'cos\(', 'math.cos(math.radians(', parsed)
        parsed = re.sub(r'tan\(', 'math.tan(math.radians(', parsed)
        parsed = re.sub(r'log\(', 'math.log10(', parsed)
        parsed = re.sub(r'ln\(', 'math.log(', parsed)
        parsed += ")" * (expr.count("sin(") + expr.count("cos(") + expr.count("tan("))

        steps.append(f"Step 2: Parsed formula -> {parsed}")

        try:
            res = eval(parsed, {"math": math, "__builtins__": None})
            if isinstance(res, float):
                res = round(res, 6)
            steps.append(f"Step 3: Result calculated -> {res}")
            
            for s in steps:
                st.markdown(f"<div class='step-line'>{s}</div>", unsafe_allow_html=True)

            if not st.session_state.history or st.session_state.history[-1]['q'] != expr:
                st.session_state.history.append({
                    'q': expr, 'r': str(res), 't': datetime.now().strftime("%H:%M")
                })
            
            speak(f"The answer is {res}")

        except Exception:
            st.markdown("<div class='step-line' style='border-left-color: #ef4444;'>Waiting for complete mathematical expression...</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: NEWSPAPER PUZZLE ---
with tab_puzzle:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>📰 Daily Indian Newspaper Word Puzzle</h3><p style='color:#94A3B8;'>Date: {date.today().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    
    GRID = [
        ["I", "N", "D", "I", "A", "M", "A", "T", "H", "S"],
        ["S", "C", "I", "E", "N", "C", "E", "P", "E", "N"],
        ["P", "L", "A", "N", "E", "T", "A", "R", "R", "C"],
        ["A", "E", "A", "R", "T", "H", "C", "O", "D", "E"],
        ["C", "A", "R", "D", "B", "R", "A", "I", "N", "S"],
        ["E", "M", "O", "O", "N", "L", "I", "G", "H", "T"],
        ["T", "R", "I", "G", "O", "N", "O", "M", "E", "T"],
        ["S", "P", "A", "C", "E", "P", "Y", "T", "H", "O"],
        ["N", "U", "M", "B", "E", "R", "F", "I", "V", "E"],
        ["W", "A", "T", "E", "R", "F", "A", "L", "L", "S"]
    ]

    WORDS_12 = {
        "INDIA": "Our country name",
        "MATHS": "Subject of calculations",
        "SCIENCE": "Study of nature and universe",
        "PLANET": "Celestial body orbiting a star",
        "EARTH": "Our home world",
        "CODE": "Program instructions",
        "BRAIN": "Control center of the body",
        "SPACE": "Cosmic realm above sky",
        "MOON": "Earth's natural satellite",
        "LIGHT": "Energy that lets us see",
        "PENCIL": "Tool used for writing",
        "CARD": "Paper object or ticket"
    }

    for row in GRID:
        st.markdown(f"<div class='grid-row'>{' '.join(row)}</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("#### 📝 Find 12 Words (Dashed Format):")
    for w in WORDS_12.keys():
        if w in st.session_state.solved_words:
            st.markdown(f"✅ **{w}** (Solved)")
        else:
            dashed = " ".join(["_" for _ in w])
            st.markdown(f"📌 `{dashed}` ({len(w)} letters)")

    st.markdown("---")
    guess = st.text_input("Type a word you found:", key="puz_in").strip().upper()
    if st.button("Submit Word"):
        if guess in WORDS_12:
            if guess not in st.session_state.solved_words:
                st.session_state.solved_words.append(guess)
                speak(f"Correct! You found {guess}")
                st.rerun()
            else:
                st.warning("You already found this word!")
        else:
            st.error("Incorrect word. Keep looking!")

    st.markdown("---")
    if st.button("🔑 Show Answer Key / Clues"):
        st.session_state.show_answer = not st.session_state.show_answer

    if st.session_state.show_answer:
        st.markdown("<div style='background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.write("### Clues & Answers:")
        for w, clue in WORDS_12.items():
            st.write(f"- **{w}**: {clue}")
        st.markdown("</div>", unsafe_allow_html=True)

    if len(st.session_state.solved_words) == 12:
        st.markdown("""
        <div style='background: #15803d; color: white; padding: 20px; border-radius: 12px; text-align: center; margin-top: 15px;'>
            <h1>✔ PUZZLE COMPLETED!</h1>
            <p>Awesome job! You found all 12 words in today's grid!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Congratulations! You completed today's newspaper puzzle!")

    st.markdown("</div>", unsafe_allow_html=True)
