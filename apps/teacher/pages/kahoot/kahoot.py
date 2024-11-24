import streamlit as st
import pandas as pd
from apps.teacher.pages.kahoot.example_text import example_text
from apps.teacher.llms.gpt.generate_quiz_gpt import generate_quiz_gpt
from apps.teacher.llms.gemini.generate_quiz_gemini import generate_quiz_gemini
from apps.teacher.webscraping.return_transcript import return_transcript
from apps.teacher.reset_apps import reset_apps

import time

st.title("Kahoot Testgenerator💡", anchor=False)

st.subheader("Text oder YouTube-Link einfügen...", divider="blue", anchor=False)
st.write("Möchtest du aus einem eingefügten Text (Möglichkeit A) oder einem YouTube-Video (Möglichkeit B) ein Kahoot erstellen? Für Option B müssen Untertitel beim Video vorhanden sein.")

st.write("Füge einen Text oder einen YouTube-Link ein und dann drücke auf Fragen generieren.")

if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False

if 'user_youtube_link' not in st.session_state:
    st.session_state.user_youtube_link = ""

if 'user_text' not in st.session_state:
    st.session_state.user_text = ""

if "got_transcript" not in st.session_state:
    st.session_state.got_transcript = False

def generate_questions(user_text, num_questions, time_limit, ai_model):
    st.success("Generiere Fragen... ⛏️")
    st.toast(f"KI generiert Fragen... 💡")
    time.sleep(1)
    st.toast("Bitte warte einen kurzen Moment ⏰ ")

    with st.spinner(''):
        if ai_model == "Open Creator":
            response = generate_quiz_gpt(user_text, num_questions, time_limit)
        elif ai_model == "Genius AI":
            response = generate_quiz_gemini(user_text, num_questions, time_limit)
        else:
            st.error("Kein gültiges KI-Modell ausgewählt :exclamation:")
        st.session_state.response = response
        st.session_state.questions_generated = True
        # st.success("Fertig generiert 🎉🎉🎉")
        st.balloons()
        time.sleep(0.75)
        st.rerun()

def restart_kahoot():
    st.session_state.questions_generated = False
    st.toast("App wird neu gestartet... 🏁")
    time.sleep(0.5)
    reset_apps()
    st.rerun()

## Setzt bei Wechsel alles zurück
if st.session_state.current_page != "apps/teacher/pages/kahoot/kahoot.py":
    reset_apps()
    st.session_state.current_page = "apps/teacher/pages/kahoot/kahoot.py"

# Generator Tab
if st.session_state.questions_generated == False:

    left, mid, right = st.columns([6,1,6], gap="small")

    with left:
        st.subheader("A: Text einfügen", divider="violet", anchor=False)
        # User Text eingefügt
        user_text = st.text_area("Text hier einfügen:", height=68, placeholder=example_text)
        st.session_state.user_text = user_text

    with right:
        st.subheader("B: Link einfügen", divider="green", anchor=False)            
        user_youtube_link = st.text_input("YouTube-Link hier einfügen:",
                                          placeholder="z.B. https://www.youtube.com/watch?v=Nhw-t-RrWk8",
                                          key="user_youtube_link",
                                          )
        st.session_state.got_transcript = return_transcript(user_youtube_link)

        print("API Call: ", st.session_state.got_transcript)
        if st.session_state.got_transcript == False:
            st.write("")    
        elif st.session_state.got_transcript:
            st.success("Untertitel gefunden ✅")
            st.session_state.user_text = st.session_state.got_transcript
        elif st.session_state.got_transcript == None and st.session_state.user_youtube_link != "":
            st.error("Keine Untertitel verfügbar ❌")

    num_questions = st.selectbox("Anzahl zu generierende Fragen", [5, 10, 15, 20, 25, 30, 35, 40], index=3)

    with st.expander("Erweiterte Einstellungen anzeigen"):
        time_limit = st.selectbox("Zeitlimit in Sekunden", [15, 30, 60, 90, 120], index=1)
        ai_model = st.selectbox("KI-Modell", ["Open Creator", "Genius AI"], index=0)

    st.write("")

    left, right = st.columns(2, gap="large")
    
    with left:
        if st.button(label="Fragen generieren :material/laps:", key="button-blue", use_container_width=True):
            
            # Wenn YouTube Link, generiere Fragen aus eingefügten Text
            if st.session_state.user_youtube_link != "" and st.session_state.got_transcript != None:

                # User Text aus YouTube-Link extrahiert
                user_text = st.session_state.user_text
                
                # Schneidet Trankskript automatisch auf max. 60k Zeichen zu
                if len(user_text) > 60000:
                    print("User Text was sliced")
                    user_text = user_text[:60000]
            
            # Error falls keine Untertitel verfügbar
            if st.session_state.user_youtube_link != "" and st.session_state.got_transcript == None:
                st.error("Füge einen korrekten Link ein 🔗")
                st.stop()

            # Error falls kein Text eingefügt
            if st.session_state.user_text == "" and st.session_state.user_youtube_link == "":
                st.error("Füge einen Text 📝 oder einen Link 🔗 ein, um ein Quiz zu generieren...")
                st.stop()

                # Setzt Name aus ersten 2 Wörtern von user_text
            st.session_state.topic = "_".join(user_text.split(" ")[:2])

            # Wenn kein YouTube Link, generiere Fragen aus eingefügten Text
            max_text_length = 60000
            user_text_length = len(user_text)

            # Limit 60k Zeichen
            if user_text_length > max_text_length:
                # Anzeigen der Nachrichten in Streamlit mit Formatierung und Ersetzung in einer Zeile
                st.toast(f"Input-Textlänge: {user_text_length:,}".replace(",", ".") + " Zeichen 🇦")
                st.error(f"Input-Text zu lang :exclamation: **{user_text_length:,}".replace(",", ".") + " Zeichen** ")
                st.error(f"Bitte unter **{max_text_length:,}".replace(",", ".") + " Zeichen** :warning: halten")
                
            else:
                generate_questions(user_text, num_questions, time_limit, ai_model)

# Ergebnis Tab
if st.session_state.questions_generated == True:
    st.header("Ergebnis", anchor=False)
    df = pd.DataFrame(st.session_state.response)
    st.write(df)

    # CSV Buffer erstellen
    csv = df.to_csv(index=False)
        
    col1, col2 = st.columns(spec=2, gap="large")

    # Download Button
    if col1.download_button(
        label="Fragen herunterladen :material/download:",
        data=csv,
        file_name=f"{st.session_state.topic}-kahoot_fragen.csv",
        mime="text/csv",
        key="button-blue2",
        use_container_width=True
    ):
        st.toast("Fragen wurden heruntergeladen ✅ ")
        time.sleep(1)
        st.toast("Du kannst sie dir rechts oben im Browser ansehen! 🌎")

        
    # Neustart Button
    if col2.button(
            label="Neu starten :material/restart_alt:",
            key="button-blue3",
            use_container_width=True
        ):
        restart_kahoot()

