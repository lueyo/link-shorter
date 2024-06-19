import datetime
from pydantic import BaseModel
from typing import Optional, List

class Link (BaseModel):
    id: Optional[str] = None
    url: str
    short_code: str

class LinkCreate(BaseModel):
    url: str
    


    
