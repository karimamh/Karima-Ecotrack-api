u200B
u200B
 
from typing import Optional
from pydantic import BaseModel


class ZoneBase(BaseModel):
    name: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ZoneOut(ZoneBase):
    id: int

    model_config = {"from_attributes": True}



