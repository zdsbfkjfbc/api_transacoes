from src.infra.database import engine, Base
from src.infra.models import TransacaoDB

print("Tentando conectar e criar tabelas...")

Base.metadata.create_all(bind=engine)   
print("Tabelas criadas com sucesso!")