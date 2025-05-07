from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd
import os
from tools.mapper_tool import resolve_wojewodztwo

class DecisionInput(BaseModel):
    segment: str = Field(..., description="Segment pojazdu, np. TIR, C, D")
    wojewodztwo: str = Field(..., description="ID województwa lub kod pocztowy (np. 'selYHX5...', '05-300')")

class DecisionTool(BaseTool):
    name: str = "decide_if_order_is_good"
    description: str = "Podejmuje decyzję, czy zlecenie pasuje do preferencji na podstawie segmentu i województwa"
    args_schema: Type[BaseModel] = DecisionInput

    def __init__(self):
        super().__init__()
        self._df = None

    @property
    def df(self):
        if self._df is None:
            path = os.path.join("dane", "tablica binarna segment + wojewodztwo.xlsx")
            df = pd.read_excel(path)
            df.columns = [str(c).strip().upper() for c in df.columns]
            self._df = df
        return self._df

    def _run(self, *, tool_input: DecisionInput, **kwargs) -> str:
        try:
            segment = tool_input.segment.strip().upper()
            wojewodztwo = tool_input.wojewodztwo.strip()
            resolved = resolve_wojewodztwo(wojewodztwo)

            if not resolved:
                return f"❌ Nie udało się rozpoznać województwa dla: {wojewodztwo}"

            resolved = resolved.upper()
            if resolved not in self.df.columns:
                return f"❌ Województwo '{resolved}' nie występuje w tabeli preferencji"

            if segment not in self.df["SEGMENT"].values:
                return f"❌ Segment '{segment}' nie występuje w tabeli preferencji"

            wartosc = self.df.loc[self.df["SEGMENT"] == segment, resolved].values[0]
            return "TAK" if wartosc == 1 else "NIE"

        except Exception as e:
            return f"❌ Błąd w DecisionTool: {str(e)}"

    def _arun(self, *, tool_input: DecisionInput, **kwargs):
        raise NotImplementedError("Async niezaimplementowany")
