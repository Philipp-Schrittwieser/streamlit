import streamlit as st
import random

def teacher_nav():

    # Seite als Router
    def routing_page():
        st.title("Was möchtest du erstellen? 🧠", anchor=False)
        st.write("Hilf mir bitte beim Erstellen von einem...")
        st.write("")
        one, two = st.columns([6, 4])
        if one.button("**Kahoot Quiz** - Excel 💡", use_container_width=True):
            st.session_state.show_routing_page = False
            st.session_state.current_page = "apps/teacher/pages/kahoot/kahoot.py"
            st.rerun()
        one.write("")
        if one.button("**Arbeitsblatt** - Word 📝", use_container_width=True):
            st.session_state.show_routing_page = False
            st.session_state.current_page = "apps/teacher/pages/exercise_sheet/exercise_sheet.py"
            st.rerun()
            

    # Initialisieren des Session State
    if 'show_routing_page' not in st.session_state:
        st.session_state.show_routing_page = True

    # Initialisieren first_run
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    if st.session_state.show_routing_page:
        routing_page()

    else:  
        # Sichtbare Seiten
        visible_pages = { "Erstelle ein...": [
            st.Page("apps/teacher/pages/kahoot/kahoot.py",
                    title="Kahoot Quiz", 
                    icon="💡"), 
            st.Page("apps/teacher/pages/exercise_sheet/exercise_sheet.py", 
                    title="Arbeitsblatt", 
                    icon="📝")],
            "Sonstiges...": [
            st.Page("apps/teacher/pages/about_us/about_us.py", 
                    title="Über uns", 
                    icon="👥"),
            st.Page("apps/teacher/pages/logout/logout.py", 
                    title="Log out 👋")
        ]}

        teacher_quotes = [
            "Lehrer zu sein ist einfach. Es ist wie Reiten auf einem Fahrrad. Außer das Fahrrad ist in Flammen, der Raum ist in Flammen, und du bist in Flammen.",
            "Lehrer haben Superkräfte: Sie können gleichzeitig reden, hören, schreiben, ein Auge auf 30 Kinder werfen und ihre Kaffeetasse finden – alles ohne ihren Stuhl zu verlassen!",
            "Lehrer: die einzigen Menschen, die dir sagen können, wo du hinmusst, wie du dorthin kommst und wie du dich unterwegs benimmst.",
            "Lehrer zu sein bedeutet, ein lebenslanger Influencer zu sein – nur dass das Studio ein Klassenzimmer ist und die Likes aus echten Herzen kommen.",
            "Gute Lehrer sind die, die ihre Schüler etwas lehren. Großartige Lehrer sind die, die ihre Schüler inspirieren, selbst Lehrer zu werden.",
            "Lehrer: Die einzigen Leute, die dir Hausaufgaben geben und erwarten, dass du dich darüber freust.",
            "Ein Lehrer nimmt die Hand, öffnet den Verstand und berührt das Herz.",
            "Das Klassenzimmer ist der einzige Ort, wo ‘es gibt keine dummen Fragen’ sowohl eine Herausforderung als auch ein Versprechen ist.",
            "Lehrer haben die Fähigkeit, Sterne zu sehen und Schülern zu helfen, ihre zu erreichen."
        ]

        random_quote = random.choice(teacher_quotes)

        st.sidebar.text(f'"{random_quote}"')

        # Navigation nur mit sichtbaren Seiten
        pg = st.navigation(visible_pages, position="sidebar")
        pg.run()

        # Switch zur ausgewählten Seite
        if st.session_state.first_run:
            st.session_state.first_run = False
            st.switch_page(st.session_state.current_page)
