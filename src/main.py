from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

# IMPORTS (Verifique se os caminhos batem com suas pastas)
from src.infra.database import get_db, Base, engine
from src.schemas import TransacaoIn
from src.infra.postgres_repository import TransacaoPostgresRepository
from src.use_cases.criar_transacao import CriarTransacaoUseCase

# Cria as tabelas no banco (se não existirem)
Base.metadata.create_all(bind=engine)

# Instancia a aplicação
app = FastAPI()

# --- ROTA POST (CRIAR) ---
@app.post("/transacao", status_code=status.HTTP_201_CREATED)
def criar_nova_transacao(transacao: TransacaoIn, db: Session = Depends(get_db)):
    
    # 1. Monta as peças
    repositorio = TransacaoPostgresRepository(db)
    caso_de_uso = CriarTransacaoUseCase(repositorio)

    # 2. Executa a lógica (com a regra dos 60s)
    sucesso = caso_de_uso.executar(transacao)

    # 3. Responde
    if sucesso is False:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    return {"mensagem": "Transação criada com sucesso!", "status": "ok"} # 201 Created vazio

# --- ROTA GET (ESTATÍSTICA) ---
@app.get("/estatistica")
def obter_estatisticas_transacoes(db: Session = Depends(get_db)):
    
    # 1. Define Janela de Tempo (Agora - 60s em UTC)
    janela_de_tempo = datetime.now(timezone.utc) - timedelta(seconds=60)

    # 2. Instancia o Repositório
    repositorio = TransacaoPostgresRepository(db)

    # 3. Pede para o banco calcular
    estatisticas = repositorio.calcular_estatisticas(janela_de_tempo)

    # 4. Retorna
    return estatisticas