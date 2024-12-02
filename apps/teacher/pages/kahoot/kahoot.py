import streamlit as st
import pandas as pd
from apps.teacher.pages.kahoot.example_text import example_text
# from apps.teacher.llms.gpt.generate_quiz_gpt import generate_quiz_gpt
from apps.teacher.llms.gemini.generate_0_quiz_gemini import generate_0_quiz_gemini
# from apps.teacher.webscraping.return_transcript import return_transcript
from apps.teacher.reset_apps import reset_apps
from helpers import return_current_pagename
from db.db import new_kahoot
import uuid
from io import StringIO, BytesIO
from apps.teacher.animations import show_generate, show_generate_finished, show_donwload_completed, show_restart_app

st.title("Kahoot Generator💡", anchor=False)

if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False
    # st.session_state.questions_generated = True

if 'user_youtube_link' not in st.session_state:
    st.session_state.user_youtube_link = ""

if 'user_text' not in st.session_state:
    st.session_state.user_text = ""

if "got_transcript" not in st.session_state:
    st.session_state.got_transcript = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "apps/teacher/pages/kahoot/kahoot.py"

if "id" not in st.session_state:
    st.session_state.id = ""

if "response" not in st.session_state:
    st.session_state.response = False

if "topic" not in st.session_state:
    st.session_state.topic = ""

def generate_questions(ai_model, user_text, num_questions, time_limi, difficulty):
    show_generate("Fragen")

    with st.spinner(''):

        # Generieren
        if ai_model == "Open Creator":
            # llm_resp = generate_quiz_gpt(user_text, num_questions, time_limit)
            pass
        elif ai_model == "Genius AI":
            llm_resp, llm_error = generate_0_quiz_gemini(model_name="gemini-1.5-flash", user_text=user_text, num_questions=num_questions, time_limit=time_limit, difficulty=difficulty)
        elif ai_model == "Genius AI Pro":
            # nur zur Sicherheit als Umleitung auf Flash, falls Pro aus irgendeinem Grund noch im Session State ist
            llm_resp, llm_error = generate_0_quiz_gemini(model_name="gemini-1.5-flash", user_text=user_text, num_questions=num_questions, time_limit=time_limit, difficulty=difficulty)
        else:
            st.error("Kein gültiges KI-Modell ausgewählt :exclamation:")

        # Error Handling
        if llm_error == False:
            st.session_state.response = llm_resp
            st.session_state.questions_generated = True
            show_generate_finished()
        else:
            st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut - eventuell mit einem anderen Text/Video...")
            st.button("Ok")

def restart_kahoot():
    reset_apps()
    show_restart_app()

## Setzt bei Wechsel alles zurück
if st.session_state.current_page != "apps/teacher/pages/kahoot/kahoot.py":
    reset_apps()
    st.session_state.current_page = "apps/teacher/pages/kahoot/kahoot.py"

# Generator Tab
if st.session_state.questions_generated == False:

    st.subheader("Text einfügen und Quiz generieren...", divider="blue", anchor=False)
    st.write("Unterhalb kannst du einen Text einfügen aus dem Fragen generiert werden sollen.")

    # left, mid, right = st.columns([6,1,6], gap="small")

    # with left:
    # st.subheader("A: Text einfügen", divider="violet", anchor=False)
    # User Text eingefügt
    user_text = st.text_area("Text hier einfügen:", height=95, placeholder=example_text)
    st.session_state.user_text = user_text

    # with right:
    #     st.subheader("B: Link einfügen", divider="green", anchor=False) 
    #     st.write("Gerade im Umbau... 🚧")           

        
    #     user_youtube_link = st.text_input("YouTube-Link hier einfügen:",
    #                                       placeholder="z.B. https://www.youtube.com/watch?v=Nhw-t-RrWk8",
    #                                       key="user_youtube_link",
    #                                       )
        
    #     if user_youtube_link != "":
    #         st.session_state.got_transcript = scrape_youtube_transcript(user_youtube_link)


    #     left, right = st.columns([11,2], gap="small", vertical_alignment="center")
        
    #     with left:
    #         # print("API Call: ", st.session_state.got_transcript)
    #         if st.session_state.got_transcript == False:
    #             st.write("")    
    #         elif st.session_state.got_transcript:
    #             st.success("Untertitel gefunden ✅")
    #             st.session_state.user_text = st.session_state.got_transcript
    #         elif st.session_state.got_transcript == None and st.session_state.user_youtube_link != "":
    #             st.error("Keine Untertitel verfügbar ❌")

    #     right.button(":material/check:")


    num_questions = st.selectbox("Anzahl zu generierender Fragen", [5, 10, 15, 20, 25, 30, 35, 40], index=3)

    with st.expander("Quiz aus YouTube-Video generieren"):
        st.subheader("Quiz aus YouTube-Video generieren:", divider="violet", anchor=False)
        st.write("Wenn du mit den SuS ein YouTube-Video anschauen willst, kannst du daraus auch Fragen generieren. Wir empfehlen dir die Untertitel zu extrahieren und dann in unser Tool einzufügen. Zum Extrahieren nutze diesen Link: [www.youtube-transcript.io](https://www.youtube-transcript.io/) 🔗")
        st.write("Hier findest du eine kurze Video-Anleitung dazu:")
        st.video("https://youtu.be/mvq3y7GtocU")

    with st.expander("Erweiterte Einstellungen anzeigen"):
        
        ai_model = "Genius AI"
        difficulty = st.selectbox("Schwierigkeitsgrad", ["Leicht", "Mittel", "Schwer"], index=1)
        time_limit = st.selectbox("Zeitlimit in Sekunden", [15, 30, 60, 90, 120], index=1)

        # ai_model = st.selectbox("KI-Modell", ["Open Creator", "Genius AI"], index=1)
        # ai_model = st.selectbox("KI-Modell", ["Genius AI", "Genius AI Pro"], index=0)

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
            if st.session_state.topic == "":
                # print(f"User Text Input: {st.session_state.user_text}")
                # Replace alles, was nicht in Dateiname vorkommen darf
                topic_cleaned = st.session_state.user_text.replace('\n', ' ').replace('\t', ' ').replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ').replace('/', ' ').replace('\\', ' ').replace(':', ' ').replace('*', ' ').replace('"', ' ').replace("'", ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ').strip()
                # print(f"Text cleaned: {topic_cleaned}")
                st.session_state.topic = "_".join(topic_cleaned.split(" ")[:2])
                # print(f"Topic: {st.session_state.topic}")

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
                generate_questions(ai_model, user_text, num_questions, time_limit, difficulty)
                st.session_state.user_text = user_text

