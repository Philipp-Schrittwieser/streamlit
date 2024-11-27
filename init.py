import streamlit as st
from db.db import connect_db
from helpers import visual_configs
from db.db import return_kahoot

is_deployed = st.secrets["IS_DEPLOYED"]

def initialize_variables():
    
    if "base_url" not in st.session_state:
      if is_deployed == "true":
          base_url = "https://ai-school.onrender.com/"
      else:
          base_url = "http://localhost:8501/"

      st.session_state.base_url = base_url

    # Initialisiere Zustandsvariablen, falls sie noch nicht existieren
    if 'login_state' not in st.session_state:
      st.session_state.login_state = "logging-in"

    if 'logged_in_app' not in st.session_state:
        st.session_state.logged_in_app = None

    if 'password' not in st.session_state:
      st.session_state.password = ""

    # Init DB
    if "db" not in st.session_state:
        st.session_state.db = connect_db()

    if "referal_checked" not in st.session_state:
        st.session_state.referal_checked = False

def check_referal():
  print(f"Query Params: {st.query_params}")

  if "id" in st.query_params:
    from_id = st.query_params["id"]

    with st.spinner("Lade Kahoot..."):
        st.session_state.kahoot = return_kahoot(from_id)
        st.session_state.questions_generated = True
        st.session_state.topic = st.session_state.kahoot["topic"]

    shared_item_from_db = st.session_state.kahoot

    match shared_item_from_db["current_page"]:
        case 'kahoot':
            # st.session_state.selected_page = "apps/teacher/pages/kahoot/kahoot.py"
            st.session_state.current_page = "apps/teacher/pages/kahoot/kahoot.py"

        case 'exercise_sheet':
            # st.session_state.selected_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"
            st.session_state.current_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"
        case _:  # Default Fall
            raise Exception("Invalid page")

    # Direkt zur Seite wechseln
    st.session_state.show_selection_page = False
    st.session_state.first_run = False



def init_routine():

  # 1. Title, Icon, Logo, Google Analytics, Footer
  visual_configs(st)

  # 2. Init Variables
  initialize_variables()

  # 3. Check if reroute referal
  check_referal()



