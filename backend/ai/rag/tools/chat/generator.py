import os
from dotenv import load_dotenv
from ai.llm.client.chatbot import OAIChatClient

load_dotenv()

def generate_answer(query, context):
    default_system_prompt = """
    Anda adalah asisten AI yang sangat membantu dan dapat menjawab pertanyaan berdasarkan konteks.
    Jika jawaban tidak ada dalam konteks, katakan: 'Informasi tidak ditemukan dalam dokumen.'
    konteks nya adalah sebagai berikut: \n
    {context}
    \n
    Lalu jawab pertanyaan pengguna di bawah ini.
    """
    client = OAIChatClient(base_url=os.getenv('GENERATION_API_BASE'), api_key=os.getenv("GENERATION_API_KEY"), system_prompt=default_system_prompt)
    default_system_prompt = default_system_prompt.format(context=context)
    response_text = client.create_chat(query=query)

    return response_text
