# schemas.py 
# Modelos Pydantic para entrada/saída da API (validação de dados/regras e serialização)

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class alunoBase(BaseModel):
    """
    Base de dados para criar/atualizar alunos.
    """
    nome: str = Field(min_length=3, max_length=150)
    cpf: str = Field(min_length=2, max_length=20)
    disciplina: str = Field(min_length=2, max_length=100)
    turma: str = Field(min_length=2, max_length=100)
    universidade: str = Field(min_length=2, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    professora: str = Field(default=None, min_length=2, max_length=150)

class alunoCreate(alunoBase):
    """
    Payload para criação de aluno.
    """
    pass

class alunoUpdate(BaseModel):
    """
    Payload para atualização parcial/total de aluno.
    Todos os campos são opcionais para permitir atualizações parciais (PUT completo ou PATCH style).
    """
    nome: str | None = Field(default=None, min_length=3, max_length=150)
    cpf: str | None = Field(default=None, min_length=2, max_length=20)
    disciplina: str | None = Field(default=None, min_length=2, max_length=100)
    turma: str | None = Field(default=None, min_length=2, max_length=100)
    universidade: str | None = Field(default=None, min_length=2, max_length=100)
    cidade: str | None = Field(default=None, min_length=2, max_length=100)
    professora: str | None = Field(default=None, min_length=2, max_length=150)

class alunoOut(BaseModel):
    """
    Resposta enviada ao cliente.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: str
    disciplina: str
    turma: str
    universidade: str
    cidade: str
    professora: str