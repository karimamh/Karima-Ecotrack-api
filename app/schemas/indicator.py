u200B
u200B
 
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class IndicatorBase(BaseModel):
    source_id: int
    type: str
    value: float
    unit: str
    timestamp: datetime
    zone_id: int
    extra: Optional[Dict[str, Any]] = None


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    extra: Optional[Dict[str, Any]] = None


class IndicatorOut(IndicatorBase):
    id: int
    created_by_id: Optional[int] = None

    model_config = {"from_attributes": True}


class PaginatedIndicators(BaseModel):
    total: int = Field(..., description="Nombre total")
    items: list[IndicatorOut]



