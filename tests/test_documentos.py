# tests/test_documentos.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_criar_e_buscar_por_palavra_chave():
    payload = {
        "titulo": "Os impactos sociais na Era da informação",
        "autor": "João da Silva",
        "conteudo": "Esse documento fala sobre informação e sociedade.",
        "data": "2025-01-01",
        "latitude": -30.0,
        "longitude": -51.0,
    }

    # Cria documento
    resp_post = client.post("/documentos", json=payload)
    assert resp_post.status_code == 201
    body = resp_post.json()
    assert body["id"] is not None

    # Busca pela palavra "informação", como no exemplo do desafio
    resp_get = client.get("/documentos", params={"palavraChave": "informação"})
    assert resp_get.status_code == 200
    results = resp_get.json()
    assert len(results) >= 1
    assert any("informação" in d["conteudo"] for d in results)


def test_busca_por_expressao():
    payload = {
        "titulo": "Novo encontro de Antiguidades!",
        "autor": "Maria",
        "conteudo": "Encontro de históricos carros antigos na cidade de Porto Alegre.",
        "data": "2025-01-01",
        "latitude": -30.05,
        "longitude": -51.17,
    }
    client.post("/documentos", json=payload)

    resp_get = client.get(
        "/documentos",
        params={"busca": "carros antigos porto alegre"},
    )

    assert resp_get.status_code == 200
    results = resp_get.json()
    assert len(results) >= 1
