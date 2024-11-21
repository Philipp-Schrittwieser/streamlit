import streamlit as st
from assets.htmls import h1
  
def other_app():
    h1("Andere App")
    st.write("Willkommen in der anderen App!")
    st.button(label="Test-Button", on_click=print("Clicked"), key="button-blue")
