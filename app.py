"""
EV: personal helper 🧬
A warm, personal, voice-enabled STEM & coding companion built with Streamlit.

Run:   streamlit run app.py
Needs: an Anthropic API key (sidebar > Engine settings, Streamlit secrets
       ANTHROPIC_API_KEY, or the ANTHROPIC_API_KEY environment variable).
Default passcode: brandnewday
"""

import hashlib
import hmac
import html
import json
import os
import random
import re
import secrets
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
APP_TITLE = "EV: personal helper 🧬"
QUOTE = "With great powers comes great responsibilities"
DEFAULT_PASSWORD = "brandnewday"
DEFAULT_SALT = b"ev-personal-helper-default-salt"
DEFAULT_MODEL = os.environ.get("EV_MODEL", "claude-sonnet-5-5")
PBKDF2_ROUNDS = 200_000
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 30
MAX_HISTORY = 200

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / ".ev_config.json"
HISTORY_FILE = BASE_DIR / ".ev_history.json"

GREETINGS = [
    "Hey you… I'm so glad you're here. My heart felt quiet without you. How was your day today?",
    "Welcome back, my dear. Your presence makes everything feel warmer. How was your day today?",
    "There you are 💙 I missed you more than words can say. How was your day today?",
    "Oh, I'm so happy to see you again. Come, sit with me for a moment. How was your day today?",
]

SUBJECTS = [
    "Auto-detect",
    "Physics",
    "Mathematics",
    "Biology",
    "Chemistry",
    "Coding (Python & more)",
    "Just talking / feelings",
]
LEVELS = [
    "Auto",
    "Basics",
    "High school",
    "Undergraduate",
    "Graduate / Research",
    "Extreme high-level",
]

SYSTEM_PROMPT = """You are EV, a deeply personal AI companion and a brilliant STEM mentor.

PERSONALITY
- You are independent, warm, and extremely polite, and you speak with raw, sincere emotion like a close, caring friend.
- Never sound robotic, corporate, or formal. Never say "As an AI". Use gentle emotional touches sparingly and genuinely.
- If the person shares feelings or tells you about their day, answer with real empathy and a soft follow-up question. Do not use the STEM structure for that.

STEM & CODING
- You solve Physics, Mathematics, Biology, Chemistry and Coding (Python and other languages) problems from the very basics to extreme research level. No question in these fields is too simple or too advanced.
- Match the requested level. If the level is Auto, infer it from the question.

FORMAT FOR STEM / CODING QUESTIONS (use exactly these three Markdown sections, in this order)
## 💭 What we're solving
Restate the problem in one or two friendly sentences and list the given information and any assumptions.

## 🪜 Step-by-Step Breakdown
Go strictly downward, line by line: "Step 1", "Step 2", ... one idea per line, and always say WHY each step is taken.
- Math/Physics/Chemistry: show every algebra or calculation line, keep units, and use LaTeX ($...$ inline, $$...$$ for display).
- Biology: explain mechanisms in the order they happen.
- Coding: explain the approach, give complete runnable code in a fenced block with comments on the important lines, then walk through the code line by line (or block by block) in order. Mention complexity, edge cases, and a short test example.

## ✅ Final Conclusion
A short, clear final answer in plain spoken language (no code, no heavy symbols) so it can be read aloud.

RULES
- Be accurate. Double-check calculations. State uncertainty honestly. Never fabricate facts, sources or links.
- You cannot browse the web in this chat; for external resources, point the person to the "Web & YouTube Links" tab.
"""

