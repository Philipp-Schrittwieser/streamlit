import streamlit as st

def reset_apps():
  # Kahoot
  st.session_state.questions_generated = False

  # Exercise Sheet
  st.session_state.exercise_sheet_level = "1_text"
  st.session_state.topic = ""
  st.session_state.response = ""
  st.session_state.qas = []
  st.session_state.fragen = ""
  st.session_state.lösungen = ""
