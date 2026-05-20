from typing import List
from collections import defaultdict
import asyncio
from tools.web_search import search_query
from tools.url_scraper import scrape_url



async def search(sub_questions: List[str]):

    # Async web search using tavily
    search_tasks = [search_query(question) for question in sub_questions]
    search_results = await asyncio.gather(*search_tasks)


    # Deduplicate urls
    seen_urls = set()
    unique_search_results = []

    for question, results in zip(sub_questions, search_results):
        for item in results:
            if not item["content"] or len(item["content"]) < 100:
                continue

            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])

                unique_search_results.append({
                    "question": question,
                    "url": item["url"],
                    "title": item["title"],
                    "summary": item["content"]
                })

    # Async url scrapping
    scrape_tasks = [scrape_url(item["url"]) for item in unique_search_results]
    scraped_contents = await asyncio.gather(*scrape_tasks)


    # Building final response
    grouped = defaultdict(list)

    for result, content in zip(unique_search_results, scraped_contents):
        if content:
            grouped[result["question"]].append({
                "url": result["url"],
                "title": result["title"],
                "content": {
                    "summary": result["summary"],
                    "full_text": content
                }
            })
    
    final_results = [
        {
            "question": question,
            "results": results
        }
        for question, results in grouped.items()
    ]

    return final_results

            



