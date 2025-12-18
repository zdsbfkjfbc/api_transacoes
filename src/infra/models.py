from sqlalchemy import Column, Integer, String, Float, DateTime
from src.infra.database import Base

class TransacaoDB(Base):
    # 1. Nome da Tabela
    __tablename__ = "transacoes"

    # 2. As colunas
    # primary_key=True: É o RG único de cada linha.
    # index=True: Cria um índice para buscas ficarem rápidas
    id = Column(Integer, primary_key=True, index=True)

    # Colunas de dados normais
    valor = Column(Float, nullable=False) # nullable=False obriga a ter valor
    data_hora = Column(DateTime, nullable=False)
    estabelecimento = Column(String, nullable=False)

    # Exemplo: Se tivéssemos cartão, seria:
    # cartao = Column(String, nullable=False)