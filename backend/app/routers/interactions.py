from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/interactions", tags=["interactions"])

@router.post("", status_code=201)
def log_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    user = db.get(models.User, payload.user_id)
    prod = db.get(models.Product, payload.product_id)
    if not user or not prod:
        raise HTTPException(status_code=404, detail="User or Product not found")
    it = models.Interaction(user_id=payload.user_id, product_id=payload.product_id, kind=payload.kind)
    db.add(it); db.commit(); return {"ok": True}
