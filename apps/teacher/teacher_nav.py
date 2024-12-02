import streamlit as st
import random

def teacher_nav():
    # Initialize Session State
    if 'show_selection_page' not in st.session_state:
        st.session_state.show_selection_page = True

    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = None
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = None

    # Function to show the selection page
    def show_selection_page():
        st.title("Was möchtest du erstellen? 🧠", anchor=False)
        st.write("Hilf mir bitte beim Erstellen von einem...")
        st.write("")
        one, two = st.columns([6, 4])

        if one.button("**Kahoot Quiz** 💡 - Excel", use_container_width=True, key="kahoot_text"):
            st.session_state.show_selection_page = False
            st.session_state.selected_page = "apps/teacher/pages/kahoot/kahoot.py"
            st.rerun()

        # elif one.button("**Kahoot Quiz von YouTube** 🎥 - Excel", use_container_width=True, key="kahoot_youtube"):
        #     st.session_state.show_selection_page = False
        #     st.session_state.selected_page = "apps/teacher/pages/kahoot/kahoot.py"
        #     st.rerun()

        elif one.button("**Arbeitsblatt** 📝 - Word", use_container_width=True, key="exercise_sheet_text"):
            st.session_state.show_selection_page = False
            st.session_state.selected_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"
            st.rerun()

        # elif one.button("**Arbeitsblatt generiert** 📝 - Word", use_container_width=True, key="exercise_sheet_generated"):
        #     st.session_state.show_selection_page = False
        #     st.session_state.selected_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"
        #     st.rerun()

        elif one.button("**Grammatik Übung** 🔎 - Word", use_container_width=True, key="grammar_exercise", ):
            st.session_state.show_selection_page = False
            st.session_state.selected_page = "apps/teacher/pages/grammar_exercise/grammar_exercise.py"
            st.rerun()

        elif one.button("**Lernspiele** 🧩 - Konzepte", use_container_width=True, key="learning_game"):
            st.session_state.show_selection_page = False
            st.session_state.selected_page = "apps/teacher/pages/learning_games/learning_games.py"
            st.rerun()


    if st.session_state.show_selection_page:
        show_selection_page()

    else:
        # Visible Pages
        visible_pages = {
            "Dokumente erstellen...": [
                st.Page("apps/teacher/pages/kahoot/kahoot.py",
                        title="Kahoot Quiz",
                        icon="💡"),
                st.Page("apps/teacher/pages/exercise_sheet/exercise_sheet.py",
                        title="Arbeitsblatt",
                        icon="📝"),
                st.Page("apps/teacher/pages/grammar_exercise/grammar_exercise.py",
                        title="Grammatik Übung",
                        icon="🔎")
            ],
            "Ideen sammeln...": [
                st.Page("apps/teacher/pages/learning_games/learning_games.py",
                        title="Lernspiele",
                        icon="🧩")
            ],
            "Sonstiges...": [
                st.Page("apps/teacher/pages/about_us/about_us.py",
                        title="Über uns",
                        icon="👥"),
                st.Page("apps/teacher/pages/logout/logout.py",
                        title="Log out 👋")
            ]
        }

        teacher_quotes = [
            "Lehrer zu sein ist einfach. Es ist wie Reiten auf einem Fahrrad. Außer das Fahrrad ist in Flammen, der Raum ist in Flammen, und du bist in Flammen.",
            "Lehrer haben Superkräfte: Sie können gleichzeitig reden, hören, schreiben, ein Auge auf 30 Kinder werfen und ihre Kaffeetasse finden – alles ohne ihren Stuhl zu verlassen!",
            "Lehrer: die einzigen Menschen, die dir sagen können, wo du hinmusst, wie du dorthin kommst und wie du dich unterwegs benimmst.",
            "Lehrer zu sein bedeutet, ein lebenslanger Influencer zu sein – nur dass das Studio ein Klassenzimmer ist und die Likes aus echten Herzen kommen.",
            "Gute Lehrer sind die, die ihre Schüler etwas lehren. Großartige Lehrer sind die, die ihre Schüler inspirieren, selbst Lehrer zu werden.",
            "Lehrer: Die einzigen Leute, die dir Hausaufgaben geben und erwarten, dass du dich darüber freust.",
            "Ein Lehrer nimmt die Hand, öffnet den Verstand und berührt das Herz.",
            "Das Klassenzimmer ist der einzige Ort, wo 'es gibt keine dummen Fragen' sowohl eine Herausforderung als auch ein Versprechen ist.",
            "Lehrer haben die Fähigkeit, Sterne zu sehen und Schülern zu helfen, ihre zu erreichen."
        ]

        random_quote = random.choice(teacher_quotes)
        st.sidebar.text(f'"{random_quote}"')

        # Navigation with visible pages
        pg = st.navigation(visible_pages, position="sidebar")
        pg.run()

        # Switch to the selected page on first run
        if st.session_state.first_run:
            st.session_state.first_run = False
            target_page = st.session_state.get('selected_page', st.session_state.selected_page)
            print("ROUTING TO:", target_page)
            st.session_state.current_page = target_page
            st.switch_page(target_page)