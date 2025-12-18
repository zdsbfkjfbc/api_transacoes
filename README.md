👣 Passo 1: Crie o ArquivoNa raiz do seu projeto (onde está o docker-compose.yml), crie um arquivo chamado README.md.👣 Passo 2: O Conteúdo (Copie e Cole)Este template abaixo não é um README básico. Ele contém uma seção de "Decisões Arquiteturais", que é o que diferencia um Pleno de um Júnior.Copie tudo abaixo e cole no arquivo:Markdown# 🏦 API de Transações Financeiras (High Performance)

## 📋 Sobre o Projeto
API REST desenvolvida para processar transações financeiras e calcular estatísticas em tempo real.
O projeto foi construído com foco em **Clean Architecture**, **Testes Automatizados** e **Performance**, garantindo que a complexidade de tempo para leitura de estatísticas seja constante O(1) na aplicação, delegando agregação para o Banco de Dados.

---

## 🚀 Tecnologias
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI (Async)
* **Banco de Dados:** PostgreSQL 15
* **ORM:** SQLAlchemy (com Session Management via Dependency Injection)
* **Testes:** Pytest (Unitários e Integração)
* **Infraestrutura:** Docker & Docker Compose

---

## ⚙️ Arquitetura e Decisões de Design

### 1. Clean Architecture (Desacoplamento)
O projeto segue estritamente a separação de responsabilidades:
* **Router (Controller):** Apenas recebe HTTP e valida esquemas (Pydantic).
* **Use Case (Service):** Contém a regra de negócio (ex: validação da janela de 60 segundos).
* **Repository (Infra):** Abstrai o acesso ao banco de dados.

### 2. Performance de Estatísticas (SQL Aggregation)
Em vez de carregar milhares de transações para a memória da aplicação para somar, utilizamos funções de agregação nativas do banco (`SUM`, `AVG`, `COUNT`). 
Isso reduz o tráfego de rede e o uso de RAM da aplicação, permitindo escalabilidade vertical.

### 3. Proteção contra Regressão
Foi implementada uma suíte de testes automatizados que garante que alterações futuras nas regras de negócio (ex: mudar janela de 60s para 30s) quebrem o build localmente antes de chegar em produção.

---

## 🛠️ Como Rodar Localmente

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU-USUARIO/api-transacoes.git](https://github.com/SEU-USUARIO/api-transacoes.git)
Suba o ambiente:Bashdocker compose up -d --build
Acesse a Documentação Interativa (Swagger):Abra no navegador: http://localhost:8000/docs🧪 Rodando os TestesPara executar os testes unitários e de integração:Bash# Instale as dependências de dev (se estiver rodando fora do Docker)
pip install -r requirements.txt

# Execute
python -m pytest -v
📝 Endpoints PrincipaisMétodoRotaDescriçãoPOST/transacaoRecebe JSON com valor e data_hora. Retorna 201 se criado ou 422 se for mais antigo que 60s.GET/estatisticaRetorna JSON com sum, avg, min, max, count dos últimos 60 segundos.