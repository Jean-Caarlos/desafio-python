# app/main.py
from typing import List, Optional

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import Base, engine
from .deps import get_db
from .utils_geo import haversine_distance_km


# Cria as tabelas no banco na primeira execução
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Desafio Técnico DBServer - Documentos",
    version="1.0.0",
    description="Microsserviço para criação e busca de documentos por palavra-chave ou expressão.",
)


@app.post("/documentos", response_model=schemas.DocumentOut, status_code=201)
def criar_documento(
    documento: schemas.DocumentCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um novo documento e salva no banco de dados.
    """
    return crud.create_document(db, documento)


@app.get("/documentos", response_model=List[schemas.DocumentOut])
def buscar_documentos(
    palavraChave: Optional[str] = Query(
        None,
        description="Palavra-chave para busca simples (uma palavra).",
    ),
    busca: Optional[str] = Query(
        None,
        description="Frase/expressão para busca avançada (bônus 2).",
    ),
    latitude: Optional[float] = Query(
        None,
        description="Latitude para ordenar resultados por proximidade (bônus 1).",
    ),
    longitude: Optional[float] = Query(
        None,
        description="Longitude para ordenar resultados por proximidade (bônus 1).",
    ),
    db: Session = Depends(get_db),
):
    """
    Busca documentos de duas formas:
    - Se 'busca' for informado: busca por expressão/frase (bônus 2).
    - Senão, usa 'palavraChave' (obrigatório nesse caso).

    Se latitude e longitude forem informados, os resultados são ordenados
    do documento mais próximo para o mais distante (bônus 1).
    """

    # Validação de parâmetros
    if not palavraChave and not busca:
        raise HTTPException(
            status_code=400,
            detail="Informe 'palavraChave' ou 'busca' para realizar a pesquisa.",
        )

    if palavraChave and busca:
        raise HTTPException(
            status_code=400,
            detail="Use apenas um dos parâmetros: 'palavraChave' OU 'busca'.",
        )

    # Escolhe o tipo de busca
    if busca:
        documentos = crud.search_documents_by_phrase(db, busca)
    else:
        documentos = crud.search_documents_by_keyword(db, palavraChave)  # type: ignore[arg-type]

    # Se não quiser ordenar por localização, retorna direto
    if latitude is None or longitude is None:
        return documentos

    # Ordenação por proximidade geográfica (bônus 1)
    docs_com_dist = []
    for doc in documentos:
        distancia = haversine_distance_km(
            latitude,
            longitude,
            doc.latitude,
            doc.longitude,
        )
        docs_com_dist.append((distancia, doc))

    docs_ordenados = [doc for _, doc in sorted(docs_com_dist, key=lambda x: x[0])]
    return docs_ordenados
