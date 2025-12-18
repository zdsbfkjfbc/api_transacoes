import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import do projeto atual
from src.main import app
from src.infra.database import Base, get_db

# 1. Configuração do Banco em Memória (SQLite)
# Usamos ":memory:" para criar um banco que vive na RAM. Desligou, sumiu.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Necessário para SQLite
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. A Fixture da Sessão de Banco
# Isso roda ANTES de cada teste
@pytest.fixture(scope="function")
def session ():
    # Cria as tabelas vazias no banco de memória
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()
        # Ao final, destruimos as tabelas para o próximo teste começar limpo
        Base.metadata.drop_all(bind=engine) 

# 3. O Cliente de Teste (O "Navegador Robô")
@pytest.fixture(scope="function")
def client(session):
    # A MÁGICA DA TROCA (Dependency Override):
    # Ensinamos a API a usar o nosso banco de memória em vez do Postgres real
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db

    # Entrega o cliente pronto para fazer as requisições
    with TestClient(app) as c:
        yield c