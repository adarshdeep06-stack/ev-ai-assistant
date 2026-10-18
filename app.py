import streamlit as st
import streamlit.components.v1 as components
import math
import re

# --- 1. PAGE CONFIGURATION & LIQUID GLASS STYLING ---
st.set_page_config(page_title="EV Offline Assistant", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    /* Dark Liquid Glass Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c20, #15102a, #060212);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .ev-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=1)

# --- 2. OFFLINE SCIENTIFIC CALCULATOR ENGINE ---
def ev_scientific_calc(query: str):
    """Parses text/speech input for scientific operations completely offline."""
    q = query.lower().strip()
    
    # Mathematical Constants & Aliases
    safe_dict = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sqrt': math.sqrt, 'log': math.log10, 'ln': math.log,
        'exp': math.exp, 'pi': math.pi, 'e': math.e,
        'factorial': math.factorial, 'radians': math.radians,
        'degrees': math.degrees, 'pow': math.pow, 'abs': abs
    }
    
    # Natural language query replacements
    clean_q = re.sub(r'square root of ([0-9.]+)', r'sqrt(\1)', q)
    clean_q = re.sub(r'log of ([0-9.]+)', r'log(\1)', clean_q)
    clean_q = re.sub(r'sin of ([0-9.]+)', r'sin(radians(\1))', clean_q)
    clean_q = re.sub(r'cos of ([0-9.]+)', r'cos(radians(\1))', clean_q)
    clean_q = re.sub(r'tan of ([0-9.]+)', r'tan(radians(\1))', clean_q)
    clean_q = clean_q.replace('x', '*').replace('^', '**')
    clean_q = re.sub(r'[^0-9\.\+\-\*\/\(\)\,\s\a-z\_]', '', clean_q)
    
    try:
        # Safe mathematical evaluation
        res = eval(clean_q, {"__builtins__": None}, safe_dict)
        if isinstance(res, float):
            res = round(res, 6)
        return f"Calculated Result: {res}", str(res)
    except Exception:
        return "I am operating in offline mode. Enter a scientific calculation (e.g., 'sqrt(144)', 'sin(45)', '2^8').", None

# --- 3. VOICE SYNTHESIS HELPER ---
def speak_response(text):
    """Uses client-side browser speech synthesis (Works completely offline)."""
    clean_text = text.replace("'", "\\'")
    html_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.rate = 1.0;
        msg.pitch = 1.1;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(html_code, height=0, width=0)

# --- 4. APP LAYOUT ---
st.markdown("<h1 class='ev-header'>🤖 EV: Offline Assistant & Arcade</h1>", unsafe_allow_html=1)

tab_calc, tab_game = st.tabs(["🧮 Scientific Calculator", "🎮 Jewel Match Game"])

# --- TAB 1: SCIENTIFIC CALCULATOR ---
with tab_calc:
    st.markdown("<div class='glass-card'><h3>EV Voice & Scientific Math Engine</h3><p>Supported operations: sin, cos, tan, sqrt, log, ln, power (^), factorials, constants (pi, e).</p></div>", unsafe_allow_html=1)
    
    # Quick Input Reference Buttons
    col_a, col_b, col_c, col_d = st.columns(4)
    if col_a.button("sqrt(144)"): st.session_state['user_input'] = "sqrt(144)"
    if col_b.button("sin(45 degrees)"): st.session_state['user_input'] = "sin of 45"
    if col_c.button("log(100)"): st.session_state['user_input'] = "log(100)"
    if col_d.button("factorial(5)"): st.session_state['user_input'] = "factorial(5)"
    
    user_query = st.text_input("Speak or Type expression for EV:", key="user_input", placeholder="e.g. 15 * log(50) or sqrt(256)")
    
    if user_query:
        response_text, result_val = ev_scientific_calc(user_query)
        st.markdown(f"<div class='glass-card'><h4>EV Response:</h4><p style='font-size: 1.3rem; color: #00d2ff;'>{response_text}</p></div>", unsafe_allow_html=1)
        if result_val:
            speak_response(f"The result is {result_val}")

# --- TAB 2: EMBEDDED HTML5 MATCH-3 GAME ---
with tab_game:
    st.markdown("<div class='glass-card'><h3>EV Arcade: Match-3 Gem Crusher</h3><p>Click two adjacent tiles to swap them and match 3 or more in a row!</p></div>", unsafe_allow_html=1)
    
    # Complete, Standalone HTML5/JS Match-3 Game Canvas
    game_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; background: transparent; text-align: center; color: white; font-family: sans-serif; }
        #canvas { background: rgba(0,0,0,0.5); border-radius: 12px; border: 2px solid #3a7bd5; cursor: pointer; }
        .score-board { font-size: 20px; margin-bottom: 10px; font-weight: bold; color: #00d2ff; }
    </style>
    </head>
    <body>
    <div class="score-board">Score: <span id="score">0</span></div>
    <canvas id="canvas" width="320" height="320"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const grid = 8, size = 40;
        const colors = ['#ff4d4d', '#33dd33', '#3399ff', '#ffcc00', '#cc66ff'];
        let board = [], score = 0, selected = null;

        function init() {
            for(let r=0; r<grid; r++) {
                board[r] = [];
                for(let c=0; c<grid; c++) board[r][c] = Math.floor(Math.random()*colors.length);
            }
            draw();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for(let r=0; r<grid; r++) {
                for(let c=0; c<grid; c++) {
                    ctx.fillStyle = colors[board[r][c]];
                    ctx.beginPath();
                    ctx.arc(c*size + size/2, r*size + size/2, size/2 - 4, 0, Math.PI*2);
                    ctx.fill();
                    if(selected && selected.r === r && selected.c === c) {
                        ctx.strokeStyle = '#ffffff';
                        ctx.lineWidth = 3;
                        ctx.stroke();
                    }
                }
            }
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const c = Math.floor((e.clientX - rect.left) / size);
            const r = Math.floor((e.clientY - rect.top) / size);
            
            if(!selected) {
                selected = {r, c};
            } else {
                let dr = Math.abs(selected.r - r), dc = Math.abs(selected.c - c);
                if((dr === 1 && dc === 0) || (dr === 0 && dc === 1)) {
                    let temp = board[selected.r][selected.c];
                    board[selected.r][selected.c] = board[r][c];
                    board[r][c] = temp;
                    checkMatches();
                }
                selected = null;
            }
            draw();
        });

        function checkMatches() {
            let matched = false;
            for(let r=0; r<grid; r++) {
                for(let c=0; c<grid-2; c++) {
                    let val = board[r][c];
                    if(val !== -1 && val === board[r][c+1] && val === board[r][c+2]) {
                        board[r][c] = board[r][c+1] = board[r][c+2] = -1;
                        score += 30; matched = true;
                    }
                }
            }
            if(matched) {
                document.getElementById('score').innerText = score;
                setTimeout(() => {
                    for(let r=0; r<grid; r++)
                        for(let c=0; c<grid; c++)
                            if(board[r][c] === -1) board[r][c] = Math.floor(Math.random()*colors.length);
                    draw();
                }, 300);
            }
        }
        init();
    </script>
    </body>
    </html>
    """
    components.html(game_code, height=400)
