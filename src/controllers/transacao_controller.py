from fastapi import APIRouter, HTTPException, status, Response
from src.models.schemas import TransacaoIn

# Aqui importarei o nosso use case
from src.use_cases.criar_transacao import CriarTransacaoUseCase 

router = APIRouter()

@router.post("/transacoes", status_code=status.HTTP_201_CREATED)
def criar_transacao(transacao: TransacaoIn, response: Response):
    #1. Instancia o use case

    use_case = CriarTransacaoUseCase()

    try:

        # 2. Executa o use case
        resultado = use_case.execute(transacao) 

        # 3. Traduz a resposta do Use Case para a resposta HTTP 
        if resultado is False:
            # Se o Use Case disse "False" (Ignorar), devolvemos 204
            response.status_code = status.HTTP_204_NO_CONTENT
            return response
        
        #Se deu tudo certo, o 201 é automático
        return 
    
    except ValueError as e:
        # 4. Se o Use Case gritou um erro de valor, transformamos em 422
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    