import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_answer(query, context):
    client = OpenAI(
        base_url=os.getenv("GENERATION_API_BASE"),
        api_key=os.getenv("GENERATION_API_KEY")
    )

    system_prompt = (
        "Anda adalah asisten AI yang menjawab berdasarkan konteks. "
        "Jika jawaban tidak ada dalam konteks, katakan: 'Informasi tidak ditemukan dalam dokumen.'"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Konteks:\n{context}\n\nPertanyaan: {query}"}
    ]

    response = client.chat.completions.create(
        model=os.getenv("GENERATION_MODEL"),
        messages=messages,
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content
