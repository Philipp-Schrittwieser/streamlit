import streamlit.components.v1 as components

def import_gtm():
    # Google Analytics tracking code
    ga_tracking_code = "GTM-W7P62GV8"
    
    # Embed Google Analytics tracking code
    ga_code = f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_tracking_code}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{ga_tracking_code}');
    </script>
    """
    components.html(ga_code, height=0)