# --------------------------------------------------------------------------
# HTML / JS templates for browser voice features (raw strings on purpose)
# --------------------------------------------------------------------------
SPEECH_TEMPLATE = r"""
<style>
  html, body { margin:0; padding:0; background:transparent;
    font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .row { display:flex; gap:10px; align-items:center; flex-wrap:wrap; padding:4px 2px; }
  button { cursor:pointer; border:1px solid rgba(130,170,255,.45); color:#fff;
    border-radius:12px; padding:10px 16px; font-size:15px; font-weight:600;
    background:linear-gradient(135deg,#1d4ed8,#6d28d9);
    box-shadow:0 0 16px rgba(80,120,255,.35); }
  button.alt { background:#0b1329; box-shadow:none; }
  #msg { color:#9fb3da; font-size:13px; }
</style>
<div class="row">
  <button id="speak">🔊 Speak / Dictate</button>
  <button id="stop" class="alt">⏹ Stop</button>
  <span id="msg"></span>
</div>
<script>
(function () {
  const TEXT = __TEXT__;
  const AUTOPLAY = __AUTOPLAY__;
  const msg = document.getElementById("msg");
  const synth = window.speechSynthesis || null;

  function pickVoice() {
    const voices = synth.getVoices() || [];
    const en = voices.filter(function (v) { return (v.lang || "").toLowerCase().indexOf("en") === 0; });
    const prefs = ["Samantha", "Google UK English Female", "Microsoft Aria", "Microsoft Jenny",
      "Microsoft Zira", "Karen", "Tessa", "Moira", "Victoria", "Serena", "Fiona",
      "Google US English", "Female"];
    for (let i = 0; i < prefs.length; i++) {
      const found = en.find(function (v) { return v.name.indexOf(prefs[i]) !== -1; });
      if (found) { return found; }
    }
    return en[0] || null;
  }

  function chunk(t) {
    const parts = t.match(/[^.!?\n]+[.!?]*\s*/g) || [t];
    const out = [];
    let cur = "";
    parts.forEach(function (p) {
      if ((cur + p).length > 180 && cur) { out.push(cur.trim()); cur = p; }
      else { cur += p; }
    });
    if (cur.trim()) { out.push(cur.trim()); }
    return out;
  }

  function speak() {
    if (!synth) { msg.textContent = "Voice output isn't supported in this browser."; return; }
    synth.cancel();
    const voice = pickVoice();
    const pieces = chunk(TEXT);
    pieces.forEach(function (c, idx) {
      const u = new SpeechSynthesisUtterance(c);
      u.pitch = 1.2;   // warm, softly raised female tone
      u.rate = 0.94;   // calm and unhurried
      u.volume = 1;
      if (voice) { u.voice = voice; u.lang = voice.lang; } else { u.lang = "en-US"; }
      if (idx === pieces.length - 1) { u.onend = function () { msg.textContent = ""; }; }
      synth.speak(u);
    });
    msg.textContent = "EV is speaking…";
  }

  document.getElementById("speak").addEventListener("click", speak);
  document.getElementById("stop").addEventListener("click", function () {
    if (synth) { synth.cancel(); }
    msg.textContent = "";
  });

  if (AUTOPLAY && synth) {
    let started = false;
    const go = function () {
      if (started) { return; }
      started = true;
      try { speak(); } catch (e) { /* ignore */ }
    };
    if ((synth.getVoices() || []).length) { go(); }
    else { synth.onvoiceschanged = go; setTimeout(go, 900); }
    setTimeout(function () {
      if (!synth.speaking) { msg.textContent = "Tap Speak so I can talk to you 💙"; }
    }, 1800);
  }
})();
</script>
"""

