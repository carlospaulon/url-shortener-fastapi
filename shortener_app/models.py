from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

# URL Model é uma subclasse (filha) de Base
class URL(Base):
    __tablename__ = 'urls' # Nome da tabela

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True) # Shorten secret
    secret_key = Column(String, unique=True, index=True) # Admin Shorten Secret (manipular a Short URL)
    target_url = Column(String, index=True) # URL que queremos encurtar (não pode ser unica, senão outros users não conseguem criar no mesmo endereço)
    is_active = Column(Boolean, default=True) # Servirá quando o user quiser deletar a URL, mas vamos primeiro deixar como ativado=False, para dar uma chance do user realizar um undo
    clicks = Column(Integer, default=0) # quantidade de clicks