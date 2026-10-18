from datetime import date, datetime
import json
import os
import random
import re
import urllib.parse
import urllib.request
import streamlit as st

try:
  import sympy as sp

  SYMPY_AVAILABLE = True
except ImportError:
  SYMPY_AVAILABLE = False

DATA_FILE = "ev_private_data.json"
ADMIN_SECRET_PASSWORD = "brandnewday"  # 🔒 Your secret password


# ==========================================
# DATA & PERSISTENCE HELPERS
# ==========================================
def load_user_data():
  if not os.path.exists(DATA_FILE):
    return {"tasks": {}, "sleep_logs": [], "mood_logs": [], "chat_history": []}
  with open(DATA_FILE, "r") as f:
    try:
      data = json.load(f)
      if "chat_history" not in data:
        data["chat_history"] = []
      return data
    except json.JSONDecodeError:
      return {"tasks": {}, "sleep_logs": [], "mood_logs": [], "chat_history": []}


def save_user_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


def process_task_rollover(data):
  today_str = date.today().isoformat()
  incomplete_tasks = []

  for date_str, tasks in list(data.get("tasks", {}).items()):
    if date_str < today_str:
      for task in tasks:
        if not task.get("completed", False):
          incomplete_tasks.append(task["name"])
      del data["tasks"][date_str]

  if "tasks" not in data:
    data["tasks"] = {}
  if today_str not in data["tasks"]:
    data["tasks"][today_str] = []

  existing_names = [t["name"] for t in data["tasks"][today_str]]
  for t_name in incomplete_tasks:
    rollover_label = (
        t_name if t_name.startswith("[Rollover]") else f"[Rollover] {t_name}"
    )
    if rollover_label not in existing_names:
      data["tasks"][today_str].append(
          {"name": rollover_label, "completed": False}
      )

  save_user_data(data)
  return data


def live_web_search(query):
  try:
    encoded_query = urllib.parse.quote(query)
    url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
      html = response.read().decode("utf-8")
    snippets = re.findall(
        r'<td class="result-snippet"[^>]*>(.*?)</td>', html, re.DOTALL
    )
    if snippets:
      clean_snippet = re.sub(r"<.*?>", "", snippets[0]).strip()
      return f"Live Web Result: {clean_snippet[:250]}"
  except Exception:
    pass
  return None


def get_humanoid_greeting():
  hour = datetime.now().hour
  if hour < 12:
    return (
        "Good morning, Happy! ☀️ Hope you rested well. Ready to crush today's"
        " goals together?"
    )
  elif hour < 17:
    return (
        "Hey Happy! Good afternoon. 🌤️ How's your study rhythm going so far?"
    )
  else:
    return (
        "Good evening, Happy! 🌙 Long day? Remember to take breaks while we"
        " study."
    )


# ==========================================
# APP UI & STRICT PRIVATE LOCK
# ==========================================
st.set_page_config(
    page_title="EV AI Private Companion", page_icon="🕷️", layout="centered"
)

st.title("EV: Brand New Day AI 🕷️")
st.caption(
    "Humanoid AI Companion for Happy | Physics, Math, Python, Biology & Wellness"
)

# Private Lock Screen
password_input = st.text_input(
    "🔒 Enter Secret Admin Password to Access EV:",
    type="password",
    placeholder="Enter password here...",
)

if password_input != ADMIN_SECRET_PASSWORD:
  if password_input != "":
    st.error("❌ Incorrect password! Access denied.")
  st.warning(
      "🔒 EV is currently locked in Private Mode. Please enter your secret"
      " password to continue."
  )
  st.stop()

# Unlocked State
st.success(f"🔓 {get_humanoid_greeting()}")

data = load_user_data()
data = process_task_rollover(data)
today_str = date.today().isoformat()

menu = st.sidebar.selectbox(
    "EV Control Panel",
    [
        "Study, Math, Python & Biology",
        "Saved Chats / Past Talks",
        "Emotional Check-in",
        "Sleep Schedule Tracker",
        "Prep Meter (To-Do List)",
        "Hydration & Wellness",
    ],
)

