from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.deps.auth import get_current_active_user, admin_required
from app.schemas.zone import ZoneOut, ZoneCreate, ZoneUpdate
from app.models.zone import Zone

router = APIRouter(prefix="/zones", tags=["zones"], dependencies=[Depends(get_current_active_user)])


@router.get("/", response_model=list[ZoneOut])
def list_zones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Zone).offset(skip).limit(min(limit, 200)).all()


@router.post("/", response_model=ZoneOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db)):
    zone = Zone(**payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.patch("/{zone_id}", response_model=ZoneOut, dependencies=[Depends(admin_required)])
def update_zone(zone_id: int, payload: ZoneUpdate, db: Session = Depends(get_db)):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(zone, k, v)
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    db.delete(zone)
    db.commit()
    return None
