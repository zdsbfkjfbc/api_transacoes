from datetime import datetime, timezone
from src.models.schemas import TransacaoIn

from src.infra.transacoes_repository import TransacoesRepository

class CriarTransacaoUseCase:
    
    def execute(self, transacao: TransacaoIn) -> bool:

        """
        Executa as regras de negócio para criar uma nova transação.
        Retorna: True se criou, False se deve ignorar (204), ou levanta erro.
        """

        # 1. A lógica do tempo(agora isolada aqui)
        agora = datetime.now(timezone.utc)

        # Regra 1: Futuro (Erro)

        if transacao.data_hora > agora:
            # Note: Usamos o ValueError (Erro generico no Python), Não HTTPExpeption
            raise ValueError("Transação no futuro não é permitida.")
        
        diferenca = (agora - transacao.data_hora).total_seconds()

        if diferenca > 60:
            return False  # Ignorar transações com mais de 60 segundos
        
        #Regra 3: Sucesso
        repo = TransacoesRepository()
        repo.salvar(transacao)

        return True # Indica que foi criada