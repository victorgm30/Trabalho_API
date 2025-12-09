# crud.py
# Funções de acesso ao banco para o recurso aluno

from sqlalchemy.orm import Session
from models import aluno
from schemas import alunoCreate, alunoUpdate

def list_alunos(db: Session, skip: int = 0, limit: int = 50, cidade: str | None = None):
    """
    Lista alunos com paginação simples e filtro por cidade opcional.
    """
    query = db.query(aluno)
    if cidade:
        query = query.filter(aluno.cidade.ilike(f"%{cidade}%"))
    return query.offset(skip).limit(limit).all()

def get_aluno(db: Session, aluno_id: int):
    """
    Busca aluno por ID.
    """
    return db.query(aluno).filter(aluno.id == aluno_id).first()

def create_aluno(db: Session, payload: alunoCreate):
    """
    Cria nova aluno a partir do payload validado.
    """
    aluno = aluno(**payload.dict())
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

def update_aluno(db: Session, aluno: aluno, payload: alunoUpdate):
    """
    Atualiza campos fornecidos no payload (atualização parcial/total).
    """
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(aluno, field, value)
    db.commit()
    db.refresh(aluno)
    return aluno

def delete_aluno(db: Session, aluno: aluno):
    """
    Remove aluno do banco.
    """
    db.delete(aluno)
    db.commit()