from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", status_code=201)
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if db.get(models.Product, payload.product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    fb = models.Feedback(user_id=payload.user_id, product_id=payload.product_id, rating=payload.rating, comment=payload.comment)
    db.add(fb); db.commit(); return {"ok": True}
