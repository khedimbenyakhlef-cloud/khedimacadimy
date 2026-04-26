from fastapi import APIRouter
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings
from models.recommandation import Wilaya
from models.filiere import Filiere

router = APIRouter(prefix="/admin", tags=["admin"])

WILAYAS = [
    (1,"Adrar","01","Sud"),(2,"Chlef","02","Centre-Ouest"),(3,"Laghouat","03","Sud"),
    (4,"Oum El Bouaghi","04","Est"),(5,"Batna","05","Est"),(6,"Béjaïa","06","Kabylie"),
    (7,"Biskra","07","Sud-Est"),(8,"Béchar","08","Sud-Ouest"),(9,"Blida","09","Centre"),
    (10,"Bouira","10","Centre"),(16,"Alger","16","Centre"),(19,"Sétif","19","Est"),
    (23,"Annaba","23","Nord-Est"),(25,"Constantine","25","Est"),(31,"Oran","31","Ouest"),
]

FILIERES = [
    {"nom":"Médecine générale","domaine":"Santé","duree_annees":7,"moyenne_min":16.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Médecin généraliste","taux_emploi":95},
    {"nom":"Pharmacie","domaine":"Santé","duree_annees":5,"moyenne_min":15.5,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Pharmacien","taux_emploi":90},
    {"nom":"Génie informatique","domaine":"Informatique","duree_annees":5,"moyenne_min":14.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Développeur, IA","taux_emploi":88},
    {"nom":"Génie électronique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électronicien","taux_emploi":82},
    {"nom":"Architecture","domaine":"Architecture","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["sciences","technique"],"interets_associes":["art","tech"],"debouches":"Architecte","taux_emploi":75},
    {"nom":"Droit","domaine":"Droit","duree_annees":4,"moyenne_min":12.0,"series_compatibles":["lettres","gestion"],"interets_associes":["droit","social"],"debouches":"Avocat, magistrat","taux_emploi":70},
    {"nom":"Sciences économiques","domaine":"Économie","duree_annees":5,"moyenne_min":12.0,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Économiste","taux_emploi":72},
    {"nom":"Génie civil","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur BTP","taux_emploi":82},
    {"nom":"Agronomie","domaine":"Agriculture","duree_annees":5,"moyenne_min":11.5,"series_compatibles":["sciences"],"interets_associes":["agri","sciences"],"debouches":"Ingénieur agronome","taux_emploi":65},
    {"nom":"Informatique de gestion","domaine":"Informatique","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths","sciences"],"interets_associes":["tech","business"],"debouches":"Développeur web","taux_emploi":78},
]

@router.post("/seed")
async def seed_database():
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_async_engine(db_url)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as db:
        for w_id, nom, code, region in WILAYAS:
            db.add(Wilaya(id=w_id, nom=nom, code=code, region=region))
        for f in FILIERES:
            db.add(Filiere(**f))
        await db.commit()
    await engine.dispose()
    return {"status": "ok", "wilayas": len(WILAYAS), "filieres": len(FILIERES)}
