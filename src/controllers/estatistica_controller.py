from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  


# Imports do Projeto
from src.infra.database import get_db
from src.infra.postgres_repository import TransacaoPostgresRepository
from src.use_cases.calcular_estatisticas import CalcularEstatisticasUseCase

router = APIRouter()    

@router.get("/estatisticas", status_code=200)

def obter_estatisticas(db: Session = Depends(get_db)):

    # 1. Instância o Repositório (Conectando ao Postgres)
    repositorio = TransacaoPostgresRepository(db)

    # 2. Instância o Use Case (Injetando o Repositório)
    use_case = CalcularEstatisticasUseCase(repositorio)

    # 3. Executa a logica e retorna o dicionário pronto
    resultado = use_case.executar()
    
    return resultado