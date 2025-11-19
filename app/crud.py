# app/crud.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas


def create_document(db: Session, doc_in: schemas.DocumentCreate) -> models.Document:
    db_doc = models.Document(
        titulo=doc_in.titulo,
        autor=doc_in.autor,
        conteudo=doc_in.conteudo,
        data=doc_in.data,
        latitude=doc_in.latitude,
        longitude=doc_in.longitude,
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def search_documents_by_keyword(db: Session, palavra_chave: str) -> List[models.Document]:
    """Busca por UMA palavra (palavraChave) em título, autor ou conteúdo."""
    like = f"%{palavra_chave}%"
    return (
        db.query(models.Document)
        .filter(
            or_(
                models.Document.titulo.ilike(like),
                models.Document.autor.ilike(like),
                models.Document.conteudo.ilike(like),
            )
        )
        .all()
    )


def search_documents_by_phrase(db: Session, phrase: str) -> List[models.Document]:
    """
    Busca por expressão/frase (busca):
    - quebra a frase por espaços
    - exige que TODAS as palavras apareçam em pelo menos um dos campos
      (AND entre termos).
    """
    terms = [t.strip() for t in phrase.split() if t.strip()]
    if not terms:
        return []

    filters = []
    for term in terms:
        like = f"%{term}%"
        filters.append(
            or_(
                models.Document.titulo.ilike(like),
                models.Document.autor.ilike(like),
                models.Document.conteudo.ilike(like),
            )
        )

    return db.query(models.Document).filter(and_(*filters)).all()