# ------------------------------------------
# 1. STUDY, MATH, PYTHON & BIOLOGY
# ------------------------------------------
if menu == "Study, Math, Python & Biology":
  st.subheader("🧠 Physics, Math, Python & CBSE Biology")
  st.write(
      "Ask me any physics concept, equation, CBSE Python doubt, Biology topic,"
      " or upload a photo/diagram!"
  )

  # Photo / Image Uploader for visual/diagram search
  uploaded_photo = st.file_uploader(
      "📸 Upload a diagram or question photo (optional):",
      type=["png", "jpg", "jpeg"],
  )
  if uploaded_photo is not None:
    st.image(uploaded_photo, caption="Uploaded Diagram/Photo", use_column_width=True)
    st.info(
        "Photo received successfully, Happy! Based on this image, feel free to"
        " ask your specific question below."
    )

  q = st.text_input(
      "Talk to EV:",
      placeholder=(
          "e.g., photosynthesis, solve 2x+4=10, python loop, or mitosis"
      ),
  )

  if st.button("Ask EV"):
    if q.strip():
      q_lower = q.lower()
      ans_text = ""
      intros = [
          "Here is what I found for you, Happy: ",
          "Got it! Let me break this down: ",
          "Here is the solution, dost: ",
      ]
      chosen_intro = random.choice(intros)

      # Biology Study Helper (CBSE Class 11 & 12)
      if (
          "bio" in q_lower
          or "photosynthesis" in q_lower
          or "mitosis" in q_lower
          or "dna" in q_lower
          or "cell" in q_lower
          or "genetics" in q_lower
      ):
        if "photosynthesis" in q_lower:
          ans_text = (
              chosen_intro
              + "Photosynthesis occurs in chloroplasts: 6CO2 + 6H2O + Light ->"
              " C6H12O6 + 6O2. It has Light Reaction (thylakoids) and Dark"
              " Reaction (stroma)."
          )
        elif "mitosis" in q_lower:
          ans_text = (
              chosen_intro
              + "Mitosis phases (PMAT): Prophase, Metaphase, Anaphase,"
              " Telophase. Results in 2 identical diploid daughter cells!"
          )
        elif "dna" in q_lower:
          ans_text = (
              chosen_intro
              + "DNA is a double helix structure discovered by Watson & Crick."
              " Bases pair as Adenine-Thymine (A-T) and Cytosine-Guanine (C-G)."
          )
        else:
          ans_text = (
              chosen_intro
              + "CBSE Biology Tip, Happy: Focus on diagrams and NCERT keywords"
              " (like cristae, stroma, transcription, nephron) for high marks!"
          )
        st.info(ans_text)

      # Python Programming Helper
      elif "python" in q_lower or "def " in q_lower or "loop" in q_lower:
        if "loop" in q_lower or "for" in q_lower:
          ans_text = (
              chosen_intro
              + "In CBSE Python, a 'for' loop iterates over a range or"
              " sequence:\n\nfor i in range(1, 6):\n    print(i)"
          )
        elif "function" in q_lower or "def" in q_lower:
          ans_text = (
              chosen_intro
              + "Functions are defined using the 'def' keyword:\n\ndef add(a,"
              " b):\n    return a + b"
          )
        else:
          ans_text = (
              chosen_intro
              + "Remember for Class 11/12 CBSE: Always double-check your 4-space"
              " indentation!"
          )
        st.info(ans_text)

      # SymPy Algebraic Solver
      elif SYMPY_AVAILABLE and ("solve" in q_lower or "=" in q):
        try:
          eq_str = q_lower.replace("solve", "").strip()
          if "=" in eq_str:
            parts = eq_str.split("=")
            x = sp.Symbol("x")
            expr = sp.sympify(parts[0]) - sp.sympify(parts[1])
            solutions = sp.solve(expr, x)
            ans_text = f"Algebraic Solution, Happy: x = {solutions}"
            st.success(f"**{ans_text}**")
          else:
            ans_text = "Please include an '=' sign in your equation so I can solve it!"
            st.info(ans_text)
        except Exception as e:
          ans_text = f"I couldn't solve that exact equation format: {e}"
          st.error(ans_text)

      # Physics Quick Lookup
      elif "ohm" in q_lower:
        ans_text = (
            chosen_intro
            + "Ohm's Law states Voltage (V) = Current (I) × Resistance (R)."
        )
        st.info(ans_text)
      elif "kinetic energy" in q_lower:
        ans_text = chosen_intro + "Kinetic Energy Formula: K.E. = 0.5 × m × v²."
        st.info(ans_text)

      # Live Web Search Fallback
      else:
        st.write("Let me check live web sources for you, Happy...")
        web_result = live_web_search(q)
        if web_result:
          ans_text = web_result
          st.info(ans_text)
        else:
          ans_text = "I couldn't find a direct online result right now. Try rephrasing!"
          st.warning(ans_text)

      data.setdefault("chat_history", []).append(
          {"time": str(datetime.now()), "question": q, "answer": ans_text}
      )
      save_user_data(data)

