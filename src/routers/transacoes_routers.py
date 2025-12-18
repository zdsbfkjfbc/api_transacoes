from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.database import get_db
from src.schemas import TransacaoIn
from src.repositories.transacoes_repository import TransacoesRepository
from src.use_cases.criar_transacao import CriarTransacaoUseCase

# Cria o agrupador de rotas 
router = APIRouter()    


@router.post("/transacoes", status_code=status.HTTP_201_CREATED)
def criar_nova_transacao (
    transacao: TransacaoIn,            # 1. FastAPI valida o JSON aqui
    db: Session = Depends(get_db)      # 2. Injeção de dependência do DB
):
    """
    Recebe uma transação, valida e salva.
    Se a transação for muito antiga (>60s), retorna 422.
    """
    
    # 3. MONTAGEM DAS PEÇAS (Wiring)
    # Criamos o repositório passando o banco de dados real

    repositorio = TransacoesRepository(db)

    # Criamos o use case, passando o repositório real   
    caso_de_uso = CriarTransacaoUseCase(repositorio)    

    # 4. EXECUÇÃO 
    # Chamamos a lógica que testamos (que tem a regra dos 60s)
    # Note que agora estamos passando o OBJETO transacao inteiro
    sucesso = caso_de_uso.executar(transacao)

    # 5. Resposta
    if sucesso is False:
        # Se retornou False (regra dos 60s), lançamos erro 422 (Unprocessable Entity)
        # 422 é o padrão REST para "Entendi o formato, mas não aceito esse dado"
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # Se deu tudo certo, retornamos 201 (Created) sem corpo
    return