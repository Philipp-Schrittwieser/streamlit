import time
from assets.style import return_styles

def configs(st):
    # 1 Title und Icon setzen
    st.set_page_config(
    page_title="AI School",
    page_icon="📚"
    # page_icon="images/female2.webp",
    # initial_sidebar_state="collapsed"
    # layout="wide",
    # initial_sidebar_state="expanded",
    )

    # 2 CSS laden
    set_css(st)
    
    # 3 Logo setzen
    logo = "images/books_title.png"  # Pfad zum Bild
    st.logo(image=logo, size="large")  # Bild anzeigen

    # x Initialisieren Sie Tailwind
    # tw.initialize_tailwind()
    # return tw
    
def set_css(st):
    # with open("assets/style.css") as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.markdown(f'<style>{return_styles()}</style>', unsafe_allow_html=True)
 

def loading_bar(progress_bar):
    
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)  # Optional: Verzögerung zum Testen

    time.sleep(1)
    progress_bar.empty()  # Blendet die Loading-Bar aus