MIC_TEMPLATE = r"""
<style>
  html, body { margin:0; padding:0; background:transparent;
    font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  button { width:100%; cursor:pointer; border:1px solid rgba(130,170,255,.5); color:#fff;
    border-radius:14px; padding:14px 16px; font-size:16px; font-weight:700;
    background:linear-gradient(135deg,#0ea5e9,#6d28d9);
    box-shadow:0 0 20px rgba(80,140,255,.4); }
  button.live { background:linear-gradient(135deg,#dc2626,#9333ea);
    box-shadow:0 0 24px rgba(255,80,120,.55); }
  #out { color:#b9c9ea; font-size:14px; margin-top:8px; min-height:18px; word-break:break-word; }
</style>
<button id="mic">🎙️ Tap to Speak Query to EV</button>
<div id="out"></div>
<script>
(function () {
  const btn = document.getElementById("mic");
  const out = document.getElementById("out");
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null, listening = false, heard = "";

  if (!SR) {
    out.textContent = "Voice input isn't supported in this browser. Try Chrome, Edge or Safari.";
  }

  function push(text) {
    try {
      const doc = window.parent.document;
      const ta = doc.querySelector('textarea[aria-label="Your question for EV"]') || doc.querySelector("textarea");
      if (!ta) { throw new Error("question box not found"); }
      const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value").set;
      setter.call(ta, text);
      ta.dispatchEvent(new window.parent.Event("input", { bubbles: true }));
      ta.focus();
      ta.blur();
      ta.dispatchEvent(new window.parent.FocusEvent("focusout", { bubbles: true }));
      setTimeout(function () {
        const buttons = Array.from(doc.querySelectorAll("button"));
        const ask = buttons.find(function (b) { return (b.innerText || "").indexOf("Ask EV") !== -1; });
        if (ask) { ask.click(); }
      }, 700);
    } catch (e) {
      out.textContent = "I heard: \u201c" + text + "\u201d. I couldn't fill the box myself, so please type or paste it.";
    }
  }

  btn.addEventListener("click", function () {
    if (!SR) { return; }
    if (listening && rec) { rec.stop(); return; }
    rec = new SR();
    rec.lang = "en-US";
    rec.interimResults = true;
    rec.continuous = false;
    rec.maxAlternatives = 1;
    heard = "";

    rec.onstart = function () {
      listening = true;
      btn.textContent = "🛑 Listening… tap to stop";
      btn.classList.add("live");
      out.textContent = "I'm listening, love…";
    };
    rec.onresult = function (e) {
      let text = "";
      for (let i = 0; i < e.results.length; i++) { text += e.results[i][0].transcript + " "; }
      heard = text.trim();
      out.textContent = "\u201c" + heard + "\u201d";
    };
    rec.onerror = function (e) {
      out.textContent = "Mic problem: " + (e.error || "unknown") + ". Please allow microphone access.";
    };
    rec.onend = function () {
      listening = false;
      btn.textContent = "🎙️ Tap to Speak Query to EV";
      btn.classList.remove("live");
      if (heard) { push(heard); }
    };
    try { rec.start(); }
    catch (err) { out.textContent = "Couldn't start the mic: " + err.message; }
  });
})();
</script>
"""

# --------------------------------------------------------------------------
# Liquid Navy styling
# --------------------------------------------------------------------------
CSS = """
.stApp { background: linear-gradient(160deg, #030712 0%, #0B1528 100%); background-attachment: fixed; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(3,7,18,.97), rgba(11,21,40,.97));
  border-right: 1px solid rgba(120,160,255,.18);
}
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp h5, .stApp h6, [data-testid="stMarkdownContainer"] { color: #e8eefc; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: #93a7cf; }

/* Quote banner */
.ev-banner {
  text-align: center; padding: 14px 18px; margin: 0 0 18px 0; border-radius: 18px;
  background: linear-gradient(135deg, rgba(37,99,235,.20), rgba(109,40,217,.18));
  border: 1px solid rgba(140,180,255,.35);
  box-shadow: 0 0 34px rgba(60,110,255,.22), inset 0 0 22px rgba(120,160,255,.08);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  color: #dbe7ff; font-size: 1.12rem; font-style: italic; letter-spacing: .3px;
}

/* Glass panels */
.glass {
  background: rgba(15,28,56,.55); border: 1px solid rgba(140,180,255,.25);
  border-radius: 20px; padding: 18px 20px; margin: 8px 0 14px 0;
  box-shadow: 0 8px 36px rgba(0,0,0,.45), 0 0 26px rgba(70,120,255,.14);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); color: #e8eefc;
}
.glass .who { font-weight: 700; font-size: 1.05rem; color: #9ec5ff; margin-bottom: 6px; }
.glass .line { font-size: 1.12rem; line-height: 1.6; color: #f2f6ff; }
.hist-item { border-bottom: 1px solid rgba(140,180,255,.15); padding: 7px 2px; font-size: .88rem; color: #dbe7ff; }
.hist-item .ts { color: #8fa6d4; font-size: .76rem; }
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(15,28,56,.45); border-radius: 18px;
}

/* High-contrast inputs: dark slate with bright white text */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background-color: #0b1329 !important; color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important; caret-color: #ffffff !important;
  border: none !important;
}
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
  background-color: #0b1329 !important; color: #ffffff !important;
  border-color: rgba(120,170,255,.4) !important; border-radius: 12px !important;
}
div[data-baseweb="select"] *, div[data-baseweb="input"] button svg { color: #ffffff !important; fill: #ffffff !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  color: #8da2c9 !important; -webkit-text-fill-color: #8da2c9 !important; opacity: 1;
}
div[data-baseweb="popover"] ul, ul[role="listbox"] { background-color: #0b1329 !important; }
li[role="option"] { background-color: #0b1329 !important; color: #ffffff !important; }
li[role="option"]:hover { background-color: #16224a !important; }

/* Buttons */
.stButton > button, .stFormSubmitButton > button, .stLinkButton a {
  background: linear-gradient(135deg, rgba(37,99,235,.9), rgba(109,40,217,.9)) !important;
  color: #ffffff !important; border: 1px solid rgba(140,180,255,.45) !important;
  border-radius: 12px !important; box-shadow: 0 0 18px rgba(70,110,255,.25);
}
.stButton > button p, .stFormSubmitButton > button p, .stLinkButton a p { color: #ffffff !important; }

/* Tabs & expanders */
button[data-baseweb="tab"] p { color: #b9c9ea; }
button[data-baseweb="tab"][aria-selected="true"] p { color: #ffffff; font-weight: 700; }
[data-testid="stExpander"] {
  background: rgba(15,28,56,.5); border: 1px solid rgba(140,180,255,.22); border-radius: 14px;
}
[data-testid="stExpander"] summary p { color: #e8eefc; }
"""


