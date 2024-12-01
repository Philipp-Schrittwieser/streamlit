import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from apps.teacher.create_documents.create_word import create_document_for_genius_ai, create_combined_grammar_document, format_questions_and_answers
from apps.teacher.reset_apps import reset_apps
from apps.teacher.llms.gemini.generate_3_grammar_gemini import generate_3_grammar_gemini

## Setzt bei Wechsel alles zurück
if st.session_state.current_page != "apps/teacher/pages/grammar_exercise/grammar_exercise.py":    
  reset_apps()
  st.session_state.current_page = "apps/teacher/pages/grammar_exercise/grammar_exercise.py"

if not "response1" in st.session_state:
    st.session_state.response1 = []

if not "response2" in st.session_state:
    st.session_state.response2 = []

if not "grammar_topic" in st.session_state:
    st.session_state.grammar_topic = ""

if not "ai_model" in st.session_state:
    st.session_state.ai_model = ""

if not "number_exercises" in st.session_state:
    st.session_state.number_exercises = 10

if not "grammar_exercise_level" in st.session_state:
    st.session_state.grammar_exercise_level = "1_create"

if not "choice" in st.session_state:
    st.session_state.choice = None


left, right = st.columns([15, 1], gap="small", vertical_alignment="center")

left.title("Grammatik Übung Generator 🔎")

if st.session_state.grammar_exercise_level == "2_show":
  if right.button(":material/arrow_back:", use_container_width=False):
    # show_restart_popup()
    reset_apps()
    st.rerun()

if st.session_state.grammar_exercise_level == "1_create":
  st.subheader("Übung erstellen...", divider="blue", anchor=False)
  st.write("Hier kannst du eine Grammatikübung erstellen, die du dann als Word herunterladen kannst.")

  st.selectbox("Fach auswählen:", ["🇩🇪 Deutsch", "🇬🇧 English", "🇫🇷 Französisch", "🇪🇸 Spanisch", "🇮🇹 Italienisch", "🇻🇦 Latein"], index=1)

  grammar_topic = st.text_input("Schwerpunkt eintippen:", placeholder="z.B. Present Simple", value="Present Simple")
  st.session_state.grammar_topic = grammar_topic

  exercises_type = st.selectbox("Übungstyp auswählen:", ["Gemischte Übungen", "Lückentext"], index=0)
  st.session_state.exercises_type = exercises_type

  with st.expander("Erweiterte Einstellungen"):
    st.session_state.ai_model = st.selectbox("KI-Modell", ["Genius AI", "Genius AI Pro"])
    st.session_state.number_exercises = st.selectbox("Anzahl der Aufgaben", [5, 10, 15, 20, 25, 30], index=2)

  if st.button("Übung generieren :material/laps:"):
      with st.spinner(''):
          selected_ai_model = st.session_state.ai_model
          if selected_ai_model == "Genius AI":
              selected_ai_model = "gemini-1.5-flash"
          else:
              selected_ai_model = "gemini-1.5-pro"

          with ThreadPoolExecutor() as executor:
              number_one_part = st.session_state.number_exercises / 5
              if st.session_state.exercises_type == "Gemischte Übungen":
                  exercises_type = f"first {number_one_part} Exercises should be fill in the blank and listing the verb in brackets, second {number_one_part} exercises should be correct answers, next {number_one_part} exercises should be  forming statements, next {number_one_part} exercises should be asking questions and last {number_one_part} exercises should be writing negations."
              else:
                  exercises_type = f"Exercises should be fill in the blank and listing the verb in brackets."

              future1 = executor.submit(generate_3_grammar_gemini, selected_ai_model, st.session_state.grammar_topic, st.session_state.number_exercises, exercises_type)
              future2 = executor.submit(generate_3_grammar_gemini, selected_ai_model, st.session_state.grammar_topic, st.session_state.number_exercises, exercises_type)
              st.session_state.response1 = future1.result()
              st.session_state.response2 = future2.result()

          st.session_state.grammar_exercise_level = "2_show"
          st.rerun()

