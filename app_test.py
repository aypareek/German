import streamlit as st
import yaml
import os

st.set_page_config(page_title="Clear B1 Exam with Ayush", page_icon="🇩🇪", layout="centered")

# --- Minimal sidebar style: only set background for compatibility
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background: #fafbfc !important;
        color: #222 !important;
    }
    .flashcard { background: #fffbe8 !important; color: #222 !important; border-radius: 14px; width:100%; max-width:650px; margin:auto;}
    .quiz-block { background: #e6eaff !important; color: #222 !important; border-radius: 14px; width:100%; max-width:650px; margin:auto;}
    .scoretag { background: #d0ffd0 !important; color: #185a18 !important; }
    .stButton>button { background: #1957ba; color: #fff; border-radius: 8px; font-size: 1.09em; }
    .stButton>button:hover { background: #174a9e;}
    .feedback-animate { animation: fadein 0.6s; }
    @keyframes fadein { from { opacity: 0; } to { opacity: 1; } }
    body, .stApp { font-size: 1.05em !important; font-family: 'Segoe UI', 'Arial', sans-serif !important; }
    @media (max-width: 1100px) {
        .stRadio [role="radiogroup"] { flex-direction: column !important; }
        .stButton>button { font-size: 1.07em !important; }
        .flashcard, .quiz-block { padding: 1em 0.8em !important; font-size: 1.02em !important; }
        .scoretag { font-size: 1em !important; }
        h1, h2, h3 { font-size: 1.13em !important; }
    }
    @media (max-width: 700px) {
        .stRadio [role="radiogroup"] { flex-direction: column !important; }
        .stButton>button { font-size: 1em !important; }
        .flashcard, .quiz-block { padding: 0.6em 0.3em !important; font-size: 0.97em !important; }
        h1, h2, h3 { font-size: 1em !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Welcome Banner (shows once per session) ---
if "welcomed" not in st.session_state:
    st.session_state.welcomed = False
if not st.session_state.welcomed:
    st.markdown(
        """
        <div style='background:#e6eaff;border-left:6px solid #1957ba; padding:1.2em 1em; border-radius:14px; margin-bottom:1.2em; box-shadow:0 1px 4px #1957ba22'>
        <h2 style='margin:0 0 0.3em 0;color:#1957ba;'>👋 Welcome to Clear B1 Exam with Ayush!</h2>
        <ul style='margin:0.5em 0 0 1.2em; font-size:1.1em;'>
          <li>Pick a topic on the left (sidebar).</li>
          <li>Try the quizzes, flip flashcards, and practice speaking.</li>
          <li>Click the “FAQ” tab for tips & help at any time.</li>
        </ul>
        <div style='font-size:1em; color:#555;margin-top:0.6em;'>You’ll see this only once per session.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state.welcomed = True

# ---------- Sidebar ----------
st.sidebar.markdown('<span style="color:#1957ba;font-size:1.2em;"><b>Navigation</b></span>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] button[kind="secondary"] {
        background: linear-gradient(90deg,#e66465,#1957ba 80%);
        color: #fff !important;
        font-weight: bold;
        font-size: 1.14em;
        padding-top: 0.7em; padding-bottom: 0.7em;
        border-radius: 22px;
        margin-bottom: 1.3em;
        margin-top: 1.2em;
        border: none;
        transition: background 0.18s, box-shadow 0.13s;
        box-shadow: 0 1.5px 8px #1957ba22;
    }
    div[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: linear-gradient(90deg,#1957ba,#e66465 80%);
        color: #fff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if st.sidebar.button("Alles zurücksetzen/Reset", key="reset_button"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
# --- Profile/Settings: Name entry + personalized greeting ---
with st.sidebar.expander("👤 Profil / Einstellungen"):
    user_name = st.text_input("Dein Name (optional):", value=st.session_state.get("user_name", ""))
    if user_name:
        st.session_state["user_name"] = user_name
        st.markdown(f"Hallo, **{user_name}**! 👋")
    else:
        st.session_state["user_name"] = ""

# ---------- YAML LOAD ----------
@st.cache_resource
def load_content():
    path = "grammar_content.yaml"
    if not os.path.exists(path):
        st.error(f"Missing YAML file: {path}")
        st.stop()
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        st.error("YAML root should be a dictionary (mapping topics to content).")
        st.stop()
    return data

content = load_content()
topics = list(content.keys())

topic = st.sidebar.selectbox("Wähle ein Thema", topics)

with st.sidebar.expander("❓ Mini-FAQ / Hilfe", expanded=False):
    st.markdown("""
    - **Was bedeutet 'nicht'?**  
      → Negation, e.g. "Ich komme nicht." = "I'm not coming."
    - **Was ist der Unterschied zwischen 'kein' und 'nicht'?**  
      → 'kein' negates nouns: "Ich habe kein Geld."  
      → 'nicht' negates verbs/adjectives: "Ich arbeite nicht."
    - **Wie bilde ich Fragen?**  
      → Verb first: "Gehst du ins Kino?"
    - **Wie funktioniert die App?**  
      → Wähle ein Thema, mache das Quiz, lerne mit Flashcards.
    """)

st.sidebar.markdown(
    """
    <div style='text-align:center;margin-top:2em;'>
      <a href="https://www.paypal.com/paypalme/ayushpareek1990" target="_blank"
         style="background:#ffd700;padding:11px 24px;border-radius:24px;color:#222;font-weight:700;text-decoration:none;font-size:1.07em;box-shadow:0 1px 4px #3332;">
         ☕️ Buy me a coffee
      </a>
      <div style="color:#aaa; font-size:0.9em; margin-top:0.4em;">Support helps keep this app free!<br></div>

    </div>
    """, unsafe_allow_html=True
)

if "progress" not in st.session_state:
    st.session_state.progress = {t: {"quizzes": 0, "flashcards": 0} for t in topics}
all_quizzes = sum(len(content[t].get("quizzes", [])) for t in topics)
total_done = sum(
    sum(
        1 for idx, q in enumerate(content[t].get("quizzes", []))
        if st.session_state.get(f"{t}_quiz_{idx}_checked", False)
    ) for t in topics
)

compact_mode = st.sidebar.checkbox("🗜️ Kompakt-Modus", value=False)
if compact_mode:
    st.markdown(
        """
        <style>
        .flashcard, .quiz-block { padding: 0.5em 0.4em !important; font-size: 0.92em !important; }
        .stButton>button { padding: 0.35em 0.7em !important; font-size: 0.93em !important; }
        </style>
        """, unsafe_allow_html=True
    )

if st.session_state.get("user_name"):
    st.markdown(
        f"<div style='text-align:center; margin-bottom:0.7em;font-size:1.15em;color:#1957ba;'>Welcome, <b>{st.session_state['user_name']}</b>!</div>",
        unsafe_allow_html=True
    )

data = content[topic]

quiz_count = len(data.get("quizzes", []))
quiz_done = sum(
    1 for idx in range(quiz_count)
    if (
        st.session_state.get(f"{topic}_quiz_{idx}_checked", False)
        or st.session_state.get(f"{topic}_quiz_{idx}", None) is not None
    )
)
if quiz_count > 0:
    percent = int(100 * quiz_done / quiz_count) if quiz_count else 0
    st.markdown(
        f"""
        <div style='background:#f7f8fb;padding:0.6em 0 0.4em 0;margin-bottom:0.5em;border-bottom:1px solid #e6eaff;'>
            <span style='font-weight:bold;font-size:1.08em;color:#1957ba;vertical-align:middle;'>🧠 Quiz-Fortschritt:</span>
            <br style="display:none;"><!-- Line break for mobile -->
            <div style='display:inline-block;vertical-align:middle;width:54%;max-width:140px;height:1em;background:#e6eaff;border-radius:8px;overflow:hidden;margin:0 1em 0 1em;'>
                <div style='height:100%;width:{percent}%;background:#1957ba;border-radius:8px;transition:width 0.3s;'></div>
            </div>
            <span style='font-size:1.08em;color:#1957ba;vertical-align:middle;'>{quiz_done} / {quiz_count}</span>
        </div>
        """,
        unsafe_allow_html=True
    )



tab_options = [
    ("📝 Erklärung", "explanation"),
    ("🧠 Quiz", "quiz"),
    ("🃏 Flashcards", "flashcards"),
    ("🎤 Sprechen", "speaking"),
    ("❓ FAQ", "faq")
]
tab_labels = [label for label, val in tab_options]
tab_vals = [val for label, val in tab_options]
tab_index = st.radio("Bereich auswählen:", tab_labels, index=0)
selected_tab = tab_vals[tab_labels.index(tab_index)]

if selected_tab == "explanation":
    st.markdown('<hr style="border: none; border-top: 2px solid #1957ba; margin: 2em 0 1em 0;">', unsafe_allow_html=True)
    st.markdown("### 📝 Erklärung")
    st.markdown(data.get("explanation", ""))

if selected_tab == "quiz":
    quizzes = data.get("quizzes", [])
    st.markdown('<hr style="border: none; border-top: 2px solid #1957ba; margin: 2em 0 1em 0;">', unsafe_allow_html=True)
    st.markdown("### 🧠 Quiz")
    num_correct = 0
    for idx, q in enumerate(quizzes):
        blockid = f"{topic}_quiz_{idx}"
        st.markdown('<div class="quiz-block">', unsafe_allow_html=True)
        st.markdown(f"**{idx+1}. {q.get('question','') }**")
        quiz_radio = st.radio(
            "",  # No label, just options
            q.get("options", []),
            key=blockid,
            index=None,
        )
        answer_given_key = f"{blockid}_checked"
        exp_key = f"{blockid}_exp"
        if quiz_radio is not None:
            if not st.session_state.get(answer_given_key, False):
                st.session_state[answer_given_key] = True
            if quiz_radio == q.get("answer"):
                st.markdown('<div class="feedback-animate">', unsafe_allow_html=True)
                st.success("✅ Richtig! 🎉 Super gemacht! 🥳")
                st.markdown('</div>', unsafe_allow_html=True)
                num_correct += 1
            else:
                st.markdown('<div class="feedback-animate">', unsafe_allow_html=True)
                st.error("❌ Falsch. Versuch's nochmal! 😅")
                st.markdown('</div>', unsafe_allow_html=True)
            if st.toggle("💡 Lösung/Erklärung anzeigen", key=exp_key, value=False):
                st.markdown(f"**Erklärung:** {q.get('explanation','')}")
        if "grammar_hint" in q:
            with st.expander("📖 Show me grammar for this sentence"):
                st.markdown(q["grammar_hint"])
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='scoretag'>Quiz-Ergebnis: {num_correct}/{len(quizzes)} "
        + ("🏅" if num_correct == len(quizzes) and len(quizzes) > 0 else "")
        + "</div>",
        unsafe_allow_html=True
    )
    if quizzes and num_correct == len(quizzes) and len(quizzes) > 0:
        st.balloons()
        st.markdown(
            "<div style='color:#185a18;font-size:1.25em;text-align:center;margin:1em 0 1em 0;'>🎉 Glückwunsch! Du hast alle Fragen richtig beantwortet! 🎉</div>",
            unsafe_allow_html=True
        )

if selected_tab == "flashcards":
    flashcards = data.get("flashcards", [])
    st.markdown('<hr style="border: none; border-top: 2px solid #1957ba; margin: 2em 0 1em 0;">', unsafe_allow_html=True)
    st.markdown("### 🃏 Flashcards")
    if flashcards:
        flash_idx_key = f"{topic}_flash_idx"
        flash_flip_key = f"{topic}_flash_flip"
        if flash_idx_key not in st.session_state:
            st.session_state[flash_idx_key] = 0
        if flash_flip_key not in st.session_state:
            st.session_state[flash_flip_key] = False
        idx = st.session_state[flash_idx_key]
        card = flashcards[idx]
        front = str(card.get('front', '') or '').strip()
        back = str(card.get('back', '') or '').strip()
        if front or back:
            if not st.session_state[flash_flip_key]:
                st.markdown(
                    f"<div class='flashcard'><b>{front if front else '[Kein Text auf der Vorderseite]'}</b></div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='flashcard' style='background:#e7fff4;'><b style='color:#185a18'>{back if back else '[Kein Text auf der Rückseite]'}</b></div>",
                    unsafe_allow_html=True
                )
                show_exp = st.toggle("💡 Erklärung anzeigen", key=f"{topic}_flash_exp_{idx}", value=False)
                if show_exp and back:
                    st.info(back)
            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                if st.button("⬅️", key=f"{topic}_flash_prev"):
                    st.session_state[flash_idx_key] = (idx - 1) % len(flashcards)
                    st.session_state[flash_flip_key] = False
                    st.rerun()
            with col2:
                if not st.session_state[flash_flip_key]:
                    if st.button("Antwort zeigen", key=f"{topic}_flash_show"):
                        st.session_state[flash_flip_key] = True
                        st.rerun()
                else:
                    if st.button("Nächste Karte", key=f"{topic}_flash_next"):
                        st.session_state[flash_idx_key] = (idx + 1) % len(flashcards)
                        st.session_state[flash_flip_key] = False
                        st.rerun()
            with col3:
                st.markdown(
                    f"<div class='cardnum'>Karte <b>{idx+1}</b> von {len(flashcards)}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("Diese Flashcard hat keinen Inhalt.")
    else:
        st.info("Für dieses Thema gibt es keine Flashcards.")

if selected_tab == "speaking" and topic == "SpeakingTrainer":
    st.markdown('<hr style="border: none; border-top: 2px solid #1957ba; margin: 2em 0 1em 0;">', unsafe_allow_html=True)
    st.markdown("### 🎤 Sprechen")
    tasks = data.get("speaking_tasks", [])
    if tasks:
        st.markdown("### Sprechübung auswählen:")
        task_titles = [f"{i+1}. {task['prompt']}" for i, task in enumerate(tasks)]
        selected_idx = st.selectbox("Wähle eine Aufgabe:", list(range(len(tasks))), format_func=lambda i: task_titles[i])
        selected_task = tasks[selected_idx]
        st.markdown(f"#### Deine Aufgabe:\n\n**{selected_task['prompt']}**")
        st.markdown("**Lade eine Aufnahme von deiner Antwort hoch (mp3/wav):**")
        audio_file = st.file_uploader("Deine Aufnahme", type=["mp3", "wav"])
        if audio_file is not None:
            st.audio(audio_file, format="audio/wav")
            st.success("Deine Antwort wurde hochgeladen und kann angehört werden.")
        else:
            st.info("Nimm deine Antwort auf deinem Handy oder PC auf, und lade die Datei hier hoch!")
        st.markdown("**Musterantwort:**")
        st.info(selected_task['model_answer'])
        st.markdown("---")
        st.markdown("💡 **Tipp:** Sprich frei, benutze Redemittel und höre dir die Musterlösung an.")

if selected_tab == "faq":
    st.markdown('<hr style="border: none; border-top: 2px solid #1957ba; margin: 2em 0 1em 0;">', unsafe_allow_html=True)
    st.markdown("### ❓ FAQ")
    st.markdown("""
    - **Was bedeutet 'nicht'?**  
      → Negation, e.g. "Ich komme nicht." = "I'm not coming."
    - **Was ist der Unterschied zwischen 'kein' und 'nicht'?**  
      → 'kein' negates nouns: "Ich habe kein Geld."  
      → 'nicht' negates verbs/adjectives: "Ich arbeite nicht."
    - **Wie bilde ich Fragen?**  
      → Verb first: "Gehst du ins Kino?"
    - **Wie funktioniert die App?**  
      → Wähle ein Thema, mache das Quiz, lerne mit Flashcards.
    """)

st.markdown(
    """
    <div style='text-align:center; margin: 2em 0 1em 0;'>
      <a href="https://www.paypal.com/paypalme/ayushpareek1990" target="_blank"
         style="background:#ffd700;padding:13px 28px;border-radius:26px;color:#222;font-weight:700;text-decoration:none;font-size:1.19em;box-shadow:0 1px 6px #3332;">
         ☕️ Buy me a coffee on PayPal
      </a>
      <div style="color:#888; font-size:1em; margin-top:0.5em;">
        This project is 100% free for the community.<br>Support = more features for everyone!
      </div>
    </div>
    """, unsafe_allow_html=True
)
st.markdown(
    """
    <hr style='margin:2rem 0'>
    <div style='text-align:center; color: #888; font-size:1em;'>
        Made with ❤️ by Ayush • Powered by Streamlit & YAML <br>
        For the best experience, please use Google Chrome <br>
        <a style='color:#1957ba;text-decoration:underline;margin:0 0.9em;' href='https://www.telc.net/sprachpruefungen/deutsch/zertifikat-deutsch-telc-deutsch-b1/' target='_blank'>Official telc B1 Info</a> |
        <a style='color:#1957ba;text-decoration:underline;margin:0 0.9em;' href='mailto:ayushpareek1608@gmail.com'>Email</a> |
        <a style='color:#1957ba;text-decoration:underline;margin:0 0.9em;' href='https://github.com/aypareek' target='_blank'>GitHub</a> |
        <a style='color:#1957ba;text-decoration:underline;margin:0 0.9em;' href='https://www.linkedin.com/in/ayushbi/' target='_blank'>LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)
