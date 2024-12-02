import streamlit as st
import time
import pandas as pd
from apps.teacher.llms.gemini.generate_1_text_gemini import generate_1_text_gemini
from apps.teacher.llms.gemini.generate_2_qas_gemini import generate_2_qas_gemini
from apps.teacher.reset_apps import reset_apps
from apps.teacher.create_documents.create_word import create_document_for_genius_ai, create_combined__exercise_document, format_questions_and_answers
from apps.teacher.pages.kahoot.example_text import example_text

# st.subheader("1️⃣. Lesetext mit KI generieren")
# st.subheader("2️⃣. Fragen mit KI generieren (Schüler)")
# st.subheader("3️⃣. Antworten mit KI generieren (Lehrer)")

def show_generate_popup(type):
  st.success(f"Generiere {type}... ⛏️")
  st.toast(f"KI generiert {type}... 💡")
  time.sleep(1)
  st.toast("Bitte warte einen kurzen Moment ⏰ ")

def show_finish_popup():
  st.balloons()
  time.sleep(0.75)
  st.rerun()

def show_download_popup(type):
  st.toast(f"{type} wurde heruntergeladen ✅ ")
  time.sleep(1)
  st.toast("Du kannst es dir rechts oben im Browser ansehen! 🌎")

def show_restart_popup():
  st.toast("App wird neu gestartet... 🏁")
  time.sleep(0.5)


## Setzt bei Wechsel alles zurück
if st.session_state.current_page != "apps/teacher/pages/exercise_sheet/exercise_sheet.py":    
  reset_apps()
  st.session_state.current_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"


if "exercise_sheet_level" not in st.session_state:
  st.session_state.exercise_sheet_level = "1_text"

if "response" not in st.session_state:
  st.session_state.response = ""

if "current_page" not in st.session_state:
  st.session_state.current_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"

left, right = st.columns([15, 1], gap="small", vertical_alignment="center")
left.title("Arbeitsblatt Generator 📝", anchor=False)

# st.write("Diese Seite ist gerade im Umbau 🚧")

if st.session_state.exercise_sheet_level == "2_qas":
  if right.button(":material/arrow_back:", use_container_width=False):
    show_restart_popup()
    reset_apps()
    st.rerun()

st.text("")

if st.session_state.exercise_sheet_level == "1_text":
  one, two, three = st.columns(3)
  one.markdown("<h4>1️⃣. <u>Lesetext</u> 📖", unsafe_allow_html=True)
  two.markdown("<h4>2️⃣. Aufgaben", unsafe_allow_html=True)
  three.markdown("<h4>3️⃣. Download", unsafe_allow_html=True)

if st.session_state.exercise_sheet_level == "2_qas":
  one, two, three = st.columns(3)
  one.markdown("<h4>1️⃣. Lesetext", unsafe_allow_html=True)
  two.markdown("<h4>2️⃣. <u>Aufgaben</u> ⁉️", unsafe_allow_html=True)
  three.markdown("<h4>3️⃣. Download", unsafe_allow_html=True)

if st.session_state.exercise_sheet_level == "3_answers":
  one, two, three = st.columns(3)
  one.markdown("<h4>1️⃣. Lesetext", unsafe_allow_html=True)
  two.markdown("<h4>2️⃣. Aufgaben", unsafe_allow_html=True)
  three.markdown("<h4>3️⃣. <u>Download</u> 💾 ", unsafe_allow_html=True)

st.text("")

if st.session_state.exercise_sheet_level == "1_text":
  st.subheader("1. Lesetext einfügen oder generieren...", divider="blue", anchor=False)
  st.write("Möchtest du einen Text einfügen, aus dem dein Arbeitsblatt erstellt wird (Möglichkeit A) oder soll ein komplett neuer Text für dich generiert werden (Möglichkeit B)?")
  st.write("Tippe dein Thema unterhalb ein und dann wähle Option A oder B.")

  st.text("")

  topic = st.text_input("Thema eintippen:", placeholder="z.B. Klimawandel")
  st.session_state.topic = topic

  st.text("")

  left, mid, right = st.columns([6,1,6], gap="small")

  with left:
    st.subheader("A: Text einfügen", divider="violet", anchor=False)
    topic_text = st.text_area("Text hier einfügen:", placeholder=example_text, height=95, max_chars=60000)
    st.write("")
    st.session_state.response = topic_text

    if st.button(label="Fortfahren :material/arrow_right_alt:", key="button-blue", use_container_width=True):
      
      if st.session_state.topic == "":
        st.toast("Thema fehlt :exclamation:")
        st.error("Bitte Thema eingeben :exclamation:")
        time.sleep(0.5)
      
      if st.session_state.response == "":
        st.toast("Text fehlt :exclamation:")
        st.error("Bitte Text einfügen :exclamation:")

      if st.session_state.topic != "" and st.session_state.response != "":
        st.session_state.response = topic_text
        st.session_state.exercise_sheet_level = "2_qas"
        st.rerun()

    with right:
      st.subheader("B: Text generieren", divider="green", anchor=False)
      st.write("Text generieren lassen:")

      with st.expander("Erweiterte Einstellungen"):
        #dropdown für KI-Modelle
        st.session_state.ai_model = st.selectbox("KI-Modell", ["Genius AI", "Genius AI Pro"])

      if st.button(label="Lesetext generieren :material/laps:", key="button-blue2", use_container_width=True):
        
        if st.session_state.topic == "":
          st.toast("Thema fehlt :exclamation:")
          st.error("Bitte Thema eingeben :exclamation:")

        else:
          show_generate_popup("Lesetext")

          with st.spinner(''):
            selected_ai_model = st.session_state.ai_model

            if selected_ai_model == "Max Creator":
              # response = generate_1_text_gpt(topic)
              pass
            elif selected_ai_model == "Genius AI":
              response = generate_1_text_gemini(model_name="gemini-1.5-flash", topic=topic)

            elif selected_ai_model == "Genius AI Pro":
              response = generate_1_text_gemini(model_name="gemini-1.5-pro", topic=topic)
              
              if response == "error": 
                print("Trying again with flash model")
                response = generate_1_text_gemini(model_name="gemini-1.5-flash", topic=topic)

            else:
              st.error("Kein gültiges KI-Modell ausgewählt :exclamation:")
              
            if response != "error":
              st.session_state.response = response
              st.session_state.exercise_sheet_level = "2_qas"
              show_finish_popup()

            else:
              st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut - eventuell mit einem anderen Thema...")
              st.button("Ok")

