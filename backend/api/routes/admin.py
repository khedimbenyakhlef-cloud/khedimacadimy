from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from core.config import settings
from models.recommandation import Wilaya, Universite, Offre
from models.filiere import Filiere
from datetime import datetime
import uuid

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

FILIERES_DATA = [
    # Santé
    {"nom":"Médecine générale","domaine":"Santé","duree_annees":7,"moyenne_min":16.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Médecin généraliste, spécialiste","taux_emploi":95},
    {"nom":"Pharmacie","domaine":"Santé","duree_annees":5,"moyenne_min":15.5,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Pharmacien, industrie pharmaceutique","taux_emploi":90},
    {"nom":"Chirurgie dentaire","domaine":"Santé","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Dentiste, chirurgien","taux_emploi":88},
    {"nom":"Médecine vétérinaire","domaine":"Santé","duree_annees":5,"moyenne_min":14.5,"series_compatibles":["sciences"],"interets_associes":["sante","agri","sciences"],"debouches":"Vétérinaire, inspection alimentaire","taux_emploi":80},
    {"nom":"Sciences infirmières","domaine":"Santé","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["sciences"],"interets_associes":["sante","social"],"debouches":"Infirmier, aide soignant","taux_emploi":92},
    # Informatique & Tech
    {"nom":"Génie informatique","domaine":"Informatique","duree_annees":5,"moyenne_min":14.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Développeur, data scientist, IA","taux_emploi":88},
    {"nom":"Informatique de gestion","domaine":"Informatique","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths","sciences"],"interets_associes":["tech","business"],"debouches":"Développeur web, analyste SI","taux_emploi":78},
    {"nom":"Systèmes informatiques","domaine":"Informatique","duree_annees":3,"moyenne_min":12.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Administrateur réseau, sécurité","taux_emploi":82},
    {"nom":"Intelligence artificielle","domaine":"Informatique","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["sciences","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur IA, data scientist","taux_emploi":90},
    # Ingénierie
    {"nom":"Génie électronique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électronicien, Sonatrach","taux_emploi":82},
    {"nom":"Génie civil","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur BTP, bureau d'études","taux_emploi":82},
    {"nom":"Génie mécanique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur mécanique, industrie","taux_emploi":78},
    {"nom":"Génie chimique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["sciences","technique"],"interets_asocies":["sciences","tech"],"debouches":"Ingénieur chimiste, pétrochimie","taux_emploi":75},
    {"nom":"Génie des procédés","domaine":"Ingénierie","duree_annees":5,"moyenne_min":12.5,"series_compatibles":["sciences","technique"],"interets_associes":["sciences","tech"],"debouches":"Ingénieur process, Sonatrach","taux_emploi":80},
    {"nom":"Génie électrique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électricien, Sonelgaz","taux_emploi":83},
    {"nom":"Architecture","domaine":"Architecture","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["sciences","technique"],"interets_associes":["art","tech"],"debouches":"Architecte, urbaniste","taux_emploi":75},
    # Sciences
    {"nom":"Mathématiques","domaine":"Sciences","duree_annees":3,"moyenne_min":13.0,"series_compatibles":["maths","sciences"],"interets_associes":["sciences","tech"],"debouches":"Enseignant, actuaire, statisticien","taux_emploi":70},
    {"nom":"Physique","domaine":"Sciences","duree_annees":3,"moyenne_min":12.5,"series_compatibles":["maths","sciences","technique"],"interets_associes":["sciences","tech"],"debouches":"Enseignant, ingénieur, chercheur","taux_emploi":65},
    {"nom":"Chimie","domaine":"Sciences","duree_annees":3,"moyenne_min":12.0,"series_compatibles":["sciences"],"interets_associes":["sciences","agri"],"debouches":"Chimiste, laboratoire, industrie","taux_emploi":65},
    {"nom":"Biologie","domaine":"Sciences","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["sciences"],"interets_associes":["sciences","sante","agri"],"debouches":"Biologiste, laboratoire","taux_emploi":60},
    {"nom":"Sciences de la nature","domaine":"Sciences","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["sciences"],"interets_associes":["sciences","agri"],"debouches":"Enseignant, chercheur","taux_emploi":55},
    # Économie & Gestion
    {"nom":"Sciences économiques","domaine":"Économie","duree_annees":5,"moyenne_min":12.0,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Économiste, analyste financier","taux_emploi":72},
    {"nom":"Sciences de gestion","domaine":"Gestion","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Manager, RH, comptable","taux_emploi":68},
    {"nom":"Commerce international","domaine":"Commerce","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","langues"],"interets_associes":["business","social"],"debouches":"Trader, import-export, logistique","taux_emploi":70},
    {"nom":"Finance et comptabilité","domaine":"Finance","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths"],"interets_associes":["business"],"debouches":"Comptable, auditeur, banquier","taux_emploi":75},
    {"nom":"Marketing","domaine":"Commerce","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","langues"],"interets_associes":["business","art"],"debouches":"Marketeur, chef de produit","taux_emploi":65},
    # Droit & Sciences sociales
    {"nom":"Droit","domaine":"Droit","duree_annees":4,"moyenne_min":12.0,"series_compatibles":["lettres","gestion"],"interets_associes":["droit","social"],"debouches":"Avocat, magistrat, notaire","taux_emploi":70},
    {"nom":"Sciences politiques","domaine":"Sciences sociales","duree_annees":4,"moyenne_min":11.5,"series_compatibles":["lettres","gestion"],"interets_associes":["social","droit"],"debouches":"Diplomate, analyste politique","taux_emploi":55},
    {"nom":"Sociologie","domaine":"Sciences sociales","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["lettres","gestion"],"interets_associes":["social"],"debouches":"Sociologue, travailleur social","taux_emploi":50},
    {"nom":"Psychologie","domaine":"Sciences sociales","duree_annees":5,"moyenne_min":11.0,"series_compatibles":["lettres","sciences"],"interets_associes":["sante","social"],"debouches":"Psychologue, conseiller","taux_emploi":60},
    # Lettres & Langues
    {"nom":"Lettres arabes","domaine":"Lettres","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres"],"interets_associes":["social"],"debouches":"Enseignant, journaliste, traducteur","taux_emploi":55},
    {"nom":"Lettres françaises","domaine":"Lettres","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres","langues"],"interets_associes":["social","art"],"debouches":"Enseignant, traducteur, journaliste","taux_emploi":52},
    {"nom":"Langue anglaise","domaine":"Langues","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["langues","lettres"],"interets_associes":["social","business"],"debouches":"Traducteur, enseignant, interprète","taux_emploi":60},
    {"nom":"Traduction","domaine":"Langues","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["langues","lettres"],"interets_associes":["social","business"],"debouches":"Traducteur, interprète, journaliste","taux_emploi":58},
    # Agriculture
    {"nom":"Agronomie","domaine":"Agriculture","duree_annees":5,"moyenne_min":11.5,"series_compatibles":["sciences"],"interets_associes":["agri","sciences"],"debouches":"Ingénieur agronome, INRA","taux_emploi":65},
    {"nom":"Sciences vétérinaires","domaine":"Agriculture","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["sciences"],"interets_associes":["agri","sante","sciences"],"debouches":"Vétérinaire, inspecteur","taux_emploi":78},
    {"nom":"Hydraulique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":12.5,"series_compatibles":["technique","maths"],"interets_associes":["tech","agri"],"debouches":"Ingénieur hydraulique, ADE","taux_emploi":80},
]

UNIVERSITES_DATA = [
    {"nom":"USTHB Alger","wilaya_id":16,"type":"Université"},
    {"nom":"Université Alger 1 Benyoucef Benkhedda","wilaya_id":16,"type":"Université"},
    {"nom":"Université Alger 3","wilaya_id":16,"type":"Université"},
    {"nom":"Université d'Oran 1 Ahmed Ben Bella","wilaya_id":31,"type":"Université"},
    {"nom":"Université d'Oran 2 Mohamed Ben Ahmed","wilaya_id":31,"type":"Université"},
    {"nom":"Université Frères Mentouri Constantine 1","wilaya_id":25,"type":"Université"},
    {"nom":"Université Constantine 3","wilaya_id":25,"type":"Université"},
    {"nom":"Université Badji Mokhtar Annaba","wilaya_id":23,"type":"Université"},
    {"nom":"Université Batna 1 Hadj Lakhdar","wilaya_id":5,"type":"Université"},
    {"nom":"Université Batna 2 Mostefa Ben Boulaïd","wilaya_id":5,"type":"Université"},
    {"nom":"Université Sétif 1 Ferhat Abbas","wilaya_id":19,"type":"Université"},
    {"nom":"Université Mouloud Mammeri Tizi Ouzou","wilaya_id":15,"type":"Université"},
    {"nom":"Université Abderrahmane Mira Béjaïa","wilaya_id":6,"type":"Université"},
    {"nom":"Université Abou Bekr Belkaïd Tlemcen","wilaya_id":13,"type":"Université"},
    {"nom":"Université Saad Dahleb Blida 1","wilaya_id":9,"type":"Université"},
    {"nom":"Université Yahia Fares Médéa","wilaya_id":26,"type":"Université"},
    {"nom":"Université Boumerdès","wilaya_id":35,"type":"Université"},
    {"nom":"Université Abdelhamid Ibn Badis Mostaganem","wilaya_id":27,"type":"Université"},
    {"nom":"Université Djillali Liabes Sidi Bel Abbès","wilaya_id":22,"type":"Université"},
    {"nom":"Université Hassiba Benbouali Chlef","wilaya_id":2,"type":"Université"},
    {"nom":"Université Mohamed Boudiaf M'Sila","wilaya_id":28,"type":"Université"},
    {"nom":"Université Ibn Khaldoun Tiaret","wilaya_id":14,"type":"Université"},
    {"nom":"Université Kasdi Merbah Ouargla","wilaya_id":30,"type":"Université"},
    {"nom":"Université Tahri Mohamed Béchar","wilaya_id":8,"type":"Université"},
    {"nom":"Université Biskra Mohamed Khider","wilaya_id":7,"type":"Université"},
    {"nom":"Université Guelma","wilaya_id":24,"type":"Université"},
    {"nom":"Université Jijel Mohamed Seddik Benyahia","wilaya_id":18,"type":"Université"},
    {"nom":"Université Skikda","wilaya_id":21,"type":"Université"},
    {"nom":"Université Souk Ahras","wilaya_id":41,"type":"Université"},
    {"nom":"Université Tipaza","wilaya_id":42,"type":"Université"},
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
        # Nettoyer dans l'ordre
        await db.execute(text("DELETE FROM recommendations"))
        await db.execute(text("DELETE FROM temoignages"))
        await db.execute(text("DELETE FROM offres"))
        await db.execute(text("DELETE FROM filieres"))
        await db.execute(text("DELETE FROM universites"))
        await db.execute(text("DELETE FROM wilayas"))
        await db.execute(text("DELETE FROM profils_bac"))
        await db.execute(text("DELETE FROM utilisateurs"))
        await db.commit()

        # Wilayas
        for w_id, nom, code, region in WILAYAS:
            db.add(Wilaya(id=w_id, nom=nom, code=code, region=region))
        await db.flush()

        # Filières
        filiere_ids = []
        for f in FILIERES_DATA:
            fid = uuid.uuid4()
            filiere_ids.append((fid, f["moyenne_min"]))
            db.add(Filiere(id=fid, **f))
        await db.flush()

        # Universités
        univ_ids = []
        for u in UNIVERSITES_DATA:
            uid = uuid.uuid4()
            univ_ids.append(uid)
            db.add(Universite(id=uid, **u))
        await db.flush()

        # Offres
        nb_offres = 0
        for fid, moy_min in filiere_ids:
            for uid in univ_ids:
                db.add(Offre(id=uuid.uuid4(), filiere_id=fid, universite_id=uid, annee=annee, capacite=50, moyenne_derniere=moy_min))
                nb_offres += 1

        await db.commit()
    await engine.dispose()
    return {"status": "ok", "wilayas": len(WILAYAS), "filieres": len(FILIERES_DATA), "universites": len(UNIVERSITES_DATA), "offres": nb_offres}