# Ergebnis Tab
if st.session_state.questions_generated == True:

    st.header("Ergebnis", anchor=False, divider="blue")

        
    st.write("Hier kannst du das Ergebnis als Excel-Dokument herunterladen, deine Fragen neu generieren oder den Link teilen.")
    
        # Wenn response generiert wurde
    if isinstance(st.session_state.response, pd.DataFrame) and not st.session_state.response.empty:
        df = st.session_state.response
        # Speichere alle generierten Quize in DB
        st.session_state.id = str(uuid.uuid4())
        print(f"ID Created: {st.session_state.id}")

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        # Excel Buffer erstellen
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='xlsxwriter')
        excel_data = buffer.getvalue()
        new_kahoot(st.session_state.id, return_current_pagename(st.session_state.current_page), st.session_state.topic, st.session_state.user_text, st.session_state.user_youtube_link, excel_data)

    # Wenn Kahoot from Sharing (aus DB) kommt
    else:
        # print(f"Kahoot from DB: {st.session_state.kahoot['csv']}")
        df = pd.read_csv(StringIO(st.session_state.kahoot['csv']))
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        # Excel Buffer erstellen
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='xlsxwriter')
        excel_data = buffer.getvalue()

    col1, col2 = st.columns(spec=[3,3], gap="medium")
    # Download Button
    if col1.download_button(
        label="Herunterladen :material/download:",
        data=excel_data,
        file_name=f"{st.session_state.topic}-Kahoot_Fragen.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="button-blue2",
        use_container_width=True
    ):
        show_donwload_completed("Fragen")
        
    # Neustart Button
    if col2.button(
            label="Neu starten :material/restart_alt:",
            key="button-blue3",
            use_container_width=True
        ):
        restart_kahoot()

    st.write("######")
    
    st.subheader("Keine Ahnung wie du das Excel in Kahoot hochlädst?", divider="violet", anchor=False)
    st.write("Kein Problem! Schau dir unsere kurze Anleitung unterhalb an:")

    with st.expander("🎥 Video-Anleitung zu Kahoot-Upload"):
        st.video("https://youtu.be/n2KJqiSG7bs")

    
        
    # st.write("######")
    
    # left, mid, right = st.columns(spec=[1,8,1], gap="medium", vertical_alignment="top")

    # with mid:
    #     sharing_link = st.session_state.base_url + "?id=" + st.session_state.id
    #     print(f"ID: {sharing_link}")
    #     st_copy_to_clipboard(
    #         # text="https://ai-school.onrender.com/" + st.session_state.id,
    #     text=sharing_link,
    #     before_copy_label="🔴 Deine Stundenvorbereitung mit einer Kollegin / einem Kollegen teilen 👩‍🏫 👨‍🏫 🔗",
    #     after_copy_label="✔️ Link erfolgreich in Zwischenablage kopiert & bereit zum versenden 👩‍🏫 👨‍🏫 🔗",
    #     show_text=False,
    #     key="button-blue4"
    # )
