from langchain.tools import BaseTool
import requests

class FetchTool(BaseTool):
    name: str = "start_fetch"
    description: str = "Wywołuje endpoint /start w aplikacji Fetch na Fly.io, aby uruchomić scrapowanie"

    def _run(self, tool_input: str = "", **kwargs) -> str:
        try:
            url = "https://fetch.fly.dev/start"  # <- Zmień na swój właściwy endpoint, jeśli inny
            response = requests.get(url)
            response.raise_for_status()
            return f"Fetch uruchomiony. Odpowiedź: {response.text}"
        except Exception as e:
            return f"Błąd podczas wywołania Fetch: {str(e)}"

    def _arun(self, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