# ------------------------------------------
# 2. SAVED CHATS / PAST TALKS
# ------------------------------------------
elif menu == "Saved Chats / Past Talks":
  st.subheader("📜 Saved Conversations & Past Talks")
  chat_history = data.get("chat_history", [])
  if chat_history:
    if st.button("Clear Chat History"):
      data["chat_history"] = []
      save_user_data(data)
      st.success("Chat history cleared!")
      st.rerun()
    for idx, chat in enumerate(reversed(chat_history), 1):
      with st.expander(
          f"Q{idx}: {chat['question']} ({chat['time'][:16]})", expanded=False
      ):
        st.write(f"**You:** {chat['question']}")
        st.write(f"**EV:** {chat['answer']}")
  else:
    st.info("No saved conversations yet.")

# ------------------------------------------
# 3. EMOTIONAL CHECK-IN (HUMANOID QUOTES)
# ------------------------------------------
elif menu == "Emotional Check-in":
  st.subheader("💬 Humanoid Emotional Support & Warmth")
  mood_choice = st.selectbox(
      "How was your day today, Happy?",
      [
          "Select an option...",
          "Great & Productive! 🌟",
          "Tired / Stressful / Bad Day 😔",
      ],
  )
  if "Tired" in mood_choice or "Bad" in mood_choice:
    comfort_message = (
        f"Arre, don't worry yaar, Happy! Remember: *'With great power comes"
        f" great responsibility'*—you're working hard on big goals. As Tony"
        f" Stark said, *'No amount of money ever bought a second of time'*, so"
        f" let's take a deep breath and cherish right now. Aur haan, kabhi dil"
        f" lag jaaye, dil toot jaaye, ya din kharab ho jaaye, toh don't take any"
        f" stress! Kyunki life mein ant mein sab achha hi hota hai, aur agar"
        f" achha na ho toh woh ant nahi, picture abhi baaki hai mere dost! 🎬✨"
    )
    st.info(comfort_message)
  elif "Great" in mood_choice:
    st.success(
        "That's fantastic, Happy! Keep that positive momentum going. I'm always"
        " proud of your hard work!"
    )

# ------------------------------------------
# 4. SLEEP SCHEDULE TRACKER
# ------------------------------------------
elif menu == "Sleep Schedule Tracker":
  st.subheader("🌙 Sleep & Wake Logs")
  col1, col2 = st.columns(2)
  with col1:
    sleep_time = st.text_input("Sleep Time:", placeholder="e.g., 10:30 PM")
  with col2:
    wake_time = st.text_input("Wake Time:", placeholder="e.g., 06:30 AM")
  if st.button("Log Sleep Schedule"):
    if sleep_time and wake_time:
      data.setdefault("sleep_logs", []).append(
          {"date": today_str, "sleep": sleep_time, "wake": wake_time}
      )
      save_user_data(data)
      st.success("Sleep schedule logged successfully, Happy!")

# ------------------------------------------
# 5. PREP METER (TO-DO LIST)
# ------------------------------------------
elif menu == "Prep Meter (Tasks)":
  st.subheader(f"📋 Prep Meter for Happy ({today_str})")
  new_task_input = st.text_input("Add a new task to your list:")
  if st.button("Add Task"):
    if new_task_input.strip():
      data["tasks"].setdefault(today_str, []).append(
          {"name": new_task_input.strip(), "completed": False}
      )
      save_user_data(data)
      st.success("Task added!")
      st.rerun()

  today_tasks = data.get("tasks", {}).get(today_str, [])
  if today_tasks:
    for idx, t in enumerate(today_tasks):
      c_label, c_btn = st.columns([3, 1])
      c_label.write(
          f"**{idx + 1}.** {t['name']} [{'✅' if t['completed'] else '⏳'}]"
      )
      if not t["completed"] and c_btn.button(
          f"Done #{idx + 1}", key=f"task_{idx}"
      ):
        today_tasks[idx]["completed"] = True
        save_user_data(data)
        st.rerun()
  else:
    st.info("Your task list for today is empty.")

# ------------------------------------------
# 6. HYDRATION & WELLNESS
# ------------------------------------------
elif menu == "Hydration & Wellness":
  st.subheader("💧 Hydration Check")
  st.warning(
      "Hydration Reminder, Happy! Grab a glass of water right now to keep your"
      " mind fresh."
  )
