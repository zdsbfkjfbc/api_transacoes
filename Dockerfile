# 1. Base: Começamos com uma imagem Python leve
from python:3.11-slim

# 2. Diretório de Trabalho
WORKDIR /app

# 3. Cache: Instalamos dependências primeiro para aproveitar o cache do Docker!
# Isso economiza tempo em builds futuros quando só o código-fonte muda.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Código: Copiamos o código-fonte da sua API
COPY . .

# 5. Inicialização: Comando para rodar a aplicação
# (Usamos 0.0.0.0 para que o contêiner escute em qualquer interface)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]