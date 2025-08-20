from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/sellers", tags=["sellers"])

@router.post("", response_model=schemas.SellerOut)
def create_seller(payload: schemas.SellerCreate, db: Session = Depends(get_db)):
    s = models.Seller(**payload.dict())
    db.add(s); db.commit(); db.refresh(s); return s
