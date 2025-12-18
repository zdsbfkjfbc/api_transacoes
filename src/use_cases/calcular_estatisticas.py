from datetime import datetime, timedelta, timezone

class CalcularEstatisticasUseCase:
    # 1. Injeção de Dependência: Recebe o Repositório via Construtor
    def __init__(self, repositorio):
        self.repositorio = repositorio
    
    def executar(self):
        """
        Define a janela de tempo (últimos 60 segundos) e 
        pede ao repositório para calcular as estatísticas.

        """
        # Regra de Negócio: Janela de 60 segundos
        agora = datetime.now(timezone.utc)
        sessenta_segundos_atras = agora - timedelta(seconds=30)

        #Delega o calculo pesado para o Banco de Dados (via Repositório)
        estatisticas = self.repositorio.calcular_estatisticas(sessenta_segundos_atras)

        return estatisticas
