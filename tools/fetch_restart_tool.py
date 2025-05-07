from langchain_core.tools import BaseTool
from pydantic import BaseModel
from typing import Type
import requests
import time

class EmptyToolInput(BaseModel):
    """Brak danych wejściowych dla restartu Fetch."""
    pass

class FetchRestartTool(BaseTool):
    name: str = "restart_fetch"
    description: str = "Restartuje aplikację Fetch na Fly.io (najpierw /stop, potem /start)"
    args_schema: Type[BaseModel] = EmptyToolInput

    def _run(self, **kwargs) -> str:
        try:
            base_url = "https://fetch-2-0.fly.dev"

            stop_resp = requests.get(f"{base_url}/stop", timeout=5)
            time.sleep(2)
            start_resp = requests.get(f"{base_url}/start", timeout=5)

            if stop_resp.status_code != 200:
                return f"❌ Błąd zatrzymania Fetch: HTTP {stop_resp.status_code}"
            if start_resp.status_code != 200:
                return f"❌ Błąd uruchomienia Fetch: HTTP {start_resp.status_code}"

            return "✅ Fetch został pomyślnie zrestartowany"

        except Exception as e:
            return f"❌ Wyjątek podczas restartu Fetch: {str(e)}"

    def _arun(self, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
