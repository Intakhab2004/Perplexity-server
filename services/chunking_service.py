from helpers.text_splitter import split_text;


def generate_chunks(search_agent_output):
    if not search_agent_output:
        raise ValueError("Search agent output is not provided")
    
    structured_chunks = []
    
    for item in search_agent_output:
        result_lists = item["results"]

        for result in result_lists:
            text = result.get("content", {}).get("full_text")
            if not text:
                continue

            text = " ".join(text.split())
            chunks = split_text(text)

            for chunk in chunks:
                if len(chunk.split()) < 8:
                    continue

                chunk_detail = {
                    "text": chunk,
                    "title": result.get("title", ""),
                    "source": result["url"],
                    "question": item["question"],
                }
        
                structured_chunks.append(chunk_detail)

    if not structured_chunks:
        print("No chunks generated")

    return structured_chunks




