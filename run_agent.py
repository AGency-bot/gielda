import os
from dotenv import load_dotenv
load_dotenv()
import json
from tools.fetch_tool import FetchTool
from tools.fetch_status_tool import FetchStatusTool
from tools.fetch_restart_tool import FetchRestartTool
from tools.s3_tool import S3Tool
from tools.decision_tool import DecisionTool  # ✅ Usunięto DecisionInput

def main():
    print("=== STATUS: sprawdzanie Fetch ===")
    status = FetchStatusTool()
    response = status.run(tool_input="")

    print(f"ℹ️ Status Fetch: {response}")

    if "offline" in response.lower() or "błąd" in response.lower():
        print("🔁 Fetch nie działa – próbuję restart...")
        restarter = FetchRestartTool()
        restart_response = restarter.run(tool_input="")
        print(f"🔄 {restart_response}")

    print("\n=== TEST: uruchomienie FetchTool ===")
    fetch = FetchTool()
    print(fetch.run(tool_input=""))  # bezpieczne nawet jeśli już działa

    print("\n=== TEST: pobranie snapshotu z S3Tool ===")
    s3 = S3Tool()
    full_snapshot = s3._get_full_snapshot()

    if full_snapshot is None:
        print("❌ Brak danych w snapshotcie.")
        return

    print("\n=== TEST: wyodrębnianie pierwszego rekordu ===")
    records = full_snapshot.get("records", [])
    if not records:
        print("❌ Brak rekordów w snapshotcie.")
        return

    first_record = records[0]
    segment = first_record.get("cellValuesByColumnId", {}).get("fldfEIZxM3O4pF3bW", "").upper()
    wojewodztwo = first_record.get("cellValuesByColumnId", {}).get("fldCbMMnj7vuHlmsu", "").upper()

    print(f"📦 Zlecenie: segment = {segment}, województwo = {wojewodztwo}")

    print("\n=== TEST: decyzja ===")
    decider = DecisionTool()
    decyzja = decider.run(tool_input={
        "segment": segment,
        "wojewodztwo": wojewodztwo
    })  # ✅ dict, nie Pydantic
    print(f"🧠 Decyzja agenta: {decyzja}")

if __name__ == "__main__":
    main()
