from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. A String de Conexão
# Diz onde o banco está.
# "postgresql://usuario:senha@endereco:porta/nome_do_banco"
# Nota: Usamos 'localhost' aqui para testar rodando o Python fora do Docker por enquanto.
SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@db:5432/transacoes_db"

# 2. Criando o Motor de Conexão
# É quem gerencia a comunicação real com o banco de dados.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Criando a Sessão
# A sessão é como uma "aba do navegador" temporária para fazer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Declarativa
# É o "molde" mestre. Todas as suas tabelas vão herdar dessa classe Base.
Base = declarative_base()

# Função utilitária para pegar o banco de dados(usaramos depois no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

