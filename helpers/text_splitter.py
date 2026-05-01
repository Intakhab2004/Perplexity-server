




def split_text(text: str, chunk_size: int = 100, overlap: int = 25):
    words = text.split()   # Word-based chunking
    max_chunks = 12

    chunks = []
    step = chunk_size - overlap

    if step <= 0:
        raise ValueError("Overlap must be smaller than chunk_size")
    
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    chunks = chunks[:max_chunks]
