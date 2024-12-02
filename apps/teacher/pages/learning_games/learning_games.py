import streamlit as st
from apps.teacher.reset_apps import reset_apps
from apps.teacher.llms.gemini.generate_4_games_gemini import generate_4_games_gemini


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


def generate_game_ideas(ai_model, topic, game_type):
  """Generiert Spielideen basierend auf dem gewählten KI-Modell."""
  ai_model = "Genius AI"
  if ai_model == "Genius AI":
    return generate_4_games_gemini("gemini-1.5-flash", topic, game_type)
  else:
    return generate_4_games_gemini("gemini-1.5-pro", topic, game_type)
  
  


st.title("Lernspiel - Konzepte 🧩")

st.subheader("SuS zum Mitmachen animieren?", divider="blue", anchor=False)

st.write("Die KI hat da ein paar Ideen, um Lernen abwechslungsreicher zu gestalten...")

if st.session_state.learning_game_level == "1_create":

  st.session_state.game_topic = st.text_input("Was du deinen SuS beibringen möchtest:", placeholder="z.B. Vokabeln lernen", value="Vokabeln lernen")

  st.session_state.game_type = st.selectbox("Worauf du den Fokus legen willst:", ["Allgemein", "Team-Spiele", "Einzelnarbeit", "Quiz", "Bewegung", "Schreiben", "Sprechen", "Zuhören", "Rollenspiele", "Simulation"], index=0)

  left, right = st.columns([1, 1], gap="small")
  if left.button("Ideen generieren :material/laps:", use_container_width=True):
    with st.spinner(''):
      st.session_state.game_ideas = generate_game_ideas(st.session_state.ai_model, st.session_state.game_topic, st.session_state.game_type)
      st.session_state.learning_game_level = "2_show"
      st.rerun()

if st.session_state.learning_game_level == "2_show":
  if st.session_state.game_ideas != "error":
    left, right = st.columns([1, 1], gap="medium")
    if left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again1"):
      with st.spinner(''):
        st.session_state.game_ideas = generate_game_ideas(st.session_state.ai_model, st.session_state.game_topic, st.session_state.game_type)
        
    if right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart1"):
      reset_apps()
      st.rerun()
    with st.container(border=True):
      for idea in st.session_state.game_ideas:
        st.markdown(f"### {idea['name']}")
        st.markdown(idea['description'])
      left, right = st.columns([1, 1], gap="medium")
      # left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again2")
      # right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart2")
  else:
    st.error("Fehler beim Generieren der Lernspiele :exclamation:")
