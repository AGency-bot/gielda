from langchain.tools import BaseTool
import requests
from typing import Optional, Union, Dict, Any

class FetchTool(BaseTool):
    name: str = "start_fetch"
    description: str = "Wywołuje endpoint /start w aplikacji Fetch na Fly.io, aby uruchomić scrapowanie danych giełdowych"

    def _run(self, tool_input: Union[str, Dict[str, Any]] = "", **kwargs) -> str:
        try:
            url = "https://fetch.fly.dev/start"  # <- Zmień na swój prawdziwy endpoint, jeśli inny
            response = requests.get(url)
            response.raise_for_status()
            return f"✅ Fetch uruchomiony. Odpowiedź: {response.text}"
        except Exception as e:
            return f"❌ Błąd podczas wywołania Fetch: {str(e)}"

    def _arun(self, tool_input: Union[str, Dict[str, Any]] = "", **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
