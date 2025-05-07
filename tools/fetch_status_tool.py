from langchain_core.tools import BaseTool
from pydantic import BaseModel
from typing import Type
import requests

class EmptyToolInput(BaseModel):
    """Brak danych wejściowych."""
    pass

class FetchStatusTool(BaseTool):
    name: str = "fetch_status"
    description: str = "Sprawdza, czy aplikacja Fetch działa na Fly.io (czy pętla jest aktywna)"
    args_schema: Type[BaseModel] = EmptyToolInput

    def _run(self, **kwargs) -> str:
        try:
            url = "https://fetch-2-0.fly.dev/status"
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

    def _arun(self, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
