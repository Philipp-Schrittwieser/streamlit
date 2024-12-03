# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright
import json
import os
from urllib.parse import urlparse, parse_qs


def get_video_id(url):
    """Extrahiert die Video-ID aus einer YouTube-URL."""
    query = urlparse(url).query
    params = parse_qs(query)
    return params.get('v', [None])[0]


def scrape_youtube_transcript(url):
    video_id = get_video_id(url)

    with sync_playwright() as p:
        # Launch the browser with headless mode set to False for visibility
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load cookies from a local file if it exists
        try:
            cookie_path = os.path.join(os.path.dirname(__file__), 'cookies.json')
            with open(cookie_path, 'r') as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
        except FileNotFoundError:
            print("No cookie file found. Continuing without loading cookies.")

        # Create a new page within the browser context
        page = context.new_page()
        
        # Define the target URL
        url = f"https://www.youtube-transcript.io/videos/{video_id}"
        

        # Navigate to the appropriate URL (please set this to the correct URL)
        page.goto(url)

        page.wait_for_timeout(3000)

        # Wait for the "table" (i.e., grid layout) to load
        page.wait_for_selector(".group.relative.grid")

        # Extract timestamps and texts from each "row" in the "table"
        transcript_entries = page.query_selector_all(".group.relative.grid")
        transcript_data = []

        for entry in transcript_entries:
            # Get all text within a single entry
            full_text = entry.inner_text()
            transcript_data.append(full_text)

        full_text = "\n".join(transcript_data)
        full_text_cleaned = full_text.replace("♪", "")

        # Display the scraped data
        print(full_text_cleaned)

        # Save cookies to a local file after the session
        # cookies = context.cookies()
        # with open('cookies.json', 'w') as f:
        #     json.dump(cookies, f)

        # Close the browser
        browser.close()

        return full_text_cleaned


if __name__ == "__main__":
    scrape_youtube_transcript()