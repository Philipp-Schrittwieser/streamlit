import streamlit as st
from apps.teacher.llms.gemini.generate_4_games_gemini import generate_4_games_gemini

if "ai_model" not in st.session_state:
  st.session_state.ai_model = "Genius AI"

if "game_ideas" not in st.session_state:
  st.session_state.game_ideas = ""

if "learning_game_level" not in st.session_state:
  st.session_state.learning_game_level = "1_create"

st.title("Lernspiel - Konzepte 🧩")

st.subheader("SuS zum Mitmachen animieren?", divider="blue", anchor=False)

st.write("Die KI hat da so einige Ideen, um Lernen abwechslungsreicher zu gestalten...")

if st.session_state.learning_game_level == "1_create":

  st.session_state.game_topic = st.text_input("Was du deinen SuS beibringen willst:", placeholder="z.B. Vokabeln lernen", value="Vokabeln lernen")

  st.session_state.game_type = st.selectbox("Worauf du den Fokus legen willst:", ["Egal", "Team", "Einzeln", "Quiz", "Bewegung", "Schreiben", "Sprechen", "Zuhören", "Rollenspiele", "Simulation", "Allgemein"], index=0)

  left, right = st.columns([1, 1], gap="small")
  if left.button("Überraschen lassen :material/laps:", use_container_width=True):
    with st.spinner(''):
      selected_ai_model = st.session_state.ai_model
      if selected_ai_model == "Genius AI":
        ideas =generate_4_games_gemini("gemini-1.5-flash", st.session_state.game_topic)
        st.session_state.game_ideas = ideas
        st.session_state.learning_game_level = "2_show"
        st.rerun()

      else: 
        ideas =generate_4_games_gemini("gemini-1.5-pro", st.session_state.game_topic)  
        st.session_state.game_ideas = ideas
        st.session_state.learning_game_level = "2_show"
        st.rerun()

if st.session_state.learning_game_level == "2_show":
  if st.session_state.game_ideas != "error":
    left, right = st.columns([1, 1], gap="medium")
    left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again1")
    right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart1")
    with st.container(border=True):
      for idea in st.session_state.game_ideas:
        st.markdown(f"### {idea['name']}")
        st.markdown(idea['description'])
      left, right = st.columns([1, 1], gap="medium")
      left.button("Nochmal generieren :material/laps:", use_container_width=True, key="generate_again2")
      right.button("Neu starten :material/restart_alt:", use_container_width=True, key="restart2")
  else:
    st.error("Fehler beim Generieren der Lernspiele :exclamation:")
