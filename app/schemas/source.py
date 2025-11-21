 
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    kind: str
    url: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    kind: Optional[str] = None
    url: Optional[str] = None
    last_sync: Optional[datetime] = None


class SourceOut(SourceBase):
    id: int
    last_sync: Optional[datetime] = None

    model_config = {"from_attributes": True}

