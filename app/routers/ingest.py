u200B
 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.db import get_db
from app.deps.auth import admin_required, get_current_active_user
from app.ingest.openaq import fetch_openaq, OpenAQAuthError
from app.ingest.openmeteo import fetch_openmeteo
from app.models import Source, Zone, Indicator
from app.core.config import settings

router = APIRouter(prefix="/ingest", tags=["ingestion"], dependencies=[Depends(admin_required)])


def ensure_source(db: Session, name: str, kind: str, url: str) -> Source:
    src = db.query(Source).filter(Source.name == name).first()
    if src:
        return src
    src = Source(name=name, kind=kind, url=url)
    db.add(src)
    db.commit()
    db.refresh(src)
    return src


@router.post("/openaq")
def ingest_openaq(zone_id: int, radius: int = 10000, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    if zone.latitude is None or zone.longitude is None:
        raise HTTPException(status_code=400, detail="La zone doit avoir une latitude/longitude pour interroger OpenAQ")
    source = ensure_source(db, "OpenAQ", "openaq", "https://api.openaq.org")
    try:
        data = fetch_openaq(lat=zone.latitude, lon=zone.longitude, api_key=settings.openaq_api_key, radius_m=radius)
    except OpenAQAuthError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'appel OpenAQ : {exc}")
    inserted = 0
    for item in data:
        indicator = Indicator(
            source_id=source.id,
            type=item.get("type"),
            value=item.get("value"),
            unit=item.get("unit") or "",
            timestamp=item.get("timestamp"),
            zone_id=zone.id,
            extra=item.get("extra"),
            created_by_id=current_user.id,
        )
        db.add(indicator)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            continue
        inserted += 1
    return {"inserted": inserted, "total": len(data)}


@router.post("/openmeteo")
def ingest_openmeteo(lat: float, lon: float, zone_id: int, days: int = 3, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    source = ensure_source(db, "Open-Meteo", "openmeteo", "https://api.open-meteo.com")
    data = fetch_openmeteo(lat=lat, lon=lon, days=days)
    inserted = 0
    for item in data:
        indicator = Indicator(
            source_id=source.id,
            type=item.get("type"),
            value=item.get("value"),
            unit=item.get("unit"),
            timestamp=item.get("timestamp"),
            zone_id=zone.id,
            extra=item.get("extra"),
            created_by_id=current_user.id,
        )
        db.add(indicator)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            continue
        inserted += 1
    return {"inserted": inserted, "total": len(data)}


