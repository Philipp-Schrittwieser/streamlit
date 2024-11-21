import streamlit as st

def h1(text, special_class="c-h1"):
  return st.html(f'<p class="{special_class}">{text}</p>')

def button_blue(text, special_class="c-button-blue"):
  return st.html(f'<button class="{special_class}">{text}</button>')