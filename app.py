import streamlit as st
import streamlit.components.v1 as components
import math
import re
from datetime import date

# --- 1. PAGE CONFIG & LIQUID NAVY STYLING ---
st.set_page_config(page_title="EV: personal helper 🧬", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    /* Liquid Navy & Lure Black Background */
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0B1528 50%, #02040A 100%);
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Glowing Glass Containers */
    .glass-panel {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.25);
    }
    
    /* EV Header */
    .ev-header {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }

    /* Fixed Text Input Contrast */
    .stTextInput input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        border: 2px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 12px !important;
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #2563eb 100%);
        color: #ffffff !important;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 8px 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }

    /* Tab navigation style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
        color: #94A3B8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.2) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. VOICE SYNTHESIS HELPER (OFFLINE EV VOICE) ---
def speak_response(text):
    """Uses client-side browser speech synthesis with EV's signature voice settings."""
    clean_text = text.replace("'", "\\'")
    html_code = f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.rate = 0.95;
        msg.pitch = 1.1;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(html_code, height=0, width=0)

# --- 3. OFFLINE SCIENTIFIC CALCULATOR ENGINE ---
def ev_scientific_calc(query: str):
    q = query.lower().strip()
    safe_dict = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sqrt': math.sqrt, 'log': math.log10, 'ln': math.log,
        'exp': math.exp, 'pi': math.pi, 'e': math.e,
        'factorial': math.factorial, 'radians': math.radians,
        'degrees': math.degrees, 'pow': math.pow, 'abs': abs
    }
    
    clean_q = re.sub(r'square root of ([0-9.]+)', r'sqrt(\1)', q)
    clean_q = re.sub(r'log of ([0-9.]+)', r'log(\1)', clean_q)
    clean_q = re.sub(r'sin of ([0-9.]+)', r'sin(radians(\1))', clean_q)
    clean_q = re.sub(r'cos of ([0-9.]+)', r'cos(radians(\1))', clean_q)
    clean_q = re.sub(r'tan of ([0-9.]+)', r'tan(radians(\1))', clean_q)
    clean_q = clean_q.replace('x', '*').replace('^', '**')
    clean_q = re.sub(r'[^0-9\.\+\-\*\/\(\)\,\s\a-z\_]', '', clean_q)
    
    try:
        res = eval(clean_q, {"__builtins__": None}, safe_dict)
        if isinstance(res, float):
            res = round(res, 6)
        return f"Result: {res}", str(res)
    except Exception:
        return "Enter a valid scientific expression (e.g. 'sqrt(144)', 'sin(30)', 'log(100)').", None

# --- 4. DAILY WORD PUZZLE DATABASE ---
DAILY_PUZZLES = [
    {"word": "APPLE", "scramble": "P E A L P", "clue": "A common sweet red or green fruit.", "hint": "Starts with 'A'"},
    {"word": "BRAIN", "scramble": "R I A N B", "clue": "The center of thought in your body.", "hint": "Starts with 'B'"},
    {"word": "CLOUD", "scramble": "O L D C U", "clue": "Fluffy white body in the sky.", "hint": "Starts with 'C'"},
    {"word": "DREAM", "scramble": "R E A M D", "clue": "Thoughts or images while sleeping.", "hint": "Starts with 'D'"},
    {"word": "EARTH", "scramble": "R T H E A", "clue": "The planet we all live on.", "hint": "Starts with 'E'"},
    {"word": "FLAME", "scramble": "L A M E F", "clue": "The visible part of a fire.", "hint": "Starts with 'F'"},
    {"word": "GRASS", "scramble": "S R A S G", "clue": "Green vegetation covering lawns.", "hint": "Starts with 'G'"},
    {"word": "HEART", "scramble": "E A R T H", "clue": "Organ that pumps blood.", "hint": "Starts with 'H'"},
    {"word": "LIGHT", "scramble": "G H T L I", "clue": "Natural agent that stimulates sight.", "hint": "Starts with 'L'"},
    {"word": "PLANT", "scramble": "L A N T P", "clue": "A living organism that absorbs water.", "hint": "Starts with 'P'"},
    {"word": "SMOKE", "scramble": "M O K E S", "clue": "Gas produced by burning material.", "hint": "Starts with 'S'"},
    {"word": "WATER", "scramble": "T E R W A", "clue": "Clear liquid essential for life.", "hint": "Starts with 'W'"}
]

# --- MAIN APP LAYOUT ---
st.markdown("<h1 class='ev-header'>EV: personal helper 🧬</h1>", unsafe_allow_html=True)

tab_calc, tab_game = st.tabs(["🧮 Scientific Calculator", "🧩 Daily Word Arcade"])

# --- TAB 1: CALCULATOR ---
with tab_calc:
    st.markdown("<div class='glass-panel'><h3>Scientific Math Assistant</h3><p style='color:#94A3B8;'>Calculates trigonometry, logarithms, factorials, roots, and standard math offline.</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("sqrt(256)"): st.session_state['math_in'] = "sqrt(256)"
    if col2.button("sin(90)"): st.session_state['math_in'] = "sin of 90"
    if col3.button("log(1000)"): st.session_state['math_in'] = "log(1000)"
    if col4.button("5^3"): st.session_state['math_in'] = "5^3"
    
    expr = st.text_input("Enter Math Expression:", key="math_in", placeholder="e.g. sqrt(144) + log(10)")
    
    # Calculate and Dictate Button
    dictate_btn = st.button("🔊 Calculate & Dictate Answer")
    
    if expr or dictate_btn:
        display_text, speech_val = ev_scientific_calc(expr)
        st.markdown(f"<div class='glass-panel'><h4 style='color:#38BDF8;'>{display_text}</h4></div>", unsafe_allow_html=True)
        
        if dictate_btn and speech_val:
            speak_response(f"The dictated answer is {speech_val}")

# --- TAB 2: DAILY WORD PUZZLE ARCADE ---
with tab_game:
    today_index = date.today().timetuple().tm_yday % len(DAILY_PUZZLES)
    puzzle = DAILY_PUZZLES[today_index]
    
    st.markdown(f"""
    <div class='glass-panel'>
        <h3>🧩 Today's Daily Offline Word Puzzle</h3>
        <p style='color:#94A3B8;'>Date: {date.today().strftime('%A, %B %d, %Y')}</p>
        <p style='font-size: 1.1rem;'>Unscramble these letters to form a 5-letter daily word:</p>
        <h1 style='letter-spacing: 8px; color: #38BDF8; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 12px; text-align: center;'>{puzzle['scramble']}</h1>
        <p><b>Clue:</b> <i>"{puzzle['clue']}"</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    user_guess = st.text_input("Your Answer:", key="puzzle_guess", placeholder="Type your 5-letter word here").strip().upper()
    
    if user_guess:
        if user_guess == puzzle['word']:
            st.success("🎉 Correct! You solved today's word puzzle!")
            speak_response("Awesome job! You solved today's puzzle.")
        else:
            st.error("Incorrect. Try again or check the Answer Key section below!")

    # --- ANSWER KEY SECTION ---
    st.markdown("---")
    with st.expander("🔑 Answer Key & Solution Section"):
        st.write(f"**Letter Hint:** {puzzle['hint']}")
        if st.button("Reveal Solution"):
            st.info(f"The answer for today's puzzle is: **{puzzle['word']}**")
