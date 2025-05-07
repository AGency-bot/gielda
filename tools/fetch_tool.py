from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel
import requests

class EmptyInput(BaseModel):
    """Brak argumentów wejściowych dla FetchTool."""
    pass

class FetchTool(BaseTool):
    name: str = "start_fetch"
    description: str = "Wywołuje endpoint /start w aplikacji Fetch na Fly.io, aby uruchomić scrapowanie danych giełdowych"
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self, *, tool_input: EmptyInput, **kwargs) -> str:
        try:
            url = "https://fetch-2-0.fly.dev/start"
            response = requests.get(url)
            response.raise_for_status()
            return f"✅ Fetch uruchomiony. Odpowiedź: {response.text}"
        except Exception as e:
            return f"❌ Błąd podczas wywołania Fetch: {str(e)}"

    def _arun(self, *, tool_input: EmptyInput, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
