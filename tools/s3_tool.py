from langchain.tools import BaseTool
import boto3
import os
import json

class S3Tool(BaseTool):
    name: str = "load_latest_snapshot"
    description: str = "Pobiera najnowszy snapshot JSON z folderu 'motoassist/' w S3 i zwraca jego zawartość"

    def _run(self, tool_input: str = "", **kwargs) -> str:
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
                return "Brak plików w folderze 'motoassist/'"

            # sortujemy po dacie
            objects = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
            latest_key = objects[0]["Key"]

            obj = s3.get_object(Bucket=bucket_name, Key=latest_key)
            json_bytes = obj["Body"].read()
            data = json.loads(json_bytes)

            return json.dumps(data, indent=2)[:2000]  # skracamy output do 2000 znaków
        except Exception as e:
            return f"Błąd pobierania z S3: {str(e)}"

    def _arun(self, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
