import os
import json
from tools.fetch_tool import FetchTool
from tools.s3_tool import S3Tool
from tools.decision_tool import DecisionTool

def main():
    print("=== TEST: uruchomienie FetchTool ===")
    fetch = FetchTool()
    print(fetch.run(tool_input=""))  # poprawka: jawne przekazanie tool_input

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
    wojewodztwo = first_record.get("cellValuesByColumnId", {}).get("fldCbMMnj7vuHlmsu", "").capitalize()

    print(f"📦 Zlecenie: segment = {segment}, województwo = {wojewodztwo}")

    print("\n=== TEST: decyzja ===")
    decider = DecisionTool()
    decyzja = decider.run(tool_input={
        "segment": segment,
        "wojewodztwo": wojewodztwo
    })

    print(f"🧠 Decyzja agenta: {decyzja}")

if __name__ == "__main__":
    main()
