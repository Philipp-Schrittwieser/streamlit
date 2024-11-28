
'''

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import random
import requests
import http.cookiejar
import tempfile
import os

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    NoTranscriptAvailable,
    VideoUnavailable
)

# Liste der Proxyserver
proxies = [
    {'http': 'http://14ad64224ed74:821cfdcc1b@91.149.228.224:12323'},
    {'http': 'http://14ad64224ed74:821cfdcc1b@78.143.227.44:12323'}
]

def load_cookies(file_path):
    cookie_jar = http.cookiejar.MozillaCookieJar(file_path)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    return cookie_jar

def load_user_agent(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Laden Sie Cookies und User-Agent
cookies = load_cookies('youtube_config.txt')
user_agent = load_user_agent('user_agent.txt')

def get_video_id_with_proxy(url):
    try:
        proxy = random.choice(proxies)
        headers = {'User-Agent': user_agent}
        response = requests.get(url, proxies=proxy, timeout=10, cookies=cookies, headers=headers)
        response.raise_for_status()
        final_url = response.url
        query = urlparse(final_url).query
        params = parse_qs(query)
        video_id = params.get('v', [None])[0]
        print(f"Video ID: {video_id}")
        return video_id
    except requests.exceptions.ProxyError:
        print("Proxy-Verbindungsfehler")
    except requests.exceptions.Timeout:
        print("Zeitüberschreitung bei der Anfrage")
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage: {str(e)}")
    return None

def get_subtitles(video_url):
    video_id = get_video_id_with_proxy(video_url)
    if not video_id:
        print("Ungültige YouTube-URL")
        return None

    proxy = random.choice(proxies)
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            cookies.save(temp_file.name, ignore_discard=True, ignore_expires=True)
            temp_file_name = temp_file.name

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["de","en"], proxies=proxy, cookies=temp_file_name)
        
        # Löschen Sie die temporäre Datei nach Verwendung
        os.unlink(temp_file_name)
        
        return transcript
    except TranscriptsDisabled:
        print("Untertitel sind für dieses Video deaktiviert.")
    except NoTranscriptFound:
        print("Keine Untertitel in den angegebenen Sprachen gefunden.")
    except Exception as e:
        print(f"Fehler beim Abrufen der Untertitel: {e}")
    return None

def return_transcript(video_url):
    if video_url != "":
        subtitles_array = get_subtitles(video_url)
        if subtitles_array:
            text_transcript = ' '.join([subtitle['text'] for subtitle in subtitles_array])
            print(text_transcript[0:25])
            return text_transcript
    return None

    '''