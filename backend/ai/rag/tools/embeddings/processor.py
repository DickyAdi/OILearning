from .extractors import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from .chunker import chunk_text
from .embedder import Embedder
from .milvus_store import init_collection, insert_embeddings

def process_file(file_path, filename):
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        text = extract_text_from_pdf(open(file_path, "rb"))
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    elif ext == "txt":
        text = extract_text_from_txt(open(file_path, "rb"))
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    chunks = chunk_text(text)
    embedder = Embedder() 
    embeddings = [embedder.embed(chunk) for chunk in chunks]

    collection = init_collection()
    insert_embeddings(collection, embeddings, chunks, filename)

    return len(chunks)
