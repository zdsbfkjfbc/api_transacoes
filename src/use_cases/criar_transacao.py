from datetime import datetime, timezone
from src.schemas import TransacaoIn

class CriarTransacaoUseCase:
    
    # 1. O CONSTRUTOR MÁGICO
    # Aqui dizemos: "Eu não sei criar repositório, alguém me entregue um pronto!"
    def __init__(self, repositorio):
        self.repositorio = repositorio

    # 2. Mudamos o nome de 'execute' para 'executar' (para bater com o controller)
    def executar(self, transacao: TransacaoIn) -> bool:
        """
        Executa as regras de negócio para criar uma nova transação.
        """
        
        # --- LÓGICA DE TEMPO (Mantivemos a sua, que está ótima) ---
        agora = datetime.now(timezone.utc)

        if transacao.data_hora > agora:
            raise ValueError("Transação no futuro não é permitida.")
        
        diferenca = (agora - transacao.data_hora).total_seconds()

        if diferenca > 60:
            return False  # Ignorar transações antigas (204)
        
        # --- A MUDANÇA ESTÁ AQUI EMBAIXO ---
        
        # Em vez de criar 'repo = TransacoesRepository()'...
        # Usamos o repositório que recebemos lá no __init__ (seja ele qual for)
        self.repositorio.salvar(transacao)

        return True