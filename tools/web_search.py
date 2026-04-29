from tavily import TavilyClient
from helpers.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


def search_query(sub_query: str): 
    try:
        response = tavily_client.search(
            query=sub_query,
            max_results=5,
            search_depth='advanced',
            exclude_domains=["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "pinterest.com", "flipboard.com"]
        )
    except Exception as e:
        raise ValueError(f"Something went wrong during web search {str(e)}")

    # Structuring output
    data = response["results"]
    formatted_data = [
        {
            "url": item["url"],
            "title": item["title"],
            "content": item["content"]
        }
        for item in data[:3]
    ]

    return formatted_data


     