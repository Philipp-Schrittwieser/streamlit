from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import random
import requests

# Liste der Proxyserver
proxies = [
    {'http': 'http://14ad64224ed74:821cfdcc1b@91.149.228.224:12323'},
    {'http': 'http://14ad64224ed74:821cfdcc1b@78.143.227.44:12323'}
]


def get_video_id_with_proxy(url):
    try:
        proxy = random.choice(proxies)
        response = requests.get(url, proxies=proxy, timeout=10)
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
    """Holt die Untertitel für ein gegebenes YouTube-Video mit Proxy."""
    video_id = get_video_id_with_proxy(video_url)
    if not video_id:
        print("Ungültige YouTube-URL")
        return None

    # Wähle zufälligen Proxy
    proxy = random.choice(proxies)
    
    try:
        # Hole Transkript mit Proxy
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["de","en"], proxies=proxy)
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