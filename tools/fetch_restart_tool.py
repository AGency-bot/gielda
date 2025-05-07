from langchain.tools import BaseTool
import requests
import time

class FetchRestartTool(BaseTool):
    name: str = "restart_fetch"
    description: str = "Restartuje aplikację Fetch na Fly.io (najpierw /stop, potem /start)"

    def _run(self, tool_input: str = "", **kwargs) -> str:
        try:
            base_url = "https://fetch.fly.dev"  # zmień, jeśli masz inny adres

            # Krok 1: zatrzymaj
            stop_resp = requests.get(f"{base_url}/stop", timeout=5)
            time.sleep(2)

            # Krok 2: uruchom ponownie
            start_resp = requests.get(f"{base_url}/start", timeout=5)

            if stop_resp.status_code != 200:
                return f"❌ Błąd zatrzymania Fetch: HTTP {stop_resp.status_code}"
            if start_resp.status_code != 200:
                return f"❌ Błąd uruchomienia Fetch: HTTP {start_resp.status_code}"

            return "✅ Fetch został pomyślnie zrestartowany"

        except Exception as e:
            return f"❌ Wyjątek podczas restartu Fetch: {str(e)}"

    def _arun(self, tool_input: str = "", **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
