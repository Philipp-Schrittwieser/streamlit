import streamlit as st
import pandas as pd
from apps.teacher.pages.kahoot.example_text import example_text
from apps.teacher.llms.gpt.generate_quiz_gpt import generate_quiz_gpt
from apps.teacher.llms.gemini.generate_quiz_gemini import generate_quiz_gemini
from apps.teacher.webscraping.return_transcript import return_transcript

import time

st.title("Kahoot Testgenerator💡", anchor=False)

st.subheader("Text oder YouTube-Link einfügen...", divider="blue", anchor=False)
st.write("Du kannst einen Text einfügen, um dein Kahoot zu generieren oder einen YouTube-Link, aus dem dein Quiz kreiert wird. Wenn Untertitel zu deinem Video vorhanden sind, kann ein Quiz erstellt werden.")

if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False

if 'user_youtube_link' not in st.session_state:
    st.session_state.user_youtube_link = ""

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

# Generator Tab
if st.session_state.questions_generated == False:
    left, right = st.columns(2, gap="large")

    with left:
        st.subheader("Option A: Text einfügen", divider="violet", anchor=False)
        user_text = st.text_area("Text hier einfügen:", height=68, value=example_text)

    with right:
        st.subheader("Option B: Link einfügen", divider="green", anchor=False)
        user_youtube_link = st.text_input("YouTube-Link hier einfügen:")
        st.session_state.user_youtube_link = user_youtube_link
        # subtitles_text = get_subtitles_text("https://www.youtube.com/watch?v=ZCvTtb80wEY")

    num_questions = st.selectbox("Anzahl zu generierende Fragen", [5, 10, 15, 20, 25, 30, 35, 40], index=1)

    with st.expander("Erweiterte Einstellungen anzeigen"):
        time_limit = st.selectbox("Zeitlimit in Sekunden", [15, 30, 60, 90, 120], index=1)
        ai_model = st.selectbox("KI-Modell", ["Open Creator", "Genius AI"], index=0)

    st.write("")
    
    if st.button(label="Fragen generieren :material/laps:", key="button-blue"):
            if st.session_state.user_youtube_link != "":
                user_text = return_transcript(st.session_state.user_youtube_link)
                print(user_text)

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
        file_name="kahoot_fragen.csv",
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
        st.session_state.questions_generated = False
        st.toast("App wird neu gestartet... 🏁")
        time.sleep(0.5)
        st.rerun()

        

