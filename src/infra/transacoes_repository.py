from typing import List
from src.models.schemas import TransacaoIn

class TransacoesRepository:
    

    # 1. Lista Global (Estática)
    # Por ser estática (fora do __init__), ela é compartilhada entre todas as instâncias

    _transacoes: List[TransacaoIn] = []

    def salvar(self, transacao: TransacaoIn) -> None:
        # 2. Salva uma transação na lista em memória
        self._transacoes.append(transacao)
        print(f"[Repository] Transação salva! Total: {len(self._transacoes)}")

    def listar_todas(self) -> List[TransacaoIn]:
        """Retorna todas as transações salvas"""
        return self._transacoes
    
    def limpar_todas(self):
        """(Util para testes) Limpa todas as transações salvas"""
        self._transacoes.clear()
        print("[Repository] Todas as transações foram limpas.")