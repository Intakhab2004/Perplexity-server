import trafilatura
from bs4 import BeautifulSoup
import httpx


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
}


async def scrape_url(url: str):
    try:
        html = None

        # Trying trafilatura to download html
        try:
            downloaded = trafilatura.fetch_url(url=url)
            if downloaded:
                html = downloaded
        
        except Exception as e:
            print(f"Trafilatura failed for {url}: {e}")

        if not html:
            # Creating async client for scrapping
            async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
                response = await client.get(
                    url=url,
                    headers=HEADERS
                )
                
            if response.status_code != 200:
                print(f"Failed with status {response.status_code} for {url}")
                return None

            html = response.text
            

        # Trying trafilatura extraction
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
        soup = BeautifulSoup(html, "html.parser")

        # remove scripts & styles
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.extract()
        
        text = soup.get_text(separator=" ")
        cleaned_text = " ".join(text.split())

        if len(cleaned_text) > 200:
            return cleaned_text[:3000]
        
        return None

    except Exception as e:
        print(f"Something went wrong while scrapping the url {str(e)}")
        return None