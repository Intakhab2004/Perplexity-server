from tavily import TavilyClient
from helpers.config import settings
import asyncio

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


def sync_search_query(sub_query: str): 
    try:
        response = tavily_client.search(
            query=sub_query,
            max_results=3,
            search_depth='ultra-fast',
            exclude_domains=["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "pinterest.com", "flipboard.com", "medium.com", "quora.com"]
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


# async function for (web search) using asyncio.to_thread method to prevent event_loop blocking
async def search_query(sub_query: str):
    try:
        result = await asyncio.to_thread(
            sync_search_query,
            sub_query
        )

        return result

    except Exception as e:
        print(f"Tavily search error: {e}")
        return []