'''
from bs4 import BeautifulSoup
import re
import json
import traceback
from playwright.sync_api import sync_playwright
import random
import streamlit as st

# Proxy-Konfiguration
proxies = [
    {'http': 'http://14ad64224ed74:821cfdcc1b@91.149.228.224:12323'},
    {'http': 'http://14ad64224ed74:821cfdcc1b@78.143.227.44:12323'}
]

def extract_youtube_id(url):
    regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.*|(?:v|e(?:mbed)?|watch|embed)/|.*[?&]v=)|youtu\.be/)([^&?]{11})'
    match = re.search(regex, url)
    
    if match:
        return match.group(1)
    else:
        return None

def return_transcript_new(url):
    try:
        if 'youtube.com' in url or 'youtu.be' in url:
            video_id = extract_youtube_id(url)
        else:
            print("Ungültige YouTube URL oder Video ID")
            st.error("Ungültige YouTube URL oder Video ID")
            return

        url = f'https://www.youtube.com/watch?v={video_id}'

        # Cookies laden
        try:
            with open('cookies.json', 'r') as f:
                stored_cookies = json.load(f)
        except FileNotFoundError:
            stored_cookies = None

        # Zufälligen Proxy auswählen
        proxy = random.choice(proxies)
        proxy_server = proxy['http'].split('@')[1]
        proxy_auth = proxy['http'].split('@')[0].replace('http://', '').split(':')

        with sync_playwright() as p:
            # Browser mit zufälligem Proxy starten
            browser = p.chromium.launch(headless=True, proxy={
                'server': proxy_server,
                'username': proxy_auth[0],
                'password': proxy_auth[1]
            })
            context = browser.new_context()

            # Gespeicherte Cookies setzen falls vorhanden
            if stored_cookies:
                context.add_cookies(stored_cookies)

            page = context.new_page()

            # Navigiere zur YouTube-Seite
            page.goto(url)

            # Längere Wartezeit für das Laden der Daten
            page.wait_for_timeout(3000)  # 5 Sekunden warten

            # Cookies speichern
            cookies = context.cookies()
            with open('cookies.json', 'w') as f:
                json.dump(cookies, f)

            # Extrahiere die JSON-Daten aus den Skripten
            page.wait_for_selector('script', state='attached')  # Warte nur auf Existenz
            scripts = page.evaluate('''
                Array.from(document.getElementsByTagName('script'))
                    .map(script => script.textContent)
                    .join('');
            ''')
            
            json_data = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', scripts)
                
            if json_data:
                try:
                    data = json.loads(json_data.group(1))
                    caption_tracks = data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
                    
                    if caption_tracks:
                        subtitle_url = caption_tracks[0]['baseUrl']
                        subtitle_response = page.request.get(subtitle_url)

                        if subtitle_response.status == 200:
                            # Untertitel parsen mit BeautifulSoup
                            soup = BeautifulSoup(subtitle_response.text(), 'xml')
                            texts = [elem.text for elem in soup.find_all('text')]
                            full_text = ' '.join(texts)
                            print(full_text[:100])
                            st.success(full_text[:100])
                            return full_text
                        else:
                            print(f"Untertitel-Download fehlgeschlagen:\n{subtitle_response.body}\nStatus: {subtitle_response.status}")
                            st.error(f"Untertitel-Download fehlgeschlagen:\n{subtitle_response.body}\nStatus: {subtitle_response.status}")
                    else:
                        print(f"Keine Untertitel gefunden für Video ID: {video_id}")
                        st.error(f"Keine Untertitel gefunden für Video ID: {video_id}")
                except Exception as e:
                    print(f"JSON Parsing Fehler:\n{str(e)}\n{traceback.format_exc()}")
                    st.error(f"JSON Parsing Fehler:\n{str(e)}\n{traceback.format_exc()}")
            else:
                print("Keine JSON-Daten gefunden im YouTube-Response")
                st.error("Keine JSON-Daten gefunden im YouTube-Response")

            context.close()
            browser.close()
            
    except Exception as e:
        print(f"Unerwarteter Fehler:\n{str(e)}\n{traceback.format_exc()}")
        st.error(f"Unerwarteter Fehler:\n{str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    urls = [
        "http://www.youtube.com/watch?v=0zM3nApSvMg",
        "https://youtu.be/0zM3nApSvMg", 
        "http://www.youtube.com/embed/0zM3nApSvMg",
        "http://www.youtube.com/v/0zM3nApSvMg?version=3&autohide=1",
        "http://youtube.com/watch?v=0zM3nApSvMg&feature=youtu.be",
        "http://youtube.com/?v=0zM3nApSvMg",
        "http://www.youtube.com/user/Google#p/a/u/2/QP5szEn2dxs"
    ]
    
    # for url in urls:
    #     print(f"\nTeste URL: {url}")
    #     return_transcript_new(url)

    return_transcript_new("https://www.youtube.com/watch?v=SMDrjiZVW-4")

'''