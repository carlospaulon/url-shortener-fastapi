import validators
from fastapi import FastAPI, HTTPException

from . import schemas

app = FastAPI()

@app.get('/')
def read_root():
    return 'Welcome to the URL Shortener APP :)'

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

# URL Post
@app.post('/url')
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url): # Valida a URL baseada na URL do Schema (A URL com parâmetro)
        raise_bad_request(message='URL not valid')
    return f'TODO: Create database entry for: {url.target_url}'

# KEY_URL Get

# Admin KEY_URL Get

# Admin KEY_URL Delete

