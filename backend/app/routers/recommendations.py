from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import schemas
from ..recommender.engine import RecommenderEngine

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("", response_model=List[schemas.RecommendationOut])
def recommend(user_id: Optional[int] = None, lat: Optional[float] = None, lon: Optional[float] = None, k: int = 20, db: Session = Depends(get_db)):
    engine = RecommenderEngine(db)
    recs = engine.recommend(user_id=user_id, lat=lat, lon=lon, k=k)
    return [schemas.RecommendationOut(product=r[0], score=round(r[1],6), distance_km=(round(r[2],3) if r[2] is not None else None)) for r in recs]
