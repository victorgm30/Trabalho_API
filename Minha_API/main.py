# Rota de uma FastAPI
# Frameworks: FastAPI e Uvicorn (servidor)

## Criando ambiente virtual:
# python --version
# python -m venv venv

## Estrutura das pastas:
# - main.py — ponto de entrada da API. -> pip install fastapi uvicorn sqlalchemy
# or pip install fastapi uvicorn sqlalchemy pydantic python-multipart
# - models.py — modelos ORM (SQLAlchemy).
# - schemas.py — modelos Pydantic (validação/IO).
# - database.py — sessão e engine do banco.
# - crud.py — operações CRUD desacopladas, o que eu quero que o BD faça.
# - requirements.txt — dependências.  -> instalar: pip install -r /requirements.txt



# main.py
# Para obter as saídas digite no terminal: uvicorn main:app --reload or uvicorn Corrida.main:app --reload
# Ponto de entrada da API: rotas REST para o recurso "alunos"

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
from models import aluno
from schemas import alunoCreate, alunoOut, alunoUpdate
import crud

# Inicializa tabelas no banco (create_all só cria se não existir)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Alunos",
    description="API REST para gerenciamento de alunos com FastAPI + SQLAlchemy.",
    version="1.0.0",
)

@app.get("/")
def welcome():
    return{"mensagem": "Bem-vindo(a) à minha API"}

@app.get("/health", summary="Verifica saúde da API")
def healthcheck():
    """
    Healthcheck simples para ver se a API está de pé.
    """
    return {"status": "ok"}

@app.get(
    "/alunos",
    response_model=List[alunoOut],
    summary="Listar alunos",
    tags=["alunos"]
)
def listar_alunos(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(50, ge=1, le=200, description="Máximo de registros a retornar"),
    cidade: str | None = Query(None, description="Filtro por cidade (parcial)"),
    db: Session = Depends(get_db)
):
    """
    Retorna lista paginada de alunos. Filtro opcional por cidade.
    """
    results = crud.list_alunos(db, skip=skip, limit=limit, cidade=cidade)
    return results

@app.get(
    "/alunos/{aluno_id}",
    response_model=alunoOut,
    summary="Obter aluno por ID",
    tags=["alunos"]
)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Retorna uma aluno pelo ID. 404 se não existir.
    """
    aluno = crud.get_aluno(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.post(
    "/alunos",
    response_model=alunoOut,
    status_code=201,
    summary="Criar nova aluno",
    tags=["alunos"]
)
def criar_aluno(payload: alunoCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova aluno. Retorna o recurso criado.
    """
    aluno = crud.create_aluno(db, payload)
    return aluno

@app.put(
    "/alunos/{aluno_id}",
    response_model=alunoOut,
    summary="Atualizar aluno por ID",
    tags=["alunos"]
)
def atualizar_aluno(aluno_id: int, payload: alunoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma aluno existente (campos fornecidos). 404 se não existir.
    """
    aluno = crud.get_aluno(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno = crud.update_aluno(db, aluno, payload)
    return aluno

@app.delete(
    "/alunos/{aluno_id}",
    status_code=204,
    summary="Excluir aluno por ID",
    tags=["alunos"]
)
def excluir_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Exclui uma aluno. 404 se não existir.
    """
    aluno = crud.get_aluno(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    crud.delete_aluno(db, aluno)
    # 204 No Content: sem corpo de resposta
    return