if st.session_state.grammar_exercise_level == "2_show":
    st.header("Übung auswählen...", divider="violet", anchor=False)
    st.write("Hier siehst du zwei Vorschläge für deine Grammatikübung. Wähle den, der dir besser gefällt.")
    
    if st.session_state.response1 != "error" and st.session_state.response2 != "error":
        
        left, right = st.columns(2, gap="medium")

        with left:
            if st.button("Wähle A :material/arrow_right_alt:", use_container_width=True, key="choice_A_top"):
                st.session_state.grammar_exercise_level = "3_download"
                st.session_state.choice = "A"
                st.rerun()
            with st.container(border=True):
                st.subheader("Vorschlag A", divider=True, anchor=False)
                for i, pair in enumerate(st.session_state.response1, 1):
                    st.write(f"**{i}. {pair['exercise']}**")
                    st.write(f"{pair['solution']}")

                if st.button("Wähle A :material/arrow_right_alt:", use_container_width=True, key="choice_A_bottom"):
                    st.session_state.grammar_exercise_level = "3_download"
                    st.session_state.choice = "A"
                    st.rerun()

        with right:
            if st.button("Wähle B :material/arrow_right_alt:", use_container_width=True, key="choice_B_top"):
                st.session_state.grammar_exercise_level = "3_download"
                st.session_state.choice = "B"
                st.rerun()
            with st.container(border=True):
                st.subheader("Vorschlag B", divider=True, anchor=False)
                for i, pair in enumerate(st.session_state.response2, 1):
                    st.write(f"**{i}. {pair['exercise']}**")
                    st.write(f"{pair['solution']}")

                if st.button("Wähle B :material/arrow_right_alt:", use_container_width=True, key="choice_B_bottom"):
                    st.session_state.grammar_exercise_level = "3_download"
                    st.session_state.choice = "B"
                    st.rerun()

    else:
        st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut - eventuell mit einem anderen Schwerpunkt...")
        st.button("Ok")

if st.session_state.grammar_exercise_level == "3_download":
    st.write('Hier kannst du noch einmal das Dokumente einsehen und wenn du zufrieden bist einfach herunterladen. Wenn du noch ein Arbeitsblatt generieren möchtest, klicke einfach auf "Neu starten".')
    
    with st.expander("Generierte Übung"):

        if st.session_state.choice == "A":
            
            for i, pair in enumerate(st.session_state.response1, 1):
                st.write(f"**{i}. {pair['exercise']}**")
                st.write(f"{pair['solution']}")
            
            exercises, solutions = format_questions_and_answers(st.session_state.grammar_topic, st.session_state.response1)

        else:

            for i, pair in enumerate(st.session_state.response2, 1):
                st.write(f"**{i}. {pair['exercise']}**")
                st.write(f"{pair['solution']}")

            exercises, solutions = format_questions_and_answers(st.session_state.grammar_topic, st.session_state.response2)
           
        st.session_state.exercises = exercises
        st.session_state.solutions = solutions

    exercises_filename = f"{st.session_state.grammar_topic}_Übungen.docx"
    exercises_bio = create_document_for_genius_ai(st.session_state.exercises)

    solutions_filename = f"{st.session_state.grammar_topic}_Lösungen.docx"
    solutions_bio = create_document_for_genius_ai(st.session_state.solutions)

    combined_filename = f"{st.session_state.grammar_topic}_Übungen_Lösungen.docx"
    combined_bio = create_combined_grammar_document(
        st.session_state.exercises,
        st.session_state.solutions
    )

    with st.expander("Einzelne Dokumente"):
        st.write("Hier kannst du die Dokumente einzeln herunterladen:")
        one, two = st.columns(2)

        one.download_button(
            use_container_width=True,
            label="Übungen :material/download:",
            data=exercises_bio.getvalue(),
            file_name=exercises_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        two.download_button(
            use_container_width=True,
            label="Lösungen :material/download:",
            data=solutions_bio.getvalue(),
            file_name=solutions_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    left, right = st.columns(2, gap="medium")

    left.download_button("Gesamtes Dokument herunterladen :material/download:", data=combined_bio.getvalue(), file_name=combined_filename, use_container_width=True)

    if right.button("Neu starten :material/restart_alt:", use_container_width=True):
        reset_apps()
        st.rerun()

