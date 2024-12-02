import streamlit as st
import time

def show_generate(string):
  st.success(f"Generiere {string}... ⛏️")
  st.toast(f"KI generiert {string}... 💡")
  time.sleep(1)
  st.toast("Bitte warte einen kurzen Moment ⏰ ")

def show_generate_finished():
  # st.success("Fertig generiert 🎉🎉🎉")
  st.balloons()
  time.sleep(0.75)
  st.rerun()

def show_donwload_completed(string):
  st.toast(f"{string} wurden heruntergeladen ✅ ")
  time.sleep(1)
  st.toast("Du kannst sie dir rechts oben im Browser ansehen! 🌎")

def show_restart_app():
  st.toast("App wird neu gestartet... 🏁")
  time.sleep(0.5)
  st.rerun()