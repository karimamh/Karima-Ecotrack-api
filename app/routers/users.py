u200B
 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.deps.auth import get_current_active_user, admin_required
from app.schemas.user import UserOut, UserUpdate
from app.core.security import hash_password
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_active_user)])


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/", response_model=list[UserOut], dependencies=[Depends(admin_required)])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(min(limit, 200)).all()


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
def edit_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    data = payload.model_dump(exclude_unset=True)
    if data.get("password"):
        user.hashed_password = hash_password(data.pop("password"))
    for k, v in data.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return None


