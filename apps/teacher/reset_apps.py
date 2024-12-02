import streamlit as st

def reset_apps():


  # Clear query params, falls neustart nach shared Dok
  # Bei Sharing Doc
  st.query_params.clear()

  # 1. Kahoot
  st.session_state.questions_generated = False
  # st.session_state.questions_generated = True


  # 2. Exercise Sheet
  st.session_state.exercise_sheet_level = "1_text"
  st.session_state.topic = ""
  st.session_state.response = ""
  st.session_state.qas = []
  st.session_state.fragen = ""
  st.session_state.lösungen = ""
  st.session_state.ai_model = "Genius AI"

  # 3. Grammar
  st.session_state.response1 = []
  st.session_state.response2 = []
  st.session_state.grammar_topic = ""
  st.session_state.ai_model = ""
  st.session_state.number_exercises = 10
  st.session_state.grammar_exercise_level = "1_create"
  st.session_state.choice = None

  # 4. Learning Games
  st.session_state.ai_model = ""
  st.session_state.game_ideas = ""
  st.session_state.learning_game_level = "1_create"