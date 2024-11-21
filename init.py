import streamlit as st

def initialize_variables():
    # Initialisiere Zustandsvariablen, falls sie noch nicht existieren
    if 'login_state' not in st.session_state:
      st.session_state.login_state = "logging-in"

    if 'logged_in_app' not in st.session_state:
        st.session_state.logged_in_app = None

    if 'password' not in st.session_state:
      st.session_state.password = ""
      