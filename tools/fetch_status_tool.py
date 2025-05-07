from langchain.tools import BaseTool
import requests

class FetchStatusTool(BaseTool):
    name: str = "fetch_status"
    description: str = "Sprawdza, czy aplikacja Fetch działa na Fly.io (czy pętla jest aktywna)"

    def _run(self, tool_input: str = "", **kwargs) -> str:
        try:
            url = "https://fetch.fly.dev/status"  # zamień na swój adres, jeśli inny
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("running") is True:
                    return "RUNNING"
                elif data.get("running") is False:
                    return "IDLE"
                else:
                    return "UNKNOWN"
            return f"HTTP {response.status_code}"
        except Exception as e:
            return f"BŁĄD: {str(e)}"

    def _arun(self, tool_input: str = "", **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
