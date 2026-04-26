"""
Script de seed : insère les 48 wilayas + filieres de base
Lancer avec : python scripts/seed_data.py
"""
import asyncio
import sys
sys.path.append(".")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.models.recommandation import Wilaya
from app.models.filiere import Filiere
from app.db.base import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

WILAYAS = [
    (1, "Adrar", "01", "Sud"), (2, "Chlef", "02", "Centre-Ouest"),
    (3, "Laghouat", "03", "Sud"), (4, "Oum El Bouaghi", "04", "Est"),
    (5, "Batna", "05", "Est"), (6, "Béjaïa", "06", "Kabylie"),
    (7, "Biskra", "07", "Sud-Est"), (8, "Béchar", "08", "Sud-Ouest"),
    (9, "Blida", "09", "Centre"), (10, "Bouira", "10", "Centre"),
    (16, "Alger", "16", "Centre"), (19, "Sétif", "19", "Est"),
    (23, "Annaba", "23", "Nord-Est"), (25, "Constantine", "25", "Est"),
    (31, "Oran", "31", "Ouest"),
]

FILIERES = [
    {
        "nom": "Médecine générale",
        "domaine": "Santé",
        "duree_annees": 7,
        "moyenne_min": 16.0,
        "series_compatibles": ["sciences"],
        "interets_associes": ["sante", "sciences"],
        "debouches": "Médecin généraliste, spécialiste, chercheur",
        "taux_emploi": 95,
    },
    {
        "nom": "Pharmacie",
        "domaine": "Santé",
        "duree_annees": 5,
        "moyenne_min": 15.5,
        "series_compatibles": ["sciences"],
        "interets_associes": ["sante", "sciences"],
        "debouches": "Pharmacien, industrie pharmaceutique",
        "taux_emploi": 90,
    },
    {
        "nom": "Génie informatique",
        "domaine": "Informatique",
        "duree_annees": 5,
        "moyenne_min": 14.0,
        "series_compatibles": ["sciences", "maths", "technique"],
        "interets_associes": ["tech", "sciences"],
        "debouches": "Développeur, data scientist, DevOps, IA",
        "taux_emploi": 88,
    },
    {
        "nom": "Génie électronique",
        "domaine": "Ingénierie",
        "duree_annees": 5,
        "moyenne_min": 13.5,
        "series_compatibles": ["technique", "maths", "sciences"],
        "interets_associes": ["tech", "sciences"],
        "debouches": "Ingénieur électronicien, Sonatrach, Sonelgaz",
        "taux_emploi": 82,
    },
    {
        "nom": "Architecture",
        "domaine": "Architecture",
        "duree_annees": 5,
        "moyenne_min": 13.5,
        "series_compatibles": ["sciences", "technique"],
        "interets_associes": ["art", "tech"],
        "debouches": "Architecte, urbaniste, bureau d'études",
        "taux_emploi": 75,
    },
    {
        "nom": "Droit",
        "domaine": "Droit",
        "duree_annees": 4,
        "moyenne_min": 12.0,
        "series_compatibles": ["lettres", "gestion"],
        "interets_associes": ["droit", "social"],
        "debouches": "Avocat, magistrat, notaire, conseiller juridique",
        "taux_emploi": 70,
    },
    {
        "nom": "Sciences économiques",
        "domaine": "Économie",
        "duree_annees": 5,
        "moyenne_min": 12.0,
        "series_compatibles": ["gestion", "maths"],
        "interets_associes": ["business", "social"],
        "debouches": "Économiste, analyste financier, banquier",
        "taux_emploi": 72,
    },
    {
        "nom": "Génie civil",
        "domaine": "Ingénierie",
        "duree_annees": 5,
        "moyenne_min": 13.0,
        "series_compatibles": ["technique", "maths"],
        "interets_associes": ["tech", "sciences"],
        "debouches": "Ingénieur BTP, chef de projet, bureau d'études",
        "taux_emploi": 82,
    },
    {
        "nom": "Agronomie",
        "domaine": "Agriculture",
        "duree_annees": 5,
        "moyenne_min": 11.5,
        "series_compatibles": ["sciences"],
        "interets_associes": ["agri", "sciences"],
        "debouches": "Ingénieur agronome, chercheur, INRA",
        "taux_emploi": 65,
    },
    {
        "nom": "Informatique de gestion",
        "domaine": "Informatique",
        "duree_annees": 3,
        "moyenne_min": 11.0,
        "series_compatibles": ["gestion", "maths", "sciences"],
        "interets_associes": ["tech", "business"],
        "debouches": "Analyste ERP, développeur web, administrateur SI",
        "taux_emploi": 78,
    },
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        for w_id, nom, code, region in WILAYAS:
            wilaya = Wilaya(id=w_id, nom=nom, code=code, region=region)
            db.add(wilaya)

        for f in FILIERES:
            filiere = Filiere(**f)
            db.add(filiere)

        await db.commit()
        print(f"✓ {len(WILAYAS)} wilayas et {len(FILIERES)} filières insérées.")


if __name__ == "__main__":
    asyncio.run(seed())
