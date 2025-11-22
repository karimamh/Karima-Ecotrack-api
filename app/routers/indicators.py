u200B
 
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.db import get_db
from app.deps.auth import get_current_active_user, admin_required
from app.schemas.indicator import IndicatorOut, IndicatorCreate, IndicatorUpdate, PaginatedIndicators
from app.models.indicator import Indicator

router = APIRouter(prefix="/indicators", tags=["indicators"], dependencies=[Depends(get_current_active_user)])


@router.get("/", response_model=PaginatedIndicators)
def list_indicators(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    zone_id: Optional[int] = None,
    indicator_type: Optional[str] = None,
    source_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Indicator)
    if from_date:
        query = query.filter(Indicator.timestamp >= from_date)
    if to_date:
        query = query.filter(Indicator.timestamp <= to_date)
    if zone_id:
        query = query.filter(Indicator.zone_id == zone_id)
    if indicator_type:
        query = query.filter(Indicator.type == indicator_type)
    if source_id:
        query = query.filter(Indicator.source_id == source_id)
    total = query.count()
    items = query.order_by(Indicator.timestamp.desc()).offset(skip).limit(min(limit, 200)).all()
    return {"total": total, "items": items}


@router.post("/", response_model=IndicatorOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_indicator(payload: IndicatorCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    indicator = Indicator(**payload.model_dump(), created_by_id=current_user.id)
    db.add(indicator)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Doublon détecté")
    db.refresh(indicator)
    return indicator


@router.patch("/{indicator_id}", response_model=IndicatorOut, dependencies=[Depends(admin_required)])
def update_indicator(indicator_id: int, payload: IndicatorUpdate, db: Session = Depends(get_db)):
    indicator = db.get(Indicator, indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicateur introuvable")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(indicator, k, v)
    db.commit()
    db.refresh(indicator)
    return indicator


@router.delete("/{indicator_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_indicator(indicator_id: int, db: Session = Depends(get_db)):
    indicator = db.get(Indicator, indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicateur introuvable")
    db.delete(indicator)
    db.commit()
    return None


