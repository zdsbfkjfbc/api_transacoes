from pydantic import BaseModel
from datetime import datetime

# O que "ENTRA" Input
# Este é o "Molde" dos dados que o cliente vai enviar no POST /transacao
class TransacaoIn(BaseModel):
    valor: float
    data_hora: datetime

# O que "SAI" Output
# Este é o "Molde" das estatísticas que vamos devolver no GET /estatistica
class EstatisticaOut(BaseModel):
    count: int
    sum: float
    avg: float
    min: float
    max: float

