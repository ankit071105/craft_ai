from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routers import users, sellers, products, interactions, recommendations, feedback
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hyper-Local E-Commerce")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(sellers.router)
app.include_router(products.router)
app.include_router(interactions.router)
app.include_router(recommendations.router)
app.include_router(feedback.router)

@app.get("/", tags=["root"])
def root():
    return {"status":"ok","message":"Backend is running."}
