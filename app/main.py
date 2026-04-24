from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, users
from app.core.database import engine, Base
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.on_event("startup")
def startup():
    # ⚠️ safe place to create tables
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}