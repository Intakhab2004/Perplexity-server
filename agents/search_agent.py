from typing import List
from tools.web_search import search_query
from tools.url_scraper import scrape_url


def search(sub_questions: List[str]):
    final_results = []

    for question in sub_questions:
        web_result = search_query(question)

        result_lists = []
        for item in web_result:
            if not item["content"] or len(item["content"]) < 100:
                continue
            else:
                detailed_content = scrape_url(url=item["url"])
                if detailed_content:
                    item["content"] = {
                        "summary": item["content"],
                        "full_text": detailed_content
                    }
                
                    result_lists.append(item)

        final_results.append({
            "question": question,
            "results": result_lists
        })
    
    return final_results

            



