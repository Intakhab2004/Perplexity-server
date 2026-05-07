import trafilatura
import requests
from bs4 import BeautifulSoup
from helpers.retry_request import create_session


def bs4_extractor(html):
    if not html:
        return None

    # Act as fallback means if trafilatura don't work
    try:
        soup = BeautifulSoup(html, "html.parser")

        # remove scripts & styles
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        cleaned_text = " ".join(text.split())

        if len(cleaned_text) < 200:
            return None
        
        return cleaned_text
    
    except Exception as e:
        print(f"BS4 error: {e}")
        return None



def scrape_url(url: str):
    try:
        # Trying trafilatura direclty
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            content = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_images=False,
                include_tables=False
            )

            if content and len(content) > 200:
                cleaned_content = " ".join(content.split())
                return cleaned_content[:3000]
            

        # Using request session for getting the html then again using trafilatura
        session = create_session()

        response = session.get(url=url, timeout=15)
        if response.status_code != 200:
            print(f"Failed with status {response.status_code} for {url}")
            return None
        
        html = response.text


        # Trying trafilatura again 
        content = trafilatura.extract(
            html,
            include_comments=False,
            include_images=False,
            include_tables=False
        )

        if content and len(content) > 200:
            cleaned_content = " ".join(content.split())
            return cleaned_content[:3000]
        
        # Now using BeautifulSoup as fallback
        fallback_content = bs4_extractor(html=html)
        if fallback_content:
            return fallback_content[:3000]
        
        return None

    except requests.exceptions.Timeout:
        print(f"Timeout while scraping: {url}")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

    except Exception as e:
        print(f"Something went while processing the url {str(e)}")
        return None