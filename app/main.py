 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from app.core.config import settings
from app.core.db import engine, Base
from app.routers import auth, users, zones, sources, indicators, stats, ingest

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

prefix = settings.api_prefix
app.include_router(auth.router, prefix=prefix)
app.include_router(users.router, prefix=prefix)
app.include_router(zones.router, prefix=prefix)
app.include_router(sources.router, prefix=prefix)
app.include_router(indicators.router, prefix=prefix)
app.include_router(stats.router, prefix=prefix)
app.include_router(ingest.router, prefix=prefix)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))


@app.get("/")
def root():
    return {"message": "EcoTrack API"}

