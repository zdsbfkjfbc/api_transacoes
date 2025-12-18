from datetime import datetime, timezone, timedelta
from src.use_cases.criar_transacao import CriarTransacaoUseCase
from src.schemas import TransacaoIn


class FakeRepositorio:
    def salvar(self, transacao):
        pass

def test_regressao_regra_tempo():   
    # 1. Arrange (Preparar)
    repo_fake = FakeRepositorio()   
    use_case = CriarTransacaoUseCase(repo_fake)

    # Cenário: Transação com 45 segundos de diferença
    # Na regra antiga (60s) -> PASSIVA (true)
    # Nova regra (30s) -> DEVE FALHAR (false)  
    data_passada = datetime.now(timezone.utc) - timedelta(seconds=45)

    # Criamos o objeto Pydantic (porque seu código espera um TransacaoIn, não um dict)
    transacao_input = TransacaoIn(valor=100.0, data_hora=data_passada)  

    # 2. Act (Executar)
    resultado = use_case.executar(transacao_input)

    # 3. Assert (Verificar)
    # AQUI ESTÁ A REGRESSÃO:
    # O teste antigo dizia: "Espero que seja aceito (True)"
    # Mas como mudamos o código para 30s, o resultado real será False.
    # O teste vai QUEBRAR.
    assert resultado == True  
     


