from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . config import get_settings

# Crio o motor para conexão com o BD
engine = create_engine(
    # Defino como argumentos (URL do Banco - vinda de Config) E (Argumento de conexão como - check_same_thread - Indica que aceita mais de uma request ao mesmo tempo)
    get_settings().db_url, connect_args={'check_same_thread': False}
)

# Gera objetos de sessão (serve para se comunicar com o BD)
SessionLocal = sessionmaker(
    # autocommit=False - Não salva alterações automaticamente
    # autoflush=False - Não envia automaticamente mudanças pendentes para o banco antes de executar queries
    # bind=engine - Liga a sessão a conexão com o BD
    autocommit=False, autoflush=False, bind=engine
)

# Cria base das tabelas herdadas de Models.py
Base = declarative_base()
