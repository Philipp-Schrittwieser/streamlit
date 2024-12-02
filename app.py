import streamlit as st
from helpers import visual_configs
from assets.htmls import h1
from apps.teacher.teacher_nav import teacher_nav
from apps.test_app.main import other_app
import time
from init import init_routine

import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

# 0 Secrets
pw_kahoot = st.secrets.PW_KAHOOT
pw_other = st.secrets.PW_OTHER

init_routine()

def check_password():
    password = st.session_state.password_input  # Hole Wert über key
    st.session_state.password = password
    st.session_state.login_state = "login-finished"


# 2. Login-Maske
if st.session_state.login_state in ["logging-in", "wrong-pw"]:
    st.title("Zugangscode", anchor=False)
        
    password = st.text_input(
        "Bitte gib deinen Zugangscode hier ein:", 
        type="password", 
        on_change=check_password,
        key="password_input"
    )

    st.write("*Die App ist für die Nutzung am PC optimiert. 💻 📴")    

    # Logge automatisch ein | Log In deaktiviert
    st.session_state.password = pw_kahoot
    st.session_state.login_state = "login-finished"
    st.rerun()

# 3. Fehlerbehandlung für falsches Passwort
if st.session_state.login_state == "wrong-pw":
    st.error("Falscher Zugang... Probiere es erneut!")
    time.sleep(3)
    st.session_state.login_state = "logging-in"
    st.rerun()


# 4. Zur App
if st.session_state.login_state == "login-finished":
    password = st.session_state.password
    if password == pw_kahoot:
        teacher_nav()

    elif password == pw_other:
        st.session_state.logged_in_app = "other"
        other_app()

    else:
        st.session_state.login_state = "wrong-pw"
        st.session_state.password_input = ""
        st.rerun()