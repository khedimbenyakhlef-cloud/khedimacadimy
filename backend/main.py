from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import orientation, filieres, users, admin

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orientation.router, prefix="/api/v1")
app.include_router(filieres.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}


from db.session import engine
from models import filiere, user, recommandation
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import AsyncSessionLocal

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        from models.filiere import Base as FiliereBase
        from models.user import Base as UserBase
        from models.recommandation import Base as RecoBase
        await conn.run_sync(FiliereBase.metadata.create_all)
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(RecoBase.metadata.create_all)