elif st.session_state.exercise_sheet_level == "2_qas":
  st.subheader("2. Aufgaben und Lösungen erstellen...", divider="violet", anchor=False)

  st.write("Dein Lesetext ist im Dropdown-Menü verfügbar. Klicke jetzt auf den Button darunter, um Aufgaben und Lösungen zu deinem Text zu erstellen.")

  number_questions = st.selectbox("Anzahl zu generierender Fragen", [3, 5, 7, 10, 12, 15, 20, 25, 30, 40], index=3)

  with st.expander("Lesetext hier ansehen"):
    st.write(st.session_state.response)

  left, right = st.columns(2, gap="large")

  with left:
    if st.button(label="Aufgaben generieren :material/laps:", key="button-blue", use_container_width=True):
      show_generate_popup("Aufgaben und Lösungen")

      with st.spinner(''):
        selected_ai_model = st.session_state.ai_model

        if selected_ai_model == "Max Creator":
          # qas = generate_2_qas_gpt(st.session_state.response)
          pass
        elif selected_ai_model == "Genius AI":
          qas = generate_2_qas_gemini(model_name="gemini-1.5-flash", input_text=st.session_state.response, number_questions=number_questions)

        elif selected_ai_model == "Genius AI Pro":
          qas = generate_2_qas_gemini(model_name="gemini-1.5-pro", input_text=st.session_state.response, number_questions=number_questions)

          if qas == "error":
            print("Trying again with flash model")
            qas = generate_2_qas_gemini(model_name="gemini-1.5-flash", input_text=st.session_state.response, number_questions=number_questions)

        else:
          st.error("Kein gültiges KI-Modell ausgewählt :exclamation:")
        
        if qas != "error":
          st.session_state.qas = qas
          st.session_state.exercise_sheet_level = "3_answers"
          show_finish_popup()

        else:
          st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut...")
          st.button("Ok")

elif st.session_state.exercise_sheet_level == "3_answers":
  st.subheader("3. Alle Unterlagen herunterladen...", divider="green", anchor=False)

  st.write('Hier kannst du noch einmal alle Dokumente einsehen und wenn du zufrieden bist einfach herunterladen. Wenn du noch ein Arbeitsblatt generieren möchtest, klicke einfach auf "Neu starten".')

  with st.expander("Generierter Lesetext"):
    st.write(st.session_state.response)
  
  with st.expander("Generierte Aufgaben"):
 
    for i, qa in enumerate(st.session_state.qas, 1):
      st.markdown(f"### **{i}. {qa['question']}**")
      st.markdown(f"{qa['answer']}")

    lines = "\n\n\u200B\n\n_________________________________________________________________________________________________________\n\n\u200B\n\n_________________________________________________________________________________________________________\n\n\u200B\n\n"
    fragen, lösungen = format_questions_and_answers(st.session_state.topic, st.session_state.qas, lines)
    
    st.session_state.fragen = fragen
    st.session_state.lösungen = lösungen



  lesetext_filename = f"{st.session_state.topic}_Lesetext.docx"
  lesetext_bio = create_document_for_genius_ai(st.session_state.response)

  fragen_filename = f"{st.session_state.topic}_Fragen.docx"
  fragen_bio = create_document_for_genius_ai(st.session_state.fragen)

  lösungen_filename = f"{st.session_state.topic}_Lösungen.docx"
  lösungen_bio = create_document_for_genius_ai(st.session_state.lösungen)


  combined_bio = create_combined__exercise_document(
    st.session_state.response,
    st.session_state.fragen,
    st.session_state.lösungen
  )

  with st.expander("Einzelne Dokumente"):
    st.write("Hier kannst du die Dokumente einzeln herunterladen:")
    one, two, three = st.columns(3)

    one.download_button(
        use_container_width=True,
        label="Lesetext :material/download:",
        data=lesetext_bio.getvalue(),
        file_name=lesetext_filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    two.download_button(
        use_container_width=True,
        label="Fragen :material/download:",
        data=fragen_bio.getvalue(),
        file_name=fragen_filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    three.download_button(
        use_container_width=True,
        label="Lösungen :material/download:",
        data=lösungen_bio.getvalue(),
        file_name=lösungen_filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

  left, right = st.columns(2, gap="large")

  with left:
    if st.download_button(
        label="Gesamtes Dokument herunterladen :material/download:",
        data=combined_bio.getvalue(),
        file_name=f"{st.session_state.topic}_Alle_Unterlagen.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    ):
      show_download_popup("Dokument")

  with right:
    if st.button(label="Neu starten :material/restart_alt:", use_container_width=True):
      show_restart_popup()
      reset_apps()
      st.rerun()

  # if st.button("Ok"):
  #   st.rerun()