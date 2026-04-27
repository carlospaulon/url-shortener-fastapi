from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str # Original URL

class URL(URLBase):
    is_active: bool # Short
    clicks: int

    class Config: # Dentro da classe defino como config ORM = True
        orm_mode = True

class URLInfo(URL):
    url: str  # Short hash infos
    admin_url: str