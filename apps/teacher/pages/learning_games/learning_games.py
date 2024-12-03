import streamlit as st
from apps.teacher.reset_apps import reset_apps
from apps.teacher.llms.gemini.generate_4_games_gemini import generate_4_games_gemini
from apps.teacher.animations import show_generate, show_generate_finished, show_restart_app
from apps.teacher.llms.gemini.generate_1_text_gemini import generate_1_text_gemini
import random

## Setzt bei Page-Wechsel alles zurück
# Wenn er davor nicht auf der Seite war, App zurücksetzen
if st.session_state.current_page != "apps/teacher/pages/learning_games/learning_games.py":    
  reset_apps()
  # Außerdem Seite, auf derzeitige Seite setzen
  st.session_state.current_page = "apps/teacher/pages/learning_games/learning_games.py"


if "ai_model" not in st.session_state:
  st.session_state.ai_model = "Genius AI"

if "game_ideas" not in st.session_state:
  st.session_state.game_ideas = ""

if "learning_game_level" not in st.session_state:
  st.session_state.learning_game_level = "1_create"

if "random_index" not in st.session_state:
  st.session_state.random_index = None


def generate_game_ideas(ai_model, topic, game_type):
  """Generiert Spielideen basierend auf dem gewählten KI-Modell."""

  if ai_model == "Genius AI":
    response = generate_4_games_gemini("gemini-1.5-flash", topic, game_type)

    if response == "error":
      print("Trying again with SAME MODEL")
      response = generate_4_games_gemini("gemini-1.5-flash", topic, game_type)

    return response
  
  elif ai_model == "Genius AI Pro":
    response = generate_4_games_gemini("gemini-1.5-pro", topic, game_type)

    if response == "error": 
      print("Trying again with flash model")
      response = generate_4_games_gemini("gemini-1.5-flash", topic, game_type)
    return response
  
  else:
    st.error("Kein gültiges KI-Modell ausgewählt :exclamation:")
    return "error"
  


st.title("Lernspiel - Konzepte 🧩")

st.subheader("SuS zum Mitmachen animieren?", divider="blue", anchor=False)

st.write("Die KI hat da ein paar Ideen, um Lernen abwechslungsreicher zu gestalten...")

if st.session_state.learning_game_level == "1_create":

  st.session_state.game_topic = st.text_input("Was du deinen SuS beibringen möchtest:", placeholder="z.B. Vokabeln lernen")

  all_game_types = ["Allgemein", "Team-Spiele", "Einzelarbeit", "Quiz", "Bewegung", "Schreiben", "Sprechen", "Zuhören", "Rollenspiele", "Simulation"]
  if st.session_state.random_index is None:
    st.session_state.random_index = random.randint(0, len(all_game_types) - 1)
  st.session_state.game_type = st.selectbox("Worauf du den Fokus legen willst:", all_game_types, index=st.session_state.random_index)

  with st.expander("Erweiterte Einstellungen"):
    #dropdown für KI-Modelle
    st.session_state.ai_model = st.selectbox("KI-Modell", ["Genius AI", "Genius AI Pro"])


  left, right = st.columns([1, 1], gap="small")

  if left.button("Ideen generieren :material/laps:", use_container_width=True):
    show_generate("Ideen")
    with st.spinner(''):
      response = generate_game_ideas(st.session_state.ai_model, st.session_state.game_topic, st.session_state.game_type)
        
      if response != "error":
        st.session_state.game_ideas = response
        st.session_state.learning_game_level = "2_show"
        show_generate_finished()

      else:
        st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut - eventuell mit einem anderen Lernziel...")
        st.button("Ok")


if st.session_state.learning_game_level == "2_show":
  
  if st.session_state.game_ideas != "error":
    left, right = st.columns([1, 1], gap="medium")
    
    if left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again1"):
      
      show_generate("Ideen")

      with st.spinner(''):
        response = generate_game_ideas(st.session_state.ai_model, st.session_state.game_topic, st.session_state.game_type)
        
        if response != "error":
          st.session_state.game_ideas = response
        else:
          st.error("Fehler beim Generieren. :exclamation: Bitte versuche es erneut - eventuell mit einem anderen Lernziel...")
          st.button("Ok")

        show_generate_finished()
        
    if right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart1"):
      reset_apps()
      show_restart_app()
    
    with st.container(border=True):
      for idea in st.session_state.game_ideas:
        st.markdown(f"### {idea['name']}")
        st.markdown(idea['description'])
      left, right = st.columns([1, 1], gap="medium")
      # left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again2")
      # right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart2")
  else:
    st.error("Fehler beim Generieren der Lernspiele :exclamation:")
