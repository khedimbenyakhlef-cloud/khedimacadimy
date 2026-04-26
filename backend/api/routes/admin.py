from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings
from models.recommandation import Wilaya, Universite, Offre
from models.filiere import Filiere
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

WILAYAS = [
    (1,"Adrar","01","Sud"),(2,"Chlef","02","Centre-Ouest"),(3,"Laghouat","03","Sud"),
    (4,"Oum El Bouaghi","04","Est"),(5,"Batna","05","Est"),(6,"Béjaïa","06","Kabylie"),
    (7,"Biskra","07","Sud-Est"),(8,"Béchar","08","Sud-Ouest"),(9,"Blida","09","Centre"),
    (10,"Bouira","10","Centre"),(11,"Tamanrasset","11","Sud"),(12,"Tébessa","12","Est"),
    (13,"Tlemcen","13","Ouest"),(14,"Tiaret","14","Ouest"),(15,"Tizi Ouzou","15","Kabylie"),
    (16,"Alger","16","Centre"),(17,"Djelfa","17","Centre"),(18,"Jijel","18","Est"),
    (19,"Sétif","19","Est"),(20,"Saïda","20","Ouest"),(21,"Skikda","21","Est"),
    (22,"Sidi Bel Abbès","22","Ouest"),(23,"Annaba","23","Nord-Est"),(24,"Guelma","24","Est"),
    (25,"Constantine","25","Est"),(26,"Médéa","26","Centre"),(27,"Mostaganem","27","Ouest"),
    (28,"M'Sila","28","Centre"),(29,"Mascara","29","Ouest"),(30,"Ouargla","30","Sud"),
    (31,"Oran","31","Ouest"),(32,"El Bayadh","32","Sud-Ouest"),(33,"Illizi","33","Sud"),
    (34,"Bordj Bou Arréridj","34","Est"),(35,"Boumerdès","35","Centre"),(36,"El Tarf","36","Est"),
    (37,"Tindouf","37","Sud"),(38,"Tissemsilt","38","Ouest"),(39,"El Oued","39","Sud-Est"),
    (40,"Khenchela","40","Est"),(41,"Souk Ahras","41","Est"),(42,"Tipaza","42","Centre"),
    (43,"Mila","43","Est"),(44,"Aïn Defla","44","Centre-Ouest"),(45,"Naâma","45","Sud-Ouest"),
    (46,"Aïn Témouchent","46","Ouest"),(47,"Ghardaïa","47","Sud"),(48,"Relizane","48","Ouest"),
    (49,"Timimoun","49","Sud"),(50,"Bordj Badji Mokhtar","50","Sud"),(51,"Ouled Djellal","51","Sud"),
    (52,"Béni Abbès","52","Sud-Ouest"),(53,"In Salah","53","Sud"),(54,"In Guezzam","54","Sud"),
    (55,"Touggourt","55","Sud-Est"),(56,"Djanet","56","Sud"),(57,"El M'Ghair","57","Sud-Est"),
    (58,"El Meniaa","58","Sud"),
]

