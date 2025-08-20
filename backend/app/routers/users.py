from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if payload.email:
        existing = db.query(models.User).filter(models.User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    u = models.User(
        name=payload.name, email=payload.email, city=payload.city,
        lat=payload.lat, lon=payload.lon, is_guest=0 if payload.email else 1
    )
    db.add(u); db.commit(); db.refresh(u); return u

@router.post("/guest", response_model=schemas.UserOut)
def create_guest(lat: float | None = None, lon: float | None = None, city: str | None = None, db: Session = Depends(get_db)):
    u = models.User(name=None, email=None, city=city, lat=lat, lon=lon, is_guest=1)
    db.add(u); db.commit(); db.refresh(u); return u

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    u = db.get(models.User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u
