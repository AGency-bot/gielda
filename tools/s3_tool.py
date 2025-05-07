from langchain_core.tools import BaseTool
from typing import Optional, List, Dict, Type
from pydantic import BaseModel
import boto3
import os
import json

from tools.mapper_tool import MapperTool

class EmptyToolInput(BaseModel):
    """Brak argumentów wejściowych dla narzędzia."""
    pass

class S3Tool(BaseTool):
    name: str = "load_new_orders"
    description: str = "Porównuje 2 najnowsze snapshoty z S3 i zwraca tylko nowe zlecenia"
    args_schema: Type[BaseModel] = EmptyToolInput

    def _run(self, **kwargs) -> str:
        try:
            new_orders = self.get_new_orders()
            if not new_orders:
                return "Brak nowych zleceń"
            return json.dumps(new_orders, indent=2)
        except Exception as e:
            return f"Błąd: {str(e)}"

    def _arun(self, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")

    def get_new_orders(self) -> List[Dict]:
        """Zwraca listę nowych rekordów z przetłumaczonym województwem."""
        bucket_name = os.environ.get("S3_BUCKET_NAME")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION"),
        )

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix="motoassist/")
        if "Contents" not in response or len(response["Contents"]) < 2:
            return []

        objects = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
        latest_key = objects[0]["Key"]
        previous_key = objects[1]["Key"]

        latest_data = self._load_snapshot(s3, bucket_name, latest_key)
        previous_data = self._load_snapshot(s3, bucket_name, previous_key)

        latest_ids = {r["id"] for r in latest_data.get("records", [])}
        previous_ids = {r["id"] for r in previous_data.get("records", [])}

        new_ids = latest_ids - previous_ids
        new_records = [r for r in latest_data.get("records", []) if r["id"] in new_ids]

        # 🧠 Dodajemy mapowanie województw
        mapper = MapperTool()
        for record in new_records:
            raw_value = record.get("cellValuesByColumnId", {}).get("fldCbMMnj7vuHlmsu")
            mapped = mapper.run(tool_input={"value": raw_value})
            record["mapped_wojewodztwo"] = mapped  # dodajemy do rekordu

        return new_records

    def _load_snapshot(self, s3, bucket_name: str, key: str) -> Dict:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        return json.loads(obj["Body"].read())

    def _get_full_snapshot(self) -> Optional[Dict]:
        """Zwraca pełny najnowszy snapshot (dict)."""
        try:
            bucket_name = os.environ.get("S3_BUCKET_NAME")
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                region_name=os.environ.get("AWS_REGION"),
            )

            response = s3.list_objects_v2(Bucket=bucket_name, Prefix="motoassist/")
            if "Contents" not in response:
                return None

            objects = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
            latest_key = objects[0]["Key"]
            return self._load_snapshot(s3, bucket_name, latest_key)
        except Exception as e:
            print(f"Błąd pobierania pełnego snapshotu: {str(e)}")
            return None
