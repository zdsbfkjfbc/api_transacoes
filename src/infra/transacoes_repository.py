from sqlalchemy.orm import Session
from src.infra.models import TransacaoDB


class TransacoesRepository:
    def __init__(self, db_session):
        self.db = db_session

    
    def criar(self, transacao: TransacaoDB):
        self.db.add(transacao)
        self.db.commit()
        self.db.refresh(transacao)
        return transacao
    
    def listar(self):
        return self.db.query(TransacaoDB).all()
