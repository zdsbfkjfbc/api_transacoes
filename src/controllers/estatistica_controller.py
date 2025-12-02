from fastapi import APIRouter, status
from src.models.schemas import EstatisticaOut
from src.use_cases.calcular_estatisticas import CalcularEstatisticasUseCase

router = APIRouter()    

# Note: response_model=EstatisticaOut
# Isso diz ao Swagger: "Essa rota vai devolver aquele JSON com count, sum, etc"
@router.get("/estatisticas", response_model=EstatisticaOut, status_code=status.HTTP_200_OK)

def obter_estatisticas():

    use_case = CalcularEstatisticasUseCase()
    resultado = use_case.execute()

    return resultado

