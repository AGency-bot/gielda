from langchain.tools import BaseTool
from typing import Union, Dict, Any
import pandas as pd
import os

class DecisionTool(BaseTool):
    name: str = "decide_if_order_is_good"
    description: str = "Podejmuje decyzję na podstawie segmentu i województwa, czy zlecenie pasuje do preferencji"

    def __init__(self):
        super().__init__()
        self._df = None  # prywatna zmienna przechowująca załadowaną tabelę

    @property
    def df(self):
        """Lazy load tablicy binarnej"""
        if self._df is None:
            path = os.path.join("dane", "tablica binarna segment + wojewodztwo.xlsx")
            df = pd.read_excel(path)
            df.columns = [str(c).strip().upper() for c in df.columns]
            self._df = df
        return self._df

    def _run(self, tool_input: Union[str, Dict[str, Any]], **kwargs) -> str:
        try:
            if not isinstance(tool_input, dict):
                return "❌ Oczekiwano obiektu typu dict z kluczami 'segment' i 'wojewodztwo'"

            segment = tool_input.get("segment", "").strip().upper()
            wojewodztwo = tool_input.get("wojewodztwo", "").strip().upper()

            if wojewodztwo not in self.df.columns:
                return f"❌ Nieznane województwo: {wojewodztwo}"
            if segment not in self.df["SEGMENT"].values:
                return f"❌ Nieznany segment: {segment}"

            wartosc = self.df.loc[self.df["SEGMENT"] == segment, wojewodztwo].values[0]

            return "TAK" if wartosc == 1 else "NIE"

        except Exception as e:
            return f"❌ Błąd w DecisionTool: {str(e)}"

    def _arun(self, tool_input: Union[str, Dict[str, Any]], **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
