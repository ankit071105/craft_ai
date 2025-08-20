from pydantic import BaseModel, Field
from typing import Optional, List

class UserCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)

class UserOut(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    is_guest: int
    class Config:
        from_attributes = True

class SellerCreate(BaseModel):
    name: str
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class SellerOut(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: Optional[str] = None
    tags: Optional[str] = None
    seller_id: Optional[int] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    image_url: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: Optional[str] = None
    tags: Optional[str] = None
    seller_id: Optional[int] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    image_url: Optional[str] = None
    class Config:
        from_attributes = True

class InteractionCreate(BaseModel):
    user_id: int
    product_id: int
    kind: str

class FeedbackCreate(BaseModel):
    user_id: Optional[int] = None
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class RecommendationOut(BaseModel):
    product: ProductOut
    score: float
    distance_km: float | None = None
