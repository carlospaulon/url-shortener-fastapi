from sqlalchemy.orm import Session

from . import keygen, models, schemas

def get_db_url_key(db: Session, url_key: str) -> models.URL:
    # Se a chave passada for encontrada no BD retorna a mesma, senão retorna None
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    # Se a chave-secreta passada for encontrada no BD retorna a mesma, senão retorna None
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_random_key(db) # A key será unica
    secret_key = f'{key}_{keygen.create_random_key(length=8)}' # Junto a key unica com uma secret random (se a secret for igual a outra, a key será única ainda assim) 

    # Cria uma entrada do BD - com target, key e secret (clicks e is_active são default)
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url

def update_db_click(db: Session, db_url: schemas.URL) -> models.URL:

    db_url.clicks += 1 # Atualiza os clicks
    db.commit() # Salva
    db.refresh(db_url) # Atualiza no BD
    return db_url

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    db_url = get_db_url_by_secret_key(db, secret_key) # Pego o banco pelo secret

    if db_url: # Se houver algo no banco (tem ou None)
        db_url.is_active = False # Desativo o link
        db.commit() # Salva
        db.refresh(db_url) # Atualiza
    return db_url