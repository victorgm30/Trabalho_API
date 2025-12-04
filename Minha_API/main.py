# Rota de uma FastAPI
# Frameworks: FastAPI e Uvicorn (servidor)

from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Bem-vindo à disciplina de Arquitetura e Desenvolvimento de APIs",
              version="1.0.0",
              description="Victor Gabriel Moreira - RU: 4655363"
)

@app.get("/")
def welcome():
    return{"mensagem": "Bem-vindo(a) à minha API"}