from fastapi import FastAPI
from src.controllers import transacao_controller
from src.controllers import estatistica_controller

app = FastAPI(title="API de Transações")

# Aqui nos "plugamos" o roteador de transações

app.include_router(transacao_controller.router)

# Aqui nos "plugamos" o roteador de estatísticas
app.include_router(estatistica_controller.router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 