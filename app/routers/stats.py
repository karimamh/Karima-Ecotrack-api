u200B
 
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.deps.auth import get_current_active_user
from app.models.indicator import Indicator

router = APIRouter(prefix="/stats", tags=["stats"], dependencies=[Depends(get_current_active_user)])


@router.get("/average")
def average(indicator_type: str, zone_id: Optional[int] = None, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None, db: Session = Depends(get_db)):
    if not indicator_type:
        raise HTTPException(status_code=400, detail="Type requis")
    query = db.query(Indicator).filter(Indicator.type == indicator_type)
    if zone_id:
        query = query.filter(Indicator.zone_id == zone_id)
    if from_date:
        query = query.filter(Indicator.timestamp >= from_date)
    if to_date:
        query = query.filter(Indicator.timestamp <= to_date)

    label_expr = func.strftime("%Y-%m-%d", Indicator.timestamp)
    rows = query.with_entities(label_expr.label("label"), func.avg(Indicator.value).label("avg")).group_by("label").order_by("label").all()
    return {"labels": [r.label for r in rows], "series": [{"name": indicator_type, "data": [round(r.avg, 3) if r.avg else None for r in rows]}]}


