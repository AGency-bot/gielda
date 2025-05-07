from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Type
import json
import os

KOD_WOJ = {
    "00": "MAZOWIECKIE", "01": "MAZOWIECKIE", "02": "MAZOWIECKIE", "03": "MAZOWIECKIE", "04": "MAZOWIECKIE",
    "05": "MAZOWIECKIE",
    "10": "WARMIŃSKO-MAZURSKIE",
    "15": "PODLASKIE",
    "20": "LUBELSKIE",
    "25": "ŚWIĘTOKRZYSKIE",
    "30": "MAŁOPOLSKIE", "31": "MAŁOPOLSKIE",
    "35": "PODKARPACKIE",
    "40": "ŚLĄSKIE", "45": "OPOLSKIE",
    "50": "DOLNOŚLĄSKIE", "51": "DOLNOŚLĄSKIE", "52": "DOLNOŚLĄSKIE", "53": "DOLNOŚLĄSKIE", "54": "DOLNOŚLĄSKIE",
    "60": "WIELKOPOLSKIE", "61": "WIELKOPOLSKIE",
    "65": "LUBUSKIE",
    "70": "ZACHODNIOPOMORSKIE", "71": "ZACHODNIOPOMORSKIE", "75": "ZACHODNIOPOMORSKIE",
    "80": "POMORSKIE", "81": "POMORSKIE", "82": "POMORSKIE", "83": "POMORSKIE", "84": "POMORSKIE",
    "85": "KUJAWSKO-POMORSKIE",
    "90": "ŁÓDZKIE", "91": "ŁÓDZKIE", "92": "ŁÓDZKIE", "93": "ŁÓDZKIE", "94": "ŁÓDZKIE",
}

class MapperInput(BaseModel):
    wojewodztwo_id: Optional[str] = Field(None, description="ID województwa z rekordu (np. selXYZ123)")
    kod_pocztowy: Optional[str] = Field(None, description="Kod pocztowy w formacie NN-NNN")

class WojewodztwoMapperTool(BaseTool):
    name: str = "mapuj_wojewodztwo"
    description: str = "Mapuje ID województwa lub kod pocztowy na nazwę województwa"
    args_schema: Type[BaseModel] = MapperInput

    def __init__(self):
        super().__init__()
        self._mapa_id = None

    def _load_id_map(self):
        if self._mapa_id is None:
            path = os.path.join("dane", "wojewodztwa_mapping.json")
            with open(path, "r", encoding="utf-8") as f:
                self._mapa_id = json.load(f)
        return self._mapa_id

    def _run(self, tool_input: MapperInput, **kwargs) -> str:
        try:
            mapa = self._load_id_map()

            if tool_input.wojewodztwo_id and tool_input.wojewodztwo_id in mapa:
                return mapa[tool_input.wojewodztwo_id]

            if tool_input.kod_pocztowy:
                prefix = tool_input.kod_pocztowy.replace("-", "")[:2]
                if prefix in KOD_WOJ:
                    return KOD_WOJ[prefix]

            return "❌ Nie udało się rozpoznać województwa"

        except Exception as e:
            return f"❌ Błąd mapowania: {str(e)}"

    def _arun(self, tool_input: MapperInput, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")

# ✅ Funkcja pomocnicza do użytku poza agentem
def resolve_wojewodztwo(raw_value: str) -> Optional[str]:
    try:
        path = os.path.join("dane", "wojewodztwa_mapping.json")
        with open(path, "r", encoding="utf-8") as f:
            mapa_id = json.load(f)

        if raw_value in mapa_id:
            return mapa_id[raw_value]

        prefix = raw_value.replace("-", "")[:2]
        return KOD_WOJ.get(prefix)

    except Exception:
        return None
