from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """Extrahiert die Video-ID aus einer YouTube-URL."""
    query = urlparse(url).query
    params = parse_qs(query)
    return params.get('v', [None])[0]

def get_subtitles(video_url):
    """Holt die Untertitel für ein gegebenes YouTube-Video."""
    video_id = get_video_id(video_url)
    if not video_id:
        print("Ungültige YouTube-URL")
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["de","en"])
        return transcript
    except Exception as e:
        print(f"Fehler beim Abrufen der Untertitel: {e}")
        return None

def return_transcript(video_url):
    # print(video_url)
    if video_url != "": 
        subtitles_array = get_subtitles(video_url)
        if subtitles_array:
            return ' '.join([subtitle['text'] for subtitle in subtitles_array])
    return None