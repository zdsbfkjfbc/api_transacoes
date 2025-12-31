from datetime import datetime, timezone
from src.schemas import TransacaoIn
from src.infra.models import TransacaoDB
from src.infra.transacoes_repository import TransacoesRepository

class CriarTransacaoUseCase:
    
    # 1. O CONSTRUTOR MÁGICO
    # Aqui dizemos: "Eu não sei criar repositório, alguém me entregue um pronto!"
    def __init__(self, repositorio: TransacoesRepository):
        self.repositorio = repositorio

    # 2. Mudamos o nome de 'execute' para 'executar' (para bater com o controller)
    def executar(self, transacao: TransacaoIn) -> bool:
        """
        Executa as regras de negócio para criar uma nova transação.
        """
        
        # --- LÓGICA DE TEMPO (Mantivemos a sua, que está ótima) ---
        agora = datetime.now(timezone.utc)

        if transacao.data_hora.tzinfo is None:
            data_transacao = transacao.data_hora.replace(tzinfo=timezone.utc)
        else:
            data_transacao = transacao.data_hora
        
        diferenca = agora - data_transacao

        if diferenca.total_seconds() > 60:
            return False  # Ignorar transações antigas (204)
        
        # Conversão (Adaptação)
        # O repositorio do Banco espera um objeto TransacaoDB(tabela),
        # mas nós temos um TransacaoIn (schema). Vamos converter:
        nova_transacao_banco = TransacaoDB(
            valor=transacao.valor,
            data_hora=transacao.data_hora,
            estabelecimento=transacao.estabelecimento
        )

        # Persistencia
        # Agora chamamos o metodo .criar() do repositorio de banco
        self.repositorio.criar(nova_transacao_banco)

        return True  # Tudo OK (201)