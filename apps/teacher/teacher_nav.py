import streamlit as st

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
        visible_pages = [
            st.Page("apps/teacher/pages/kahoot/kahoot.py",
                    title="Kahoot Quiz", 
                    icon="💡"), 
            st.Page("apps/teacher/pages/exercise_sheet/exercise_sheet.py", 
                    title="Arbeitsblatt", 
                    icon="📝"),
            st.Page("apps/teacher/pages/logout/logout.py", 
                    title="Log out 👋")
        ]

        # Navigation nur mit sichtbaren Seiten
        pg = st.navigation({"Erstelle ein...": visible_pages}, position="sidebar")
        pg.run()

        # Switch zur ausgewählten Seite
        if st.session_state.first_run:
            st.session_state.first_run = False
            st.switch_page(st.session_state.current_page)
