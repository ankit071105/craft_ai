from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..recommender.utils import haversine_km

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    p = models.Product(**payload.dict())
    db.add(p); db.commit(); db.refresh(p); return p

@router.get("", response_model=List[schemas.ProductOut])
def list_products(skip:int=0, limit:int=100, db: Session = Depends(get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@router.get("/nearby", response_model=List[schemas.ProductOut])
def nearby_products(lat: float, lon: float, radius_km: float = 50.0, db: Session = Depends(get_db)):
    prods = db.query(models.Product).all()
    out = []
    for p in prods:
        if p.lat is None or p.lon is None: continue
        d = haversine_km(lat, lon, p.lat, p.lon)
        if d <= radius_km: out.append(p)
    return out

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id:int, db: Session = Depends(get_db)):
    p = db.get(models.Product, product_id)
    if not p: raise HTTPException(status_code=404, detail="Product not found")
    return p
