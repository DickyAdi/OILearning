from ai.rag.tools.chat.retriever import retrieve_context_milvus, retrieve_context_file
from ai.rag.tools.chat.generator import generate_answer


def rag_vdb(query: str):
    """
    RAG Global → Mengambil jawaban berdasarkan semua dokumen
    yang sudah disimpan dalam Milvus Vector Database.
    """
    context = retrieve_context_milvus(query)
    answer = generate_answer(query, context)
    return answer


def rag_pdf(query: str, file_path: str):
    """
    RAG Local → Mengambil jawaban hanya dari file PDF/DOCX/TXT tertentu
    dengan vector DB sementara (in-memory Qdrant).
    """
    context = retrieve_context_file(query, file_path=file_path)
    answer = generate_answer(query, context)
    return answer
