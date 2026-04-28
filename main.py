from fastapi import FastAPI
from . import models, database
from .routers import esp32

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Etiquetas Inteligentes")

# Inclui as rotas
app.include_router(esp32.router)

@app.get("/")
def read_root():
    return {"status": "API Online"}