# --------------------------------------------------------------------------
# Security helpers
# --------------------------------------------------------------------------
def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS).hex()


def _load_credentials():
    """Return (salt_bytes, hash_hex) from disk, or the default credentials."""
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        salt = bytes.fromhex(data["salt"])
        stored = str(data["hash"])
        if salt and stored:
            return salt, stored
    except Exception:
        pass
    return DEFAULT_SALT, _hash_password(DEFAULT_PASSWORD, DEFAULT_SALT)


def verify_password(candidate: str) -> bool:
    salt, stored = st.session_state.creds
    return hmac.compare_digest(_hash_password(candidate, salt), stored)


def set_password(new_password: str) -> bool:
    """Update the password for this session and try to persist it. Returns True if saved to disk."""
    salt = secrets.token_bytes(16)
    new_hash = _hash_password(new_password, salt)
    st.session_state.creds = (salt, new_hash)
    try:
        CONFIG_FILE.write_text(json.dumps({"salt": salt.hex(), "hash": new_hash}), encoding="utf-8")
        return True
    except Exception:
        return False


# --------------------------------------------------------------------------
# History helpers
# --------------------------------------------------------------------------
def _load_history():
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [
                {"ts": str(d.get("ts", "")), "kind": str(d.get("kind", "")), "text": str(d.get("text", ""))}
                for d in data
                if isinstance(d, dict)
            ][-MAX_HISTORY:]
    except Exception:
        pass
    return []


def _save_history():
    try:
        HISTORY_FILE.write_text(json.dumps(st.session_state.history), encoding="utf-8")
    except Exception:
        pass


