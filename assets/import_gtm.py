import streamlit.components.v1 as components

def import_gtm():
  # Google Tag Manager einbinden
  with open("gtm.html", "r") as f:
      html_code = f.read()
  components.html(html_code, height=0)