FILIERES = [
    {"id":1,"nom":"Médecine générale","domaine":"Santé","duree_annees":7,"moyenne_min":16.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Médecin généraliste","taux_emploi":95},
    {"id":2,"nom":"Pharmacie","domaine":"Santé","duree_annees":5,"moyenne_min":15.5,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Pharmacien","taux_emploi":90},
    {"id":3,"nom":"Génie informatique","domaine":"Informatique","duree_annees":5,"moyenne_min":14.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Développeur, IA","taux_emploi":88},
    {"id":4,"nom":"Génie électronique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électronicien","taux_emploi":82},
    {"id":5,"nom":"Architecture","domaine":"Architecture","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["sciences","technique"],"interets_associes":["art","tech"],"debouches":"Architecte","taux_emploi":75},
    {"id":6,"nom":"Droit","domaine":"Droit","duree_annees":4,"moyenne_min":12.0,"series_compatibles":["lettres","gestion"],"interets_associes":["droit","social"],"debouches":"Avocat, magistrat","taux_emploi":70},
    {"id":7,"nom":"Sciences économiques","domaine":"Économie","duree_annees":5,"moyenne_min":12.0,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Économiste","taux_emploi":72},
    {"id":8,"nom":"Génie civil","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur BTP","taux_emploi":82},
    {"id":9,"nom":"Agronomie","domaine":"Agriculture","duree_annees":5,"moyenne_min":11.5,"series_compatibles":["sciences"],"interets_associes":["agri","sciences"],"debouches":"Ingénieur agronome","taux_emploi":65},
    {"id":10,"nom":"Informatique de gestion","domaine":"Informatique","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths","sciences"],"interets_associes":["tech","business"],"debouches":"Développeur web","taux_emploi":78},
]

UNIVERSITES = [
    {"id":1,"nom":"USTHB Alger","wilaya_id":16,"type":"Université"},
    {"id":2,"nom":"Université Alger 1","wilaya_id":16,"type":"Université"},
    {"id":3,"nom":"Université Alger 3","wilaya_id":16,"type":"Université"},
    {"id":4,"nom":"Université d'Oran 1","wilaya_id":31,"type":"Université"},
    {"id":5,"nom":"Université d'Oran 2","wilaya_id":31,"type":"Université"},
    {"id":6,"nom":"Université Constantine 1","wilaya_id":25,"type":"Université"},
    {"id":7,"nom":"Université Constantine 3","wilaya_id":25,"type":"Université"},
    {"id":8,"nom":"Université Annaba","wilaya_id":23,"type":"Université"},
    {"id":9,"nom":"Université Batna 1","wilaya_id":5,"type":"Université"},
    {"id":10,"nom":"Université Batna 2","wilaya_id":5,"type":"Université"},
    {"id":11,"nom":"Université Sétif 1","wilaya_id":19,"type":"Université"},
    {"id":12,"nom":"Université Tizi Ouzou","wilaya_id":15,"type":"Université"},
    {"id":13,"nom":"Université Béjaïa","wilaya_id":6,"type":"Université"},
    {"id":14,"nom":"Université Tlemcen","wilaya_id":13,"type":"Université"},
    {"id":15,"nom":"Université Blida 1","wilaya_id":9,"type":"Université"},
    {"id":16,"nom":"Université Blida 2","wilaya_id":9,"type":"Université"},
    {"id":17,"nom":"Université Médéa","wilaya_id":26,"type":"Université"},
    {"id":18,"nom":"Université Boumerdès","wilaya_id":35,"type":"Université"},
    {"id":19,"nom":"Université Tipaza","wilaya_id":42,"type":"Université"},
    {"id":20,"nom":"Université Mostaganem","wilaya_id":27,"type":"Université"},
]

@router.post("/seed")
async def seed_database():
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_async_engine(db_url)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    annee = datetime.now().year
    async with SessionLocal() as db:
        for w_id, nom, code, region in WILAYAS:
            db.add(Wilaya(id=w_id, nom=nom, code=code, region=region))
        await db.flush()
        for f in FILIERES:
            data = {k:v for k,v in f.items() if k != "id"}
            db.add(Filiere(id=f["id"], **data))
        await db.flush()
        for u in UNIVERSITES:
            db.add(Universite(**u))
        await db.flush()
        offre_id = 1
        for f in FILIERES:
            for u in UNIVERSITES:
                db.add(Offre(id=offre_id, filiere_id=f["id"], universite_id=u["id"], annee=annee, capacite=50, moyenne_derniere=f["moyenne_min"]))
                offre_id += 1
        await db.commit()
    await engine.dispose()
    return {"status": "ok", "wilayas": len(WILAYAS), "filieres": len(FILIERES), "universites": len(UNIVERSITES), "offres": offre_id-1}
