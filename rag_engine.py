from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def split_text(text, chunk_size=400):

    if not text:
        return []

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def create_vector_db(chunks):

    if len(chunks) == 0:
        return None, None

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, embeddings


def retrieve_chunks(query, chunks, index, k=3):

    if index is None or len(chunks) == 0:
        return []

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = []

    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return results