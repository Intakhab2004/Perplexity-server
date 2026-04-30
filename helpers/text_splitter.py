




def generate_chunks(text: str, chunk_size: int = 40, overlap: int = 10):
    words = text.split()   # Word-based chunking

    chunks = []
    step = chunk_size - overlap

    if step <= 0:
        raise ValueError("Overlap must be smaller than chunk_size")
    
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks
