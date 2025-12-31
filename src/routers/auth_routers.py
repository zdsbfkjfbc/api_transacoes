from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.database import get_db
from src.infra.usuario_repository import UsuarioRepository
from src.utils.security import verificar_senha, criar_token_acesso
from src.schemas import LoginData, Token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", tags=["Autenticação"])
def login_para_acesso(dados_login: LoginData, db: Session = Depends(get_db)):
    # 1. Busca o usuario pelo o CPF 
    repo = UsuarioRepository(db)
    usuario = repo.obter_cpf(dados_login.cpf)

    # 2. Se não achou usuario ou a senha está errada -> Erro
    if not usuario or not verificar_senha(dados_login.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos",
        )
    
    # 3. Se deu tudo certo, cria o token de acesso
    token_jwt = criar_token_acesso(dados={"sub": usuario.cpf})

    return {"access_token": token_jwt, "token_type": "bearer"}
   

   