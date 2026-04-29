import secrets
import string

from sqlalchemy.orm import Session
from . import crud

def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits # Cria uma variável com todos os caracteres UPPER + Os digitos
    return ''.join(secrets.choice(chars) for _ in range(length)) # Vai escolhar os caracteres aleatoriamente com base no range definido (padrão=5))

def create_unique_random_key(db: Session) -> str:
    key = create_random_key() # Gera uma key
    while crud.get_db_url_key(db, key): # Se dentro do banco ele encontrar algo com essa key gerada, vamos criar uma nova, senão mantenho a recem gerada
        key = create_random_key()
    return key