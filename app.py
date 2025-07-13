import streamlit as st
import yaml
import os

st.set_page_config(page_title="Clear B1 Exam with Ayush", page_icon="🇩🇪", layout="centered")

# --- Always-light, mobile/tablet-optimized style ---
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"], [data-testid="stSidebar"] {
        background: #fafbfc !important;
        color: #222 !important;
    }
    section[data-testid="stSidebar"] *, [data-testid="stSidebar"] * {
        background: #fafbfc !important;
        color: #222 !important;
    }
    .flashcard { background: #fffbe8 !important; color: #222 !important; border-radius: 14px; width:100% !important; max-width:650px; margin:auto;}
    .quiz-block { background: #e6eaff !important; color: #222 !important; border-radius: 14px; width:100% !important; max-width:650px; margin:auto;}
    .scoretag { background: #d0ffd0 !important; color: #185a18 !important; }
    .stButton>button { background: #1957ba; color: #fff; border-radius: 8px; font-size: 1.09em; }
    .stButton>button:hover { background: #174a9e;}
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

st.markdown(
    """
    <div style="text-align:center; margin-bottom:1.2rem">
        <h1 style="color:#1957ba;font-size:2.5em;">🇩🇪 Clear B1 Exam with Ayush</h1>
        <p style="font-size:1.15em; color: #444;">
            <b>Smarter German B1 prep:</b> grammar, vocab, quizzes, flashcards & mock tests. <br>
            <span style="font-size:0.97em; color: #1957ba;">Let’s clear your B1 exam – together!</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

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

# ---------- Sidebar ----------
st.sidebar.title("Themen (Topics)")
topic = st.sidebar.selectbox("🔎 Wähle ein Thema", topics)

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
# --- Buy me a coffee sidebar button ---
st.sidebar.markdown(
    """
    <div style='text-align:center;margin-top:2em;'>
      <a href="https://www.paypal.com/paypalme/ayushpareek1990" target="_blank"
         style="background:#ffd700;padding:11px 24px;border-radius:24px;color:#222;font-weight:700;text-decoration:none;font-size:1.07em;box-shadow:0 1px 4px #3332;">
         ☕️ Buy me a coffee
      </a>
      <div style="color:#aaa; font-size:0.9em; margin-top:0.4em;">Support helps keep this app free!</div>
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
st.sidebar.markdown(
    f"""
    <div style='font-size:1.1em; padding-top:0.2em'>
    <b>📈 Gesamt-Quiz-Fortschritt:</b><br>
    <progress value="{total_done}" max="{all_quizzes}" style="width:100%;height:1.1em;"></progress>
    <span style="color:#1957ba;font-size:1.09em">{total_done} / {all_quizzes}</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# -------------- TAB SELECTOR (vertical for all screens) --------------
tab_choice = st.radio(
    "Bereich auswählen:",
    ("Erklärung", "Quiz", "Flashcards", "Sprechen", "FAQ"),
    index=0
)

data = content[topic]

# -------------- ERKLÄRUNG --------------
if tab_choice == "Erklärung":
    st.markdown(data.get("explanation", ""))

# -------------- QUIZ --------------
if tab_choice == "Quiz":
    quizzes = data.get("quizzes", [])
    if quizzes:
        st.markdown("<h3 style='color:#1957ba;margin-top:1em;'>🧠 Quiz</h3>", unsafe_allow_html=True)
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
                    st.success("✅ Richtig! 🎉 Super gemacht! 🥳")
                    st.progress(100)
                    num_correct += 1
                else:
                    st.error("❌ Falsch. Versuch's nochmal! 😅")
                    st.progress(10)
                if st.toggle("💡 Lösung/Erklärung anzeigen", key=exp_key, value=False):
                    st.markdown(f"**Erklärung:** {q.get('explanation','')}")
            # --- CONTEXTUAL GRAMMAR HELPER ---
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
    else:
        st.info("Für dieses Thema gibt es kein Quiz.")

# -------------- FLASHCARDS --------------
if tab_choice == "Flashcards":
    flashcards = data.get("flashcards", [])
    if flashcards:
        st.markdown("<h3 style='color:#1957ba;margin-top:1.2em;'>🃏 Flashcards</h3>", unsafe_allow_html=True)
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

# -------------- SPEAKING TRAINER --------------
if tab_choice == "Sprechen" and topic == "SpeakingTrainer":
    st.markdown("<h3>🎤 Sprechen üben</h3>", unsafe_allow_html=True)
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

# -------------- FAQ Section --------------
if tab_choice == "FAQ":
    st.markdown("<h3>❓ Mini-FAQ</h3>", unsafe_allow_html=True)
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

# -------------- Main page Buy Me a Coffee button --------------
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

# -------------- Footer --------------
st.markdown(
    "<hr style='margin:2rem 0'>"
    "<div style='text-align:center; color: #888; font-size:1em;'>"
    "Made with ❤️ by Ayush • Powered by Streamlit & YAML • <a style='color:#1957ba;text-decoration:underline' href='https://www.telc.net/en/candidates/language-examinations/tests/german/b1.html' target='_blank'>Official telc B1 Info</a>"
    "</div>",
    unsafe_allow_html=True
)
