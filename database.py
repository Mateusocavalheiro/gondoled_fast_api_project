import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 1. COLOQUE SUAS CREDENCIAIS DO AZURE AQUI ---
SERVER = 'gondoled003.database.windows.net'
DATABASE = 'free-sql-db-3627168'
USERNAME = 'CloudSAed5e5704'
PASSWORD = 'Gondoled2026@'

# O driver padrão utilizado pelo Azure. 
# Se der erro no Windows localmente, tente mudar para 'ODBC Driver 17 for SQL Server'
DRIVER = 'ODBC Driver 17 for SQL Server'

# --- 2. MONTAGEM DA STRING DE CONEXÃO ---
# Usamos urllib para codificar a senha, evitando erros caso ela tenha caracteres especiais (@, #, !, etc)
params = urllib.parse.quote_plus(
    f"DRIVER={{{DRIVER}}};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
)

# Essa é a URL no formato que o SQLAlchemy entende para o SQL Server
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# --- 3. CRIAÇÃO DA ENGINE ---
# Não precisamos mais do 'check_same_thread' que usávamos no SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para obter a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()