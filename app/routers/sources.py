u200B
u200B
 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.deps.auth import get_current_active_user, admin_required
from app.schemas.source import SourceOut, SourceCreate, SourceUpdate
from app.models.source import Source

router = APIRouter(prefix="/sources", tags=["sources"], dependencies=[Depends(get_current_active_user)])


@router.get("/", response_model=list[SourceOut])
def list_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Source).offset(skip).limit(min(limit, 200)).all()


@router.post("/", response_model=SourceOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    if db.query(Source).filter(Source.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Source déjà existante")
    source = Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.patch("/{source_id}", response_model=SourceOut, dependencies=[Depends(admin_required)])
def update_source(source_id: int, payload: SourceUpdate, db: Session = Depends(get_db)):
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source introuvable")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(source, k, v)
    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_source(source_id: int, db: Session = Depends(get_db)):
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source introuvable")
    db.delete(source)
    db.commit()
    return None



