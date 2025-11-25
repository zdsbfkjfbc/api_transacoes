from fastapi import APIRouter, HTTPException, status, Response
from src.models.schemas import TransacaoIn
from datetime import datetime, timezone

router = APIRouter()    

@router.post("/transacao", status_code=status.HTTP_201_CREATED)

def criar_transacao(transacao: TransacaoIn, response: Response):
    
    # 1. Pega a data e hora atual em UTC para comparar com a transação
    agora = datetime.now(timezone.utc)

    # 2. Validação: Transação no futuro ->  422
    if transacao.data_hora > agora:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A transação não pode ser no futuro."
        )   
    
    # 3. Validação: Transação com mais de 60 segundos -> 204
    diferenca = (agora - transacao.data_hora).total_seconds()

    if diferenca > 60:
        # Mudamos o status para 204 (No Content)
        response.status_code = status.HTTP_204_NO_CONTENT

        # Retornamos o objeto response (sem corpo, pois é 204)

        return response
    
    # Por enquanto, vamos apenas imprimir no console para provar que chegou
    print(f"Processando transação valida! Valor: {transacao.valor}")

    return {}