from sqlalchemy.orm import Session
from src.infra.models import UsuarioDB

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter_cpf(self, cpf: str):
        return self.db.query(UsuarioDB).filter(UsuarioDB.cpf == cpf).first()
        
    def criar(self, usuario: UsuarioDB):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario