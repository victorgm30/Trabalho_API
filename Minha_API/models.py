# models.py
# Modelos de dados do domínio "alunos" usando SQLAlchemy ORM

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from database import Base

class aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    cpf = Column(String(20), nullable=False, index=True)
    disciplina = Column(String(100), nullable=False, index=True)
    turma = Column(String(100), nullable=False, index=True)
    universidade = Column(String(100), nullable=False, index=True)
    cidade = Column(String(100), nullable=False, index=True)
    professora = Column(String(150), nullable=False)