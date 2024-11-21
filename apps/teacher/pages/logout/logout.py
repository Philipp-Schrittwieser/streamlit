import streamlit as st

# # Debug-Ausgaben
# print("Login State:", st.session_state.login_state)  # Konsolenausgabe
# st.write("Login State:", st.session_state.login_state)  # Browser-Ausgabe

if st.session_state.login_state == "login-finished":
    st.title("Wir loggen dich aus...", anchor=False)
    st.write("Auf Wiedersehen 👋")
    js = '''
        <script>
            setTimeout(function() {
                window.parent.location.reload();
            }, 450);
        </script>
    '''
    st.components.v1.html(js)