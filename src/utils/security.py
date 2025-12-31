from datetime import datetime, timedelta
from typing import Optional
from jose import jwt 
from passlib.context import CryptContext

# Configurações do Token
# Em um projeto real, isso viria de varáiveis de ambiente
SECRET_KEY = "sua_chave_secreta_muito_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash(senha: str) -> str:
    """
    Recebe senha '123' e retorna o hash dela 'ab12cd34...'
    """
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Compara a senha em texto puro com o hash armazenado.
    """

    return pwd_context.verify(senha, senha_hash)

def criar_token_acesso(dados: dict):
    """
    Cria um JWT com tempo de validade.
    Recebe um dicionário (ex: {"sub": "cpf_do_usuario"})
    """
    to_encode = dados.copy()

    # Define quando o token expeira (agora + 30 minutos)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona a data de expiração ao token
    to_encode.update({"exp": expire})

    # Gera o token codificado 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    

    return encoded_jwt