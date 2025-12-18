from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session

# Importando de Infra e Use Case

from src.schemas import TransacaoIn
from src.use_cases.criar_transacao import CriarTransacaoUseCase
from src.infra.database import get_db # Pegamos a função de conexão
from src.infra.postgres_repository import TransacaoPostgresRepository # <--- O Repositório Real

router = APIRouter()

@router.post("/transacoes", status_code=status.HTTP_201_CREATED)
def criar_transacao_endpoint(
    transacao: TransacaoIn, 
    db: Session = Depends(get_db)  # Injetando a sessão do banco
): 

    # 1. Criamos o repositório passando o banco de dados da requisição
    repositorio = TransacaoPostgresRepository(db)

    # 2. Passamos o repositório para o Use Case (Clean Architecture)
    use_case = CriarTransacaoUseCase(repositorio)

    # 3. Executamos o Use Case
    use_case.executar(transacao)

    # O retorno pode ser vazio (201 Created) ou uma mensagem, conforme definimos antes
    return {"message": "Transação criada com sucesso!"}
