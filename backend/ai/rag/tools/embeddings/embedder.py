import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load .env automatically

class Embedder:
    def __init__(self, model=None):
        self.base_url = os.getenv("EMBEDDING_API_BASE")
        self.api_key = os.getenv("EMBEDDING_API_KEY")
        self.model = model or os.getenv("EMBEDDING_MODEL")

        if not self.base_url or not self.api_key:
            raise RuntimeError(
                "ENV ERROR: EMBEDDING_API_BASE or EMBEDDING_API_KEY not set in environment."
            )

        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def embed(self, text):
        res = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return res.data[0].embedding
