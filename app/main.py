from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine

from app.routes.auth import router as auth_router
from app.routes.billing import router as billing_router
from app.routes.signals import router as signals_router
from app.routes.webhook import router as webhook_router

app = FastAPI(title="Trading Signals SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(signals_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"message": "Server is running....!"}
