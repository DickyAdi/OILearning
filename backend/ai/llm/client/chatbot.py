from openai import OpenAI, omit
from typing import Optional


from ._internals import ChatClient, EmbeddingClient


class OAIChatClient(ChatClient):
    """OpenAI Chat client. This class is responsible for creating a new chat to the OAI client.

    usage:
    ```
    >>> client = OAIChatClient(base_url='127.0.0.1', model='Gemma3')
    >>> response = client.create_chat(query='Hi, who are you?')
    ```
    """
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str = "localdummy",
        system_prompt: Optional[str] = None,
        tools: Optional[list[dict]] = None,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self.message_history = []
        if system_prompt:
            self.message_history.append({'role':'system', 'content': system_prompt})

    def create_chat(
        self,
        query: str,
        temperature: Optional[float] = 0.1,
        top_p: Optional[float] = 0.9,
    ) -> str:
        """Create a new chat for the client. Message history is maintained within the client instance.

        Args:
            query (str): User query/prompt. Must be a single string
            temperature (Optional[float], optional): Controll the temperature of the model. Defaults to 0.1.
            top_p (Optional[float], optional): Controll the top_p of the model. Defaults to 0.9.

        Returns:
            str: LLM response based on the given user query/prompt
        """
        msg = self.message_history.append({"role": "user", "content": query})
        resp = self.client.chat.completions.create(
            model=self.model,
            tools=self.tools if self.tools else omit,
            temperature=temperature,
            top_p=top_p,
            messages=msg,
        )
        resp_message = resp.choices[0].message
        # For now we ignore the function_call or tool_calls due to limited knowledge
        self.message_history.append(
            {"role": "assistant", "content": resp_message.content}
        )
        return resp_message.content


class OAIEmbeddingClient(EmbeddingClient):
    """OpenAI embedding client. This class is responsible for creating an embedding vector

    usage:
    ```
    >>> client = OAIEmbeddingClient(base_url='127.0.0.1')
    >>> vector = client.embed('Hello world')
    ```
    """
    def __init__(self, base_url: str, model: str, api_key: str = "localdummy"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def embed(self, query:str, dimensions:Optional[int] = 1024) -> list[float]:
        """Embed a query

        Args:
            query (str): Input query to be embed
            dimensions (Optional[int], optional): Control the dimension of the embeddings. Defaults to 1024.

        Returns:
            list[float]: Generated embeddings
        """
        embedding = self.client.embeddings.create(
            model=self.model,
            input=query,
            dimensions=dimensions
        ).data[-1].embedding

        return embedding