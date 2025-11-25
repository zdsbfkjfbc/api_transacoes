from fastapi import FastAPI
from src.controllers import transacao_controller

app = FastAPI(title="API de Transações")

# Aqui nos "plugamos" o roteador de transações

app.include_router(transacao_controller.router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 