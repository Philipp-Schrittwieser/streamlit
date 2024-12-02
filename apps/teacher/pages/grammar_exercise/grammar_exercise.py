import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from apps.teacher.create_documents.create_word import create_document_for_genius_ai, create_combined_grammar_document, format_questions_and_answers
from apps.teacher.reset_apps import reset_apps
from apps.teacher.llms.gemini.generate_3_grammar_gemini import generate_3_grammar_gemini
from apps.teacher.animations import show_generate, show_generate_finished, show_restart_app, show_donwload_completed
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

def generate_grammar_exercises(ai_model, topic, number_exercises, exercise_type, language):
    """
    Bereitet den Prompt vor und generiert Grammatikübungen
    """
    # Set AI model
    selected_model = "gemini-1.5-flash" if ai_model == "Genius AI" else "gemini-1.5-pro"
    
    # Calculate exercises per section
    exercises_per_section = number_exercises / 5
    
    # Define exercise prompts
    exercise_prompts = {
        "Gemischte Übungen": f"first {exercises_per_section} Exercise is to fill in the blank and listing the verb in brackets, second {exercises_per_section} Exercise is to correct answers, next {exercises_per_section} Exercise is to form statements, next {exercises_per_section} Exercises is to write negations and last Exercise is {exercises_per_section} exercises is to ask questions for the school subject {language} and write in {language} !!!",
        "Lückentext": f"Exercise is ONLY to fill in the blank and listing the verb in brackets for the school subject {language} and write in {language} !!!",
        "Fehler ausbessern": f"Exercise is ONLY to correct answers for the school subject {language} and write in {language} !!!",
        "Statement": f"Exercise is ONLY to form statements for the school subject {language} and write in {language} !!!",
        "Verneinung": f"Exercise is ONLY to form negations for the school subject {language} and write in {language} !!!",
        "Frage": f"Exercise is ONLY to form questions for the school subject {language} and write in {language} !!!"
    }
    
    exercise_prompt = exercise_prompts[exercise_type]
    
    # Generate exercises
    return generate_3_grammar_gemini(selected_model, topic, number_exercises, exercise_prompt)


left, right = st.columns([15, 1], gap="small", vertical_alignment="center")

left.title("Grammatik Übung Generator 🔎")

if st.session_state.grammar_exercise_level == "2_show":
  if right.button(":material/arrow_back:", use_container_width=False):
    reset_apps()
    show_restart_app()

if st.session_state.grammar_exercise_level == "1_create":
  st.subheader("Übung erstellen...", divider="blue", anchor=False)
  st.write("Hier kannst du eine Grammatikübung erstellen, die du dann als Word herunterladen kannst.")

  st.session_state.grammar_language = st.selectbox("Fach auswählen:", ["🇩🇪 Deutsch", "🇬🇧 English", "🇫🇷 Französisch", "🇪🇸 Spanisch", "🇮🇹 Italienisch", "🇻🇦 Latein"], index=1)

  grammar_topic = st.text_input("Schwerpunkt eintippen:", placeholder="z.B. Present Simple")
  st.session_state.grammar_topic = grammar_topic

  st.session_state.exercises_type = st.selectbox("Übungstyp auswählen:", ["Gemischte Übungen", "Lückentext", "Fehler ausbessern", "Statement", "Verneinung", "Frage"], index=0)

  with st.expander("Erweiterte Einstellungen"):
    st.session_state.number_exercises = st.selectbox("Anzahl der Aufgaben", [5, 10, 15, 20, 25, 30], index=1)
    st.session_state.ai_model = st.selectbox("KI-Modell", ["Genius AI", "Genius AI Pro"])


  if st.button("Übung generieren :material/laps:"):
      with st.spinner(''):
        show_generate("Grammatikübung")
        st.session_state.response1 = generate_grammar_exercises(st.session_state.ai_model, st.session_state.grammar_topic, st.session_state.number_exercises, st.session_state.exercises_type, st.session_state.grammar_language)
        st.session_state.grammar_exercise_level = "2_show"
        show_generate_finished()

if st.session_state.grammar_exercise_level == "2_show":
    st.header("Übung prüfen...", divider="violet", anchor=False)
    st.write("Hier siehst du einen Vorschlag für deine Grammatikübung. Wenn du zufrieden bist, klicke auf 'Auswählen' ansonsten auf 'Neu generieren'.")
    st.write("######")

    if st.session_state.response1 != "error" and st.session_state.response2 != "error":
        
        left, right = st.columns([1, 1], gap="medium")

        with left:
            if st.button("Auswählen :material/arrow_right_alt:", use_container_width=True, key="choice_A_top"):
                st.session_state.grammar_exercise_level = "3_download"
                st.session_state.choice = "A"
                st.rerun()

        with right:
            if st.button("Neu generieren :material/laps:", use_container_width=True, key="choice_B_top"):
                with st.spinner(''):
                    st.session_state.response1 = generate_grammar_exercises(st.session_state.ai_model, st.session_state.grammar_topic, st.session_state.number_exercises, st.session_state.exercises_type, st.session_state.grammar_language)
                    st.session_state.grammar_exercise_level = "2_show"
                    show_generate_finished()

        with st.container(border=True):
            st.subheader("Generierte Übung", divider=True, anchor=False)
            for i, pair in enumerate(st.session_state.response1, 1):
                st.write(f"{i}. {pair['exercise']}")
                # st.write(f"{pair['solution']}")

        # if st.button("Wähle A :material/arrow_right_alt:", use_container_width=True, key="choice_A_bottom"):
        #     st.session_state.grammar_exercise_level = "3_download"
        #     st.session_state.choice = "A"
        #     st.rerun()

        # st.write("######")

        # if st.button("Wähle B :material/arrow_right_alt:", use_container_width=True, key="choice_B_top"):
        #     st.session_state.grammar_exercise_level = "3_download"
        #     st.session_state.choice = "B"
        #     st.rerun()

        # with st.container(border=True):
        #     st.subheader("Vorschlag B", divider=True, anchor=False)
        #     for i, pair in enumerate(st.session_state.response2, 1):
        #         st.write(f"{i}. {pair['exercise']}")
        #         # st.write(f"{pair['solution']}")

        #     if st.button("Wähle B :material/arrow_right_alt:", use_container_width=True, key="choice_B_bottom"):
        #         st.session_state.grammar_exercise_level = "3_download"
        #         st.session_state.choice = "B"
        #         st.rerun()

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
            
            lines = "\n\n\u200B\n\n_________________________________________________________________________________________________________\n\n\u200B\n\n"
            exercises, solutions = format_questions_and_answers(st.session_state.grammar_topic, st.session_state.response1, lines)

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

    if left.download_button("Gesamtes Dokument herunterladen :material/download:", data=combined_bio.getvalue(), file_name=combined_filename, use_container_width=True):
        show_donwload_completed("Dokument")

    if right.button("Neu starten :material/restart_alt:", use_container_width=True):
        reset_apps()
        show_restart_app()

