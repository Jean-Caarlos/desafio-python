# Desafio Python – Solução

Este repositório contém a implementação do desafio técnico solicitado pela DBServer, utilizando **Python 3**, **FastAPI**, **SQLAlchemy** e **SQLite** (banco em arquivo, não em memória).

A solução atende **100% dos requisitos obrigatórios** e **ambos os bônus** especificados no desafio:

- ✔ Criar documentos  
- ✔ Buscar documentos por palavra-chave  
- ✔ Armazenar dados em banco não volátil (SQLite em arquivo)  
- ✔ Ordenar documentos por proximidade (bônus 1)  
- ✔ Buscar documentos por expressão/frase inteira (bônus 2)

---

## 🛠 Tecnologias Utilizadas

- Python 3.10  
- FastAPI  
- Uvicorn  
- SQLAlchemy ORM  
- Pydantic / pydantic-settings  
- SQLite (`data.db`)  
- Pytest  

---

## ▶ Como Rodar o Projeto

### 1. Clonar o repositório

git clone <URL-DO-SEU-REPOSITÓRIO>.git
cd desafio-python
2. Criar e ativar ambiente virtual (opcional, recomendado)
python -m venv venv

# Ativar (Windows PowerShell):
.\venv\Scripts\activate
3. Instalar dependências
pip install -r requirements.txt

4. Iniciar o servidor
uvicorn app.main:app --reload
A API estará disponível em:

http://127.0.0.1:8000

Documentação Swagger: http://127.0.0.1:8000/docs

📚 Endpoints da API
A aplicação expõe os seguintes endpoints:

POST /documentos
Cria um novo documento.

🔹 Exemplo de payload:
json
{
  "titulo": "Os impactos sociais na Era da informação",
  "autor": "João da Silva",
  "conteudo": "Esse documento fala sobre informação e sociedade.",
  "data": "2025-01-01",
  "latitude": -29.99,
  "longitude": -51.17
}
🔹 Resposta:
json
{
  "id": 1,
  "titulo": "...",
  "autor": "...",
  "conteudo": "...",
  "data": "2025-01-01",
  "latitude": -29.99,
  "longitude": -51.17
}
GET /documentos
Busca documentos usando:

palavraChave → busca simples

busca → expressão/frase (bônus 2)

latitude + longitude → ordenação geográfica (bônus 1)

❗ Observações:
Não é permitido usar busca e palavraChave ao mesmo tempo.

Se latitude e longitude forem enviados, a API calcula a distância via fórmula de Haversine.

🔹 Exemplos de uso
Buscar por palavra-chave:

GET /documentos?palavraChave=informação
Busca com ordenação por proximidade (bônus 1):

GET /documentos?palavraChave=carro&latitude=-29.99&longitude=-51.17
Buscar por expressão (bônus 2):

GET /documentos?busca=Carros antigos em porto alegre
💡 Decisões de Implementação
O banco SQLite foi escolhido por ser simples, rápido e persistido em arquivo (não em memória).

A fórmula de Haversine foi usada para calcular distâncias geográficas (bônus 1).

Busca por expressão foi implementada quebrando o texto em palavras e aplicando filtro AND entre os termos.

O projeto segue boas práticas de organização:

models.py

schemas.py

crud.py

utils_geo.py

deps.py

main.py

🧪 Testes Automatizados
Os testes foram escritos usando Pytest.

Para rodar os testes:
pytest
Testes incluem:

Criação de documentos via POST

Busca por palavra-chave

Busca por frase

Estrutura básica da API

📦 Estrutura do Projeto
pgsql
Copiar código
desafio-python/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── config.py
│   ├── deps.py
│   ├── utils_geo.py
│   └── __init__.py
│
├── tests/
│   └── test_documentos.py
│
├── data.db
├── requirements.txt
└── README_SOLUCAO.md
✔ Resultado Final
A solução:

Atende todos os requisitos obrigatórios

Implementa os bônus 1 e 2

Utiliza arquitetura limpa e clara

Tem testes automatizados

Está pronta para ser executada e avaliada