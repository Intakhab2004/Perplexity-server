import trafilatura
import requests
from bs4 import BeautifulSoup


def extract_content(html):
    if not html:
        return None
    
    try:
        content = trafilatura.extract(html)
        if content and len(content) > 200:
            return content
    except Exception as e:
        print(f"Trafilatura error: {e}")

    # Act as fallback means if trafilatura don't work
    try:
        soup = BeautifulSoup(html, "html.parser")

        # remove scripts & styles
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        return text
    
    except Exception as e:
        print(f"BS4 error: {e}")
        return None



def scrape_url(url: str):
    try:
        # parse html content from url
        response = requests.get(url=url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })

        if response.status_code != 200:
            print(f"Failed with status {response.status_code}")
            return None
        
        html = response.text

        # Extract content from html content using trafilatura or beautifulsoup4
        content = extract_content(html)

        # clean and limit the content
        if not content:
            return None
        
        text = " ".join(content.split())
        limited_text = text[:3000]

        # return clean content
        return limited_text

    except Exception as e:
        print(f"Something went while processing the url {str(e)}")
        return None
    
