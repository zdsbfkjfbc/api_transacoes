from pydantic import BaseModel, Field
from datetime import datetime

class TransacaoIn(BaseModel):
    valor: float = Field(gt=0, description="O valor deve ser positivo")
    data_hora: datetime
    estabelecimento: str

# O que o usuário envia para logar
class LoginData(BaseModel):
    cpf: str
    senha: str   

# O que a API responde se der certo
class Token(BaseModel):
    access_token: str
    token_type: str