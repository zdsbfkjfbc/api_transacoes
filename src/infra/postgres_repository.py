from sqlalchemy.orm import Session  
from sqlalchemy import func
from datetime import datetime
from src.infra.models import TransacaoDB
from src.schemas import TransacaoIn

class TransacaoPostgresRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, transacao: TransacaoIn): 
        # 1. Mapper: Converter o objeto de Domínio (Pydantic) para Modelo de Banco (SQLAlchemy)
        # Note que não passamos o ID, o banco gera automático.
        db_transacao = TransacaoDB(
            valor = transacao.valor,
            data_hora = transacao.data_hora,
            estabelecimento = "Loja Exemplo",  # Valor fixo para simplificação
        )

        # 2. Adicionar na sessão (Stanging)
        self.db.add(db_transacao)

        # 3. Commitar (Persistir no disco)
        self.db.commit()

        # 4. Refresh: Atualizar o objeto com os dados do banco (ex: ID gerado)
        self.db.refresh(db_transacao)

        return db_transacao
    
    def calcular_estatisticas(self, janela_de_tempo: datetime):
        """
        Busca e calcula estatísticas das transações direto no banco (SQL).
        """
        # Monta a query usando funções de agregação no SQL
        query = self.db.query(
            func.count(TransacaoDB.id),
            func.coalesce(func.sum(TransacaoDB.valor), 0.0),
            func.coalesce(func.avg(TransacaoDB.valor), 0.0),
            func.coalesce(func.min(TransacaoDB.valor), 0.0),
            func.coalesce(func.max(TransacaoDB.valor), 0.0),
        ).filter(
            TransacaoDB.data_hora >= janela_de_tempo
        )

        # Executa
        resultado = query.first()

        print(f"Resultado do Banco: {resultado}")

        # O resultado vem como uma Tupla: (10, 150.0, 15.0, 10.0, 20.0)
        # Se não houver transações, vem: (0, None, None, None, None)
        
        # Tratamento de Nulos (Resposta da Pergunta de Pleno):
        # O SQL retorna NULL (None no Python) quando não soma nada.
        # Python odeia matemática com None (dá erro). Por isso usamos o
        #  "or 0.0"
        estatisticas={
            "count" : resultado[0] or 0,
            "sum" : resultado[1] or 0.0,  
            "avg" : resultado[2] or 0.0,
            "min" : resultado[3] or 0.0,
            "max" : resultado[4] or 0.0,
        }

        return estatisticas