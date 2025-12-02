from datetime import datetime, timezone
from src.models.schemas import EstatisticaOut
from src.infra.transacoes_repository import TransacoesRepository
    
class CalcularEstatisticasUseCase:
    def execute(self) -> EstatisticaOut:
        # 1. Pega todas as transações do "cofre"
        repo = TransacoesRepository()
        todas_transacoes = repo.listar_todas()

        # 2. Prepara uma lista vazia para guardar só as recentes
        transacoes_recentes = []

        # 3. Define o "agora" (UTC)
        agora = datetime.now(timezone.utc)

        # 4. O LOOP (Passa por cada transação guardada)
        for transacao in todas_transacoes:
            # 4.1 Calcula a diferença de tempo
            diferenca = (agora - transacao.data_hora).total_seconds()

            # Se a diferença for menor ou igual a 60 segundos, é recente
            if diferenca <= 60:
                transacoes_recentes.append(transacao)

        # 5. Calcula as estatísticas
        if len(transacoes_recentes) == 0:
            return EstatisticaOut(
                count=0,
                sum=0.0,
                avg=0.0,
                min=0.0,
                max=0.0
            )
    
        # 6. Agora vem a matematica (Seu Desafio)
        # Como você calcula a soma, média, máximo de 'transacoes_recentes'?
        # Dica: Use list comprehensions ou um loop

        #Exemplo para pegar todos os valores:
        valores = [t.valor for t in transacoes_recentes]

        total_soma = sum(valores)
        quantidade = len(valores)
        media = total_soma / quantidade
        minimo = min(valores)
        maximo = max(valores)

        return EstatisticaOut(
            count=quantidade,
            sum=total_soma,
            avg=media,
            min=minimo,
            max=maximo
        )