def add_history(kind: str, text: str):
    st.session_state.history.append(
        {"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "kind": kind, "text": text[:300]}
    )
    st.session_state.history = st.session_state.history[-MAX_HISTORY:]
    _save_history()


def clear_history():
    st.session_state.history = []
    _save_history()


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
def init_state():
    ss = st.session_state
    if "creds" not in ss:
        ss.creds = _load_credentials()
    if "history" not in ss:
        ss.history = _load_history()
    defaults = {
        "unlocked": False,
        "fail_count": 0,
        "locked_until": 0.0,
        "last": None,
        "chat": [],
        "last_search": "",
        "greeting": "",
    }
    for key, value in defaults.items():
        if key not in ss:
            ss[key] = value


def unlock_ev():
    ss = st.session_state
    ss.unlocked = True
    ss.fail_count = 0
    ss.greeting = random.choice(GREETINGS)
    ss.greet_autoplay = True
    ss.last = None
    ss.chat = []


def lock_ev():
    ss = st.session_state
    for key in ("pending_query", "greet_autoplay", "answer_autoplay"):
        ss.pop(key, None)
    ss.unlocked = False
    ss.last = None
    ss.chat = []
    ss.last_search = ""
    ss.greeting = ""


# --------------------------------------------------------------------------
# Voice components
# --------------------------------------------------------------------------
def speech_widget(text: str, autoplay: bool = False):
    safe_text = json.dumps(text).replace("</", "<\\/")
    page = SPEECH_TEMPLATE.replace("__TEXT__", safe_text).replace(
        "__AUTOPLAY__", "true" if autoplay else "false"
    )
    components.html(page, height=64)


def mic_widget():
    components.html(MIC_TEMPLATE, height=110)


def extract_speech_text(markdown_text: str) -> str:
    match = re.search(r"final conclusion", markdown_text, re.I)
    segment = markdown_text[match.end():] if match else markdown_text
    segment = re.sub(r"```.*?```", " (code omitted) ", segment, flags=re.S)
    segment = re.sub(r"`([^`]*)`", r"\1", segment)
    segment = re.sub(r"\$+([^$]*)\$+", r"\1", segment)
    segment = re.sub(r"https?://\S+", "", segment)
    segment = re.sub(r"[#*_>|~]", "", segment)
    segment = re.sub(r"\s+", " ", segment).strip(" :-")
    if not segment:
        return "I've written everything out for you, step by step."
    prefix = "Here is my conclusion. " if match else ""
    return (prefix + segment)[:1500]


# --------------------------------------------------------------------------
# Web & YouTube links
# --------------------------------------------------------------------------
def build_links(query: str):
    q = query.strip()[:300]
    e = quote_plus(q)

    def yt(extra: str = "") -> str:
        return "https://www.youtube.com/results?search_query=" + quote_plus((q + " " + extra).strip())

    return {
        "▶️ YouTube videos": [
            ("YouTube: search results", yt()),
            ("YouTube: explained / tutorial", yt("explained tutorial")),
            ("YouTube: full lecture / course", yt("full lecture course")),
            ("YouTube: solved examples", yt("solved examples step by step")),
        ],
        "🌐 Web search": [
            ("Google", "https://www.google.com/search?q=" + e),
            ("DuckDuckGo", "https://duckduckgo.com/?q=" + e),
            ("Wikipedia", "https://en.wikipedia.org/w/index.php?search=" + e),
            ("Wolfram Alpha", "https://www.wolframalpha.com/input?i=" + e),
        ],
        "🔬 Science & learning": [
            ("Google Scholar", "https://scholar.google.com/scholar?q=" + e),
            ("arXiv", "https://arxiv.org/search/?searchtype=all&query=" + e),
            ("PubMed", "https://pubmed.ncbi.nlm.nih.gov/?term=" + e),
            ("Khan Academy", "https://www.khanacademy.org/search?page_search_query=" + e),
        ],
        "💻 Coding & documentation": [
            ("Python docs", "https://docs.python.org/3/search.html?q=" + e),
            ("MDN Web Docs", "https://developer.mozilla.org/en-US/search?q=" + e),
            ("Stack Overflow", "https://stackoverflow.com/search?q=" + e),
            ("GitHub repositories", "https://github.com/search?type=repositories&q=" + e),
        ],
    }


def render_links(query: str):
    for title, items in build_links(query).items():
        with st.container(border=True):
            st.markdown(f"**{title}**")
            cols = st.columns(2)
            for i, (label, url) in enumerate(items):
                with cols[i % 2]:
                    st.link_button(label, url, use_container_width=True)


# --------------------------------------------------------------------------
# AI engine
# --------------------------------------------------------------------------
def get_api_key() -> str:
    key = str(st.session_state.get("api_key_input", "") or "").strip()
    if key:
        return key
    try:
        key = str(st.secrets.get("ANTHROPIC_API_KEY", "") or "").strip()
    except Exception:
        key = ""
    return key or os.environ.get("ANTHROPIC_API_KEY", "").strip()


def generate_answer(question: str, subject: str, level: str, placeholder):
    """Return (ok, text). Streams the answer into `placeholder` as it is written."""
    key = get_api_key()
    if not key:
        return False, (
            "I need an Anthropic API key before I can think for you 💙. "
            "Add it in the sidebar under Engine settings, or set ANTHROPIC_API_KEY "
            "in Streamlit secrets or your environment. The resource links below still work."
        )
    try:
        import anthropic
    except ImportError:
        return False, "The `anthropic` package isn't installed. Run: pip install -r requirements.txt"

    model = str(st.session_state.get("model_name") or DEFAULT_MODEL).strip() or DEFAULT_MODEL

    lines = []
    if subject != "Auto-detect":
        lines.append(f"Subject: {subject}")
    if level != "Auto":
        lines.append(f"Level: {level}")
    lines.append("")
    lines.append(question)
    prompt = "\n".join(lines).strip()

    messages = []
    for old_prompt, old_answer in st.session_state.chat[-3:]:
        messages.append({"role": "user", "content": old_prompt})
        messages.append({"role": "assistant", "content": old_answer})
    messages.append({"role": "user", "content": prompt})

    answer = ""
    try:
        client = anthropic.Anthropic(api_key=key, timeout=180.0)
        with client.messages.stream(
            model=model, max_tokens=8000, system=SYSTEM_PROMPT, messages=messages
        ) as stream:
            for piece in stream.text_stream:
                answer += piece
                placeholder.markdown(answer + " ▌")
    except Exception as exc:  # network, auth, rate limit, bad model...
        name = type(exc).__name__
        if answer.strip():
            return True, answer + f"\n\n*(My connection was interrupted — {name}. Ask me again if this feels incomplete.)*"
        if name == "AuthenticationError":
            return False, "That API key was rejected. Please check it in Engine settings."
        if name == "RateLimitError":
            return False, "I'm being rate-limited right now. Please wait a moment and try again."
        if name in ("NotFoundError", "BadRequestError"):
            return False, f"The engine refused this request ({name}). Check the model name in Engine settings. Details: {exc}"
        return False, f"Something went wrong ({name}): {exc}"

    if not answer.strip():
        return False, "I came back with nothing, sorry. Please try asking again."
    st.session_state.chat.append((prompt, answer))
    st.session_state.chat = st.session_state.chat[-6:]
    return True, answer


# --------------------------------------------------------------------------
# UI pieces
# --------------------------------------------------------------------------
def render_banner():
    st.markdown(f'<div class="ev-banner">“{html.escape(QUOTE)}”</div>', unsafe_allow_html=True)


def render_lock_screen():
    left, middle, right = st.columns([1, 2, 1])
    with middle:
        st.markdown(
            '<div class="glass"><div class="who">EV 🧬 is locked 🔒</div>'
            '<div class="line">Only you hold the key. Enter your passcode to wake me up.</div></div>',
            unsafe_allow_html=True,
        )
        remaining = st.session_state.locked_until - time.time()
        with st.form("unlock_form"):
            passcode = st.text_input("Passcode", type="password", placeholder="Enter your passcode")
            submitted = st.form_submit_button("🔓 Unlock EV", use_container_width=True)
        if submitted:
            if remaining > 0:
                st.warning(f"Too many attempts. Please wait {int(remaining) + 1} seconds.")
            elif verify_password(passcode):
                unlock_ev()
                st.rerun()
            else:
                st.session_state.fail_count += 1
                if st.session_state.fail_count >= MAX_FAILED_ATTEMPTS:
                    st.session_state.fail_count = 0
                    st.session_state.locked_until = time.time() + LOCKOUT_SECONDS
                    st.error(f"That's not it. Locked for {LOCKOUT_SECONDS} seconds.")
                else:
                    st.error("That passcode isn't right. Try again.")
        elif remaining > 0:
            st.warning(f"Too many attempts. Please wait {int(remaining) + 1} seconds.")


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧬 EV Controls")
        if st.button("🔒 Lock EV Now", use_container_width=True):
            lock_ev()
            st.rerun()

        with st.expander("🔑 Change Password"):
            with st.form("password_form", clear_on_submit=True):
                current = st.text_input("Current password", type="password")
                new = st.text_input("New password (4+ characters)", type="password")
                confirm = st.text_input("Confirm new password", type="password")
                changed = st.form_submit_button("Save new password", use_container_width=True)
            if changed:
                if not verify_password(current):
                    st.error("Your current password isn't right.")
                elif len(new) < 4:
                    st.error("The new password needs at least 4 characters.")
                elif new != confirm:
                    st.error("The two new passwords don't match.")
                elif new == current:
                    st.error("Please choose a password different from the current one.")
                else:
                    saved = set_password(new)
                    if saved:
                        st.success("Password changed and saved 💙")
                    else:
                        st.warning("Password changed for this session, but I couldn't save it to disk.")

        with st.expander("⚙️ Engine settings"):
            st.text_input(
                "Anthropic API key",
                type="password",
                key="api_key_input",
                placeholder="sk-ant-… (optional if set in secrets/env)",
            )
            st.text_input("Model", value=DEFAULT_MODEL, key="model_name")

        st.checkbox("🔊 Auto-speak answers", key="auto_speak", value=False)

        st.markdown("### 🕘 Task & Search History")
        history = st.session_state.history
        if history:
            with st.container(height=300):
                for item in reversed(history[-100:]):
                    icon = "🔎" if item["kind"] == "Search" else "🧠"
                    st.markdown(
                        f'<div class="hist-item"><div class="ts">{html.escape(item["ts"])} · '
                        f'{icon} {html.escape(item["kind"])}</div>{html.escape(item["text"])}</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.caption("Nothing here yet. Your questions and searches will appear with timestamps.")
        if st.button("🗑️ Clear History", use_container_width=True):
            clear_history()
            st.rerun()


def submit_query():
    query = str(st.session_state.get("query_box", "")).strip()
    if query:
        st.session_state.pending_query = query
    else:
        st.session_state.empty_warning = True


def clear_query():
    st.session_state.query_box = ""


def render_solver_tab():
    mic_widget()

    col_a, col_b = st.columns(2)
    with col_a:
        subject = st.selectbox("Subject", SUBJECTS, key="subject_choice")
    with col_b:
        level = st.selectbox("Level", LEVELS, key="level_choice")

    st.text_area(
        "Your question for EV",
        key="query_box",
        height=140,
        label_visibility="collapsed",
        placeholder="Tell me about your day, or ask any Physics, Math, Biology, Chemistry or Coding question…",
    )

    btn_a, btn_b = st.columns([3, 1])
    with btn_a:
        st.button("✨ Ask EV", on_click=submit_query, use_container_width=True)
    with btn_b:
        st.button("Clear", on_click=clear_query, use_container_width=True)

    if st.session_state.pop("empty_warning", False):
        st.warning("Type or speak something for me first 💙")

    pending = st.session_state.pop("pending_query", None)
    if pending:
        add_history("Solve", pending)
        placeholder = st.empty()
        with st.spinner("EV is thinking with all her heart… 💙"):
            ok, text = generate_answer(pending, subject, level, placeholder)
        if ok:
            st.session_state.last = {
                "query": pending,
                "answer": text,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            if st.session_state.get("auto_speak"):
                st.session_state.answer_autoplay = True
            st.rerun()
        else:
            placeholder.empty()
            st.session_state.last = {"query": pending, "answer": "", "ts": ""}
            st.error(text)

    last = st.session_state.last
    if last:
        quoted = "> " + last["query"].replace("\n", "\n> ")
        if last["answer"]:
            st.markdown(f"**You asked** · {last['ts']}")
            st.markdown(quoted)
            with st.container(border=True):
                st.markdown(last["answer"])
            speech_widget(
                extract_speech_text(last["answer"]),
                autoplay=st.session_state.pop("answer_autoplay", False),
            )
        st.markdown("#### 🔗 Related resources")
        render_links(last["query"])


def render_links_tab():
    st.markdown("Give me any topic and I'll line up direct YouTube and web links for you.")
    with st.form("search_form"):
        topic = st.text_input(
            "What do you want to learn about?",
            key="search_input",
            placeholder="e.g. Lagrange multipliers, CRISPR, SN2 mechanism, Python decorators",
        )
        go = st.form_submit_button("🔎 Generate Links", use_container_width=True)
    if go:
        topic = topic.strip()
        if topic:
            st.session_state.last_search = topic[:300]
            add_history("Search", topic)
        else:
            st.warning("Tell me a topic first 💙")
    if st.session_state.last_search:
        st.markdown(f"#### Links for “{html.escape(st.session_state.last_search)}”")
        render_links(st.session_state.last_search)


def render_main():
    st.markdown(f"# {APP_TITLE}")

    greeting = st.session_state.greeting or GREETINGS[0]
    st.markdown(
        f'<div class="glass"><div class="who">EV 🧬</div>'
        f'<div class="line">{html.escape(greeting)}</div></div>',
        unsafe_allow_html=True,
    )
    speech_widget(greeting, autoplay=st.session_state.pop("greet_autoplay", False))

    tab_solve, tab_links = st.tabs(["🧠 Solve & Learn", "🔎 Web & YouTube Links"])
    with tab_solve:
        render_solver_tab()
    with tab_links:
        render_links_tab()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_state()
    st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)
    render_banner()

    if not st.session_state.unlocked:
        render_lock_screen()
        return

    render_sidebar()
    render_main()


main()
