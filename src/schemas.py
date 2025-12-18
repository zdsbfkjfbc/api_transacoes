from pydantic import BaseModel, Field
from datetime import datetime

class TransacaoIn(BaseModel):
    valor: float = Field(gt=0, description="O valor deve ser positivo")
    data_hora: datetime