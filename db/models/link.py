import datetime
from pydantic import BaseModel
from typing import Optional

class Link(BaseModel):
    id: Optional[str] = None
    url: str
    short_code: str
    password: Optional[str] = None

class LinkCreate(BaseModel):
    url: str
    password: Optional[str] = None
    


    
