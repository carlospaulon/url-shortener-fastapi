import validators
import secrets

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Crio o BD com as tabelas já modeladas

def get_db(): # Cada request cria uma sessão com o BD (é seguro?)
    db = SessionLocal() # Crio uma sessão do BD
    try: 
        yield db # Retorna a conexão
    finally:
        db.close() # Fecha a conexão

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

#Endpoints
@app.get('/')
def read_root():
    return 'Welcome to the URL Shortener APP :)'


# URL Post
@app.post('/url', response_model=schemas.URLInfo) # Passamos como DTO do Post - URLInfo (herda tudo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)): # Função POST - Precisa de uma URL com base no Schema e DEPENDE de uma sessão com o BD para realizar a request
    if not validators.url(url.target_url): # Valida a URL baseada na URL do Schema (A URL com parâmetro)
        raise_bad_request(message='URL not valid')
    
    # TODO: Lógica - Mudar lógica do short depois
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''.join(secrets.choice(chars) for _ in range(5))
    secret_key = ''.join(secrets.choice(chars) for _ in range(8))

    # Cria uma entrada do BD - 42 a 49
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    
    
    return db_url

# KEY_URL Get

# Admin KEY_URL Get

# Admin KEY_URL Delete

