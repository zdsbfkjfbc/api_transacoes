from locust import HttpUser, task, between
from random import uniform
from datetime import datetime, timezone

class UsuarioItau(HttpUser):
    # Tempo de espera entre uma requisição e outra (1 a 3 segundos)
    # Se quiser estressar MUITO, diminua para (0.1, 0.5)
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """
        Roda uma vez quando o usuário "nasce".
        Fazemos o login aqui para pegar o Token.
        """
        response = self.client.post("/auth/token", json={
            "cpf": "123456789",     # <--- Use o CPF do seu Admin
            "senha": "admin" # <--- Use a senha do seu Admin
        })
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        else:
            print(f"Erro no login: {response.status_code}")

    @task
    def criar_transacao(self):
        """
        A tarefa que será repetida várias vezes.
        """
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        
        agora = datetime.now().isoformat()
        
        payload = {
            "valor": round(uniform(10.0, 500.0), 2), # Valor aleatório entre 10 e 500
            "data_hora": agora, # Data fixa pra simplificar, ou use datetime.now()
            "estabelecimento": "Loja Exemplo"
        }

        self.client.post("/transacoes", json=payload, headers=headers)