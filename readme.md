├── main.py                  # Ponto de entrada da API (inicia o servidor)
│   ├── database.py              # Configuração da conexão com o banco de dados
│   ├── models.py                # Modelos do banco de dados (SQLAlchemy: as tabelas reais)
│   ├── schemas.py               # Modelos Pydantic (Validação dos dados que entram e saem)
│   ├── routers/                 # Organização das rotas (URLs)
│   │   ├── __init__.py
│   │   ├── rota_esp32.py        # Rotas consumidas pelo hardware (/verificar, /registrar)
│   │   └── rota_streamlit.py    # Rotas consumidas pela interface (/atualizar, ler logs)
│   └── requirements.txt         # Lista de dependências (fastapi, uvicorn, sqlalchemy...)