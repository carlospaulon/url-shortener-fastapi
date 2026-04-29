import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

from starlette.datastructures import URL
from .config import get_settings

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Crio o BD com as tabelas já modeladas

def get_db(): # Cada request cria uma sessão com o BD (é seguro?)
    db = SessionLocal() # Crio uma sessão do BD
    try: 
        yield db # Retorna a conexão
    finally:
        db.close() # Fecha a conexão

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        'administration info', secret_key=db_url.secret_key
    )

    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f'URL {request.url} not found'
    raise HTTPException(status_code=404, detail=message)

#Endpoints
@app.get('/')
def read_root():
    return 'Welcome to the URL Shortener APP :)'


# URL Post
@app.post('/url', response_model=schemas.URLInfo) # Passamos como DTO do Post - URLInfo (herda tudo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)): # Função POST - Precisa de uma URL com base no Schema e DEPENDE de uma sessão com o BD para realizar a request
    if not validators.url(url.target_url): # Valida a URL baseada na URL do Schema (A URL com parâmetro)
        raise_bad_request(message='URL not valid')


    db_url = crud.create_db_url(db=db, url=url)
    
    return get_admin_info(db_url)


# KEY_URL Get
@app.get('/{url_key}')
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):

    if db_url := crud.get_db_url_key(db=db, url_key=url_key):
        crud.update_db_click(db=db, db_url=db_url) # Quando vou clicar no short link ele atualiza o click e redireciona para target
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


# Admin KEY_URL Get
@app.get('/admin/{secret_key}', name='administration info', response_model=schemas.URLInfo)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    
    #walrus operator realiza a função/condicao e atribui a variável (verificamos basicamente se tem valor ou é None)
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url) # Pego as informações do admin do short link criado
    else:
        raise_not_found(request)
    

# Admin KEY_URL Delete
@app.delete('/admin/{secret_key}')
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_db_url_by_secret_key(db=db, secret_key=secret_key):
        message = f'Successfully deleted shortened URL for "{db_url.target_url}"'
        return {'detail': message}
    else:
        raise_not_found(request)

