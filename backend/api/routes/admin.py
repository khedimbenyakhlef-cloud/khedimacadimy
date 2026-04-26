from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db.session import get_db
from models.recommandation import Wilaya, Universite, Offre
from models.filiere import Filiere
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])

WILAYAS = [
    (1,"Adrar","01","Sud",27.8741,0.2822),(2,"Chlef","02","Centre-Ouest",36.1647,1.3317),
    (3,"Laghouat","03","Sud",33.8000,2.8667),(4,"Oum El Bouaghi","04","Est",35.8833,7.1167),
    (5,"Batna","05","Est",35.5561,6.1744),(6,"Béjaïa","06","Kabylie",36.7508,5.0564),
    (7,"Biskra","07","Sud-Est",34.8500,5.7333),(8,"Béchar","08","Sud-Ouest",31.6167,-2.2167),
    (9,"Blida","09","Centre",36.4800,2.8289),(10,"Bouira","10","Centre",36.3731,3.9003),
    (11,"Tamanrasset","11","Sud",22.7850,5.5228),(12,"Tébessa","12","Est",35.4042,8.1244),
    (13,"Tlemcen","13","Ouest",34.8828,-1.3167),(14,"Tiaret","14","Ouest",35.3706,1.3214),
    (15,"Tizi Ouzou","15","Kabylie",36.7169,4.0497),(16,"Alger","16","Centre",36.7372,3.0869),
    (17,"Djelfa","17","Centre",34.6731,3.2631),(18,"Jijel","18","Est",36.8222,5.7656),
    (19,"Sétif","19","Est",36.1898,5.4103),(20,"Saïda","20","Ouest",34.8306,0.1542),
    (21,"Skikda","21","Est",36.8761,6.9064),(22,"Sidi Bel Abbès","22","Ouest",35.1897,-0.6306),
    (23,"Annaba","23","Nord-Est",36.9000,7.7667),(24,"Guelma","24","Est",36.4617,7.4328),
    (25,"Constantine","25","Est",36.3650,6.6147),(26,"Médéa","26","Centre",36.2642,2.7542),
    (27,"Mostaganem","27","Ouest",35.9317,0.0892),(28,"M'Sila","28","Centre",35.7064,4.5444),
    (29,"Mascara","29","Ouest",35.3958,0.1408),(30,"Ouargla","30","Sud",31.9492,5.3239),
    (31,"Oran","31","Ouest",35.6969,-0.6331),(32,"El Bayadh","32","Sud-Ouest",33.6831,1.0069),
    (33,"Illizi","33","Sud",26.5000,8.4833),(34,"Bordj Bou Arreridj","34","Centre",36.0736,4.7633),
    (35,"Boumerdès","35","Centre",36.7667,3.4667),(36,"El Tarf","36","Est",36.7678,8.3133),
    (37,"Tindouf","37","Sud-Ouest",27.6744,-8.1472),(38,"Tissemsilt","38","Ouest",35.6075,1.8136),
    (39,"El Oued","39","Sud",33.3678,6.8536),(40,"Khenchela","40","Est",35.4292,7.1439),
    (41,"Souk Ahras","41","Est",36.2864,7.9514),(42,"Tipaza","42","Centre",36.5881,2.4475),
    (43,"Mila","43","Est",36.4503,6.2636),(44,"Aïn Defla","44","Centre-Ouest",36.2572,1.9658),
    (45,"Naâma","45","Sud-Ouest",33.2672,-0.3156),(46,"Aïn Témouchent","46","Ouest",35.2989,-1.1408),
    (47,"Ghardaïa","47","Sud",32.4908,3.6739),(48,"Relizane","48","Ouest",35.7381,0.5564),
    (49,"Timimoun","49","Sud",29.2639,0.2311),(50,"Bordj Badji Mokhtar","50","Sud",21.3333,0.9500),
    (51,"Ouled Djellal","51","Sud",34.4167,5.0667),(52,"Béni Abbès","52","Sud-Ouest",30.1289,-2.1603),
    (53,"In Salah","53","Sud",27.1967,2.4797),(54,"In Guezzam","54","Sud",19.5667,5.7667),
    (55,"Touggourt","55","Sud",33.1000,6.0667),(56,"Djanet","56","Sud",24.5500,9.4833),
    (57,"El M'Ghair","57","Sud",33.9500,5.9167),(58,"El Menia","58","Sud",30.5833,2.8833),
]

UNIVERSITES_DATA = [
    # ALGER
    {"nom":"Université Alger 1 Benyoucef Benkhedda","wilaya_id":16,"type":"univ","lat":36.7372,"lng":3.0869,
     "filieres":["Droit","Médecine générale","Pharmacie","Chirurgie dentaire","Sciences islamiques"],
     "moyennes":{"Médecine générale":16.5,"Pharmacie":15.5,"Chirurgie dentaire":15.0,"Droit":12.0,"Sciences islamiques":10.0}},
    {"nom":"Université Alger 2 Abou El Kacem Saâdallah","wilaya_id":16,"type":"univ","lat":36.7500,"lng":3.0600,
     "filieres":["Psychologie","Sociologie","Langue anglaise","Langue française","Traduction","Histoire","Philosophie"],
     "moyennes":{"Psychologie":11.0,"Sociologie":10.5,"Langue anglaise":11.0,"Traduction":11.5,"Histoire":10.0,"Philosophie":10.0,"Langue française":10.0}},
    {"nom":"Université Alger 3 Hassiba Ben Bouali","wilaya_id":16,"type":"univ","lat":36.7200,"lng":3.0750,
     "filieres":["Sciences économiques","Sciences de gestion","Commerce international","Finance et comptabilité","Marketing","Économie numérique"],
     "moyennes":{"Sciences économiques":12.0,"Sciences de gestion":11.0,"Commerce international":11.5,"Finance et comptabilité":11.5,"Marketing":11.0,"Économie numérique":13.0}},
    {"nom":"USTHB - Université des Sciences et Technologie Houari Boumediene","wilaya_id":16,"type":"univ","lat":36.7058,"lng":3.1789,
     "filieres":["Génie informatique","Mathématiques","Physique","Chimie","Biologie","Intelligence artificielle","Cybersécurité"],
     "moyennes":{"Génie informatique":14.5,"Mathématiques":13.5,"Physique":13.0,"Chimie":12.5,"Biologie":11.5,"Intelligence artificielle":15.0,"Cybersécurité":14.0}},
    {"nom":"École Nationale Polytechnique d'Alger","wilaya_id":16,"type":"ecole","lat":36.7072,"lng":3.1781,
     "filieres":["Génie civil","Génie électrique","Génie mécanique","Génie chimique","Génie des procédés"],
     "moyennes":{"Génie civil":14.0,"Génie électrique":14.0,"Génie mécanique":13.5,"Génie chimique":13.5,"Génie des procédés":13.0}},
    # ORAN
    {"nom":"Université Oran 1 Ahmed Ben Bella","wilaya_id":31,"type":"univ","lat":35.6969,"lng":-0.6331,
     "filieres":["Médecine générale","Droit","Psychologie","Sciences économiques","Langue anglaise","Archivistique","Entrepreneuriat artistique"],
     "moyennes":{"Médecine générale":16.0,"Droit":12.0,"Psychologie":11.0,"Sciences économiques":12.0,"Langue anglaise":11.0,"Archivistique":10.5,"Entrepreneuriat artistique":10.5}},
    {"nom":"Université Oran 2 Mohamed Ben Ahmed","wilaya_id":31,"type":"univ","lat":35.7000,"lng":-0.6200,
     "filieres":["Génie informatique","Sciences de gestion","Commerce international","Langue italienne","Finance et comptabilité"],
     "moyennes":{"Génie informatique":13.5,"Sciences de gestion":11.0,"Commerce international":11.5,"Langue italienne":10.5,"Finance et comptabilité":11.5}},
    {"nom":"USTO - Université des Sciences et Technologie Mohamed Boudiaf Oran","wilaya_id":31,"type":"univ","lat":35.6833,"lng":-0.6500,
     "filieres":["Génie civil","Génie électronique","Génie mécanique","Architecture","Mathématiques","Physique"],
     "moyennes":{"Génie civil":13.5,"Génie électronique":13.5,"Génie mécanique":13.0,"Architecture":13.5,"Mathématiques":13.0,"Physique":12.5}},
    # CONSTANTINE
    {"nom":"Université Constantine 1 Frères Mentouri","wilaya_id":25,"type":"univ","lat":36.3650,"lng":6.6147,
     "filieres":["Médecine générale","Architecture","Droit","Sciences économiques","Mathématiques"],
     "moyennes":{"Médecine générale":16.0,"Architecture":13.5,"Droit":12.0,"Sciences économiques":12.0,"Mathématiques":13.0}},
    {"nom":"Université Constantine 2 Abdelhamid Mehri","wilaya_id":25,"type":"univ","lat":36.3700,"lng":6.6200,
     "filieres":["Génie informatique","Systèmes informatiques","Intelligence artificielle","Psychologie","Sociologie"],
     "moyennes":{"Génie informatique":14.0,"Systèmes informatiques":12.5,"Intelligence artificielle":15.0,"Psychologie":11.0,"Sociologie":10.5}},
    {"nom":"Université Constantine 3 Salah Boubnider","wilaya_id":25,"type":"univ","lat":36.3600,"lng":6.6100,
     "filieres":["Médecine générale","Pharmacie","Chirurgie dentaire","Sciences infirmières"],
     "moyennes":{"Médecine générale":16.5,"Pharmacie":15.5,"Chirurgie dentaire":15.0,"Sciences infirmières":11.0}},
    # ANNABA
    {"nom":"Université Annaba Badji Mokhtar","wilaya_id":23,"type":"univ","lat":36.9000,"lng":7.7667,
     "filieres":["Médecine générale","Génie civil","Génie mécanique","Droit","Chimie","Biologie"],
     "moyennes":{"Médecine générale":16.0,"Génie civil":13.0,"Génie mécanique":13.0,"Droit":12.0,"Chimie":12.0,"Biologie":11.0}},
    # SÉTIF
    {"nom":"Université Sétif 1 Ferhat Abbas","wilaya_id":19,"type":"univ","lat":36.1898,"lng":5.4103,
     "filieres":["Médecine générale","Génie informatique","Droit","Sciences économiques","Architecture"],
     "moyennes":{"Médecine générale":16.0,"Génie informatique":14.0,"Droit":12.0,"Sciences économiques":12.0,"Architecture":13.5}},
    {"nom":"Université Sétif 2","wilaya_id":19,"type":"univ","lat":36.1950,"lng":5.4150,
     "filieres":["Langue anglaise","Langue française","Traduction","Psychologie","Sociologie"],
     "moyennes":{"Langue anglaise":11.0,"Langue française":10.5,"Traduction":11.5,"Psychologie":11.0,"Sociologie":10.5}},
    # BÉJAÏA
    {"nom":"Université Béjaïa Abderrahmane Mira","wilaya_id":6,"type":"univ","lat":36.7508,"lng":5.0564,
     "filieres":["Génie informatique","Médecine générale","Droit","Sciences économiques","Architecture","Biologie","Agronomie"],
     "moyennes":{"Génie informatique":13.5,"Médecine générale":16.0,"Droit":12.0,"Sciences économiques":12.0,"Architecture":13.5,"Biologie":11.0,"Agronomie":11.5}},
    # TIZI OUZOU
    {"nom":"Université Tizi Ouzou Mouloud Mammeri","wilaya_id":15,"type":"univ","lat":36.7169,"lng":4.0497,
     "filieres":["Génie électrique","Génie civil","Médecine générale","Architecture","Droit","Biologie"],
     "moyennes":{"Génie électrique":13.5,"Génie civil":13.0,"Médecine générale":16.0,"Architecture":13.5,"Droit":12.0,"Biologie":11.0}},
    # BATNA
    {"nom":"Université Batna 1 Hadj Lakhdar","wilaya_id":5,"type":"univ","lat":35.5561,"lng":6.1744,
     "filieres":["Médecine générale","Droit","Sciences économiques","Génie civil"],
     "moyennes":{"Médecine générale":16.0,"Droit":12.0,"Sciences économiques":12.0,"Génie civil":13.0}},
    {"nom":"Université Batna 2 Mostefa Ben Boulaïd","wilaya_id":5,"type":"univ","lat":35.5600,"lng":6.1800,
     "filieres":["Génie informatique","Génie mécanique","Mathématiques","Physique"],
     "moyennes":{"Génie informatique":14.0,"Génie mécanique":13.0,"Mathématiques":13.0,"Physique":12.5}},
    # BLIDA
    {"nom":"Université Blida 1 Saad Dahlab","wilaya_id":9,"type":"univ","lat":36.4800,"lng":2.8289,
     "filieres":["Médecine générale","Génie aéronautique","Génie électronique","Sciences économiques"],
     "moyennes":{"Médecine générale":16.0,"Génie aéronautique":15.0,"Génie électronique":14.0,"Sciences économiques":12.0}},
    # TLEMCEN
    {"nom":"Université Tlemcen Abou Bekr Belkaid","wilaya_id":13,"type":"univ","lat":34.8828,"lng":-1.3167,
     "filieres":["Médecine générale","Génie informatique","Droit","Architecture","Sciences économiques","Génie électrique"],
     "moyennes":{"Médecine générale":16.0,"Génie informatique":13.5,"Droit":12.0,"Architecture":13.5,"Sciences économiques":12.0,"Génie électrique":13.0}},
    # OUARGLA
    {"nom":"Université Ouargla Kasdi Merbah","wilaya_id":30,"type":"univ","lat":31.9492,"lng":5.3239,
     "filieres":["Génie des procédés","Sciences de la nature","Droit","Lettres arabes","Hydraulique"],
     "moyennes":{"Génie des procédés":12.5,"Sciences de la nature":10.5,"Droit":12.0,"Lettres arabes":10.0,"Hydraulique":12.5}},
    # M'SILA
    {"nom":"Université M'Sila Mohamed Boudiaf","wilaya_id":28,"type":"univ","lat":35.7064,"lng":4.5444,
     "filieres":["Génie civil","Sciences économiques","Droit","Lettres arabes","Génie mécanique"],
     "moyennes":{"Génie civil":13.0,"Sciences économiques":12.0,"Droit":12.0,"Lettres arabes":10.0,"Génie mécanique":13.0}},
    # SAÏDA
    {"nom":"Université Saïda Dr Moulay Tahar","wilaya_id":20,"type":"univ","lat":34.8306,"lng":0.1542,
     "filieres":["Orthophonie","Physique","Chimie","Biotechnologie","Conception mécanique","Bio-informatique","Sciences pharmaceutiques"],
     "moyennes":{"Orthophonie":12.0,"Physique":12.5,"Chimie":12.0,"Biotechnologie":13.0,"Conception mécanique":12.5,"Bio-informatique":13.5,"Sciences pharmaceutiques":15.0}},
    # RELIZANE
    {"nom":"Université Relizane Chahid Ahmed Zabana","wilaya_id":48,"type":"univ","lat":35.7381,"lng":0.5564,
     "filieres":["Sciences économiques","Droit","Génie civil","Lettres arabes","Sciences de la nature"],
     "moyennes":{"Sciences économiques":12.0,"Droit":12.0,"Génie civil":13.0,"Lettres arabes":10.0,"Sciences de la nature":10.5}},
    # MASCARA
    {"nom":"Université Mascara Mustapha Stambouli","wilaya_id":29,"type":"univ","lat":35.3958,"lng":0.1408,
     "filieres":["Agronomie","Sciences économiques","Droit","Génie civil","Biologie"],
     "moyennes":{"Agronomie":11.5,"Sciences économiques":12.0,"Droit":12.0,"Génie civil":13.0,"Biologie":11.0}},
]

FILIERES_DATA = [
    {"nom":"Médecine générale","domaine":"Santé","duree_annees":7,"moyenne_min":16.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Médecin généraliste, spécialiste, chercheur","taux_emploi":95},
    {"nom":"Pharmacie","domaine":"Santé","duree_annees":5,"moyenne_min":15.5,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Pharmacien, industrie pharmaceutique","taux_emploi":90},
    {"nom":"Chirurgie dentaire","domaine":"Santé","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Dentiste, chirurgien","taux_emploi":88},
    {"nom":"Sciences infirmières","domaine":"Santé","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["sciences"],"interets_associes":["sante","social"],"debouches":"Infirmier, aide soignant","taux_emploi":92},
    {"nom":"Orthophonie","domaine":"Santé","duree_annees":4,"moyenne_min":12.0,"series_compatibles":["sciences","lettres"],"interets_associes":["sante","social"],"debouches":"Orthophoniste, rééducation","taux_emploi":85},
    {"nom":"Sciences pharmaceutiques","domaine":"Santé","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["sciences"],"interets_associes":["sante","sciences"],"debouches":"Pharmacien, chercheur","taux_emploi":88},
    {"nom":"Génie informatique","domaine":"Informatique","duree_annees":5,"moyenne_min":14.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Développeur, data scientist, IA","taux_emploi":88},
    {"nom":"Intelligence artificielle","domaine":"Informatique","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["sciences","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur IA, data scientist","taux_emploi":92},
    {"nom":"Cybersécurité","domaine":"Informatique","duree_annees":5,"moyenne_min":14.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Expert cybersécurité, pentesteur","taux_emploi":90},
    {"nom":"Systèmes informatiques","domaine":"Informatique","duree_annees":3,"moyenne_min":12.0,"series_compatibles":["sciences","maths","technique"],"interets_associes":["tech","sciences"],"debouches":"Administrateur réseau, sécurité","taux_emploi":82},
    {"nom":"Informatique de gestion","domaine":"Informatique","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths","sciences"],"interets_associes":["tech","business"],"debouches":"Développeur web, analyste SI","taux_emploi":78},
    {"nom":"Bio-informatique","domaine":"Informatique","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["sciences","maths"],"interets_associes":["tech","sciences","sante"],"debouches":"Bio-informaticien, chercheur","taux_emploi":82},
    {"nom":"Économie numérique","domaine":"Informatique","duree_annees":3,"moyenne_min":13.0,"series_compatibles":["gestion","maths","sciences"],"interets_associes":["tech","business"],"debouches":"Entrepreneur digital, e-commerce","taux_emploi":80},
    {"nom":"Génie civil","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur BTP, bureau d'études","taux_emploi":82},
    {"nom":"Génie électronique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électronicien, Sonatrach","taux_emploi":82},
    {"nom":"Génie mécanique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur mécanique, industrie","taux_emploi":78},
    {"nom":"Génie électrique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur électricien, Sonelgaz","taux_emploi":83},
    {"nom":"Génie chimique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["sciences","technique"],"interets_associes":["sciences","tech"],"debouches":"Ingénieur chimiste, pétrochimie","taux_emploi":75},
    {"nom":"Génie des procédés","domaine":"Ingénierie","duree_annees":5,"moyenne_min":12.5,"series_compatibles":["sciences","technique"],"interets_associes":["sciences","tech"],"debouches":"Ingénieur process, Sonatrach","taux_emploi":80},
    {"nom":"Hydraulique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":12.5,"series_compatibles":["technique","maths"],"interets_associes":["tech","agri"],"debouches":"Ingénieur hydraulique, ADE","taux_emploi":80},
    {"nom":"Génie aéronautique","domaine":"Ingénierie","duree_annees":5,"moyenne_min":15.0,"series_compatibles":["technique","maths","sciences"],"interets_associes":["tech","sciences"],"debouches":"Ingénieur aéronautique, Air Algérie","taux_emploi":85},
    {"nom":"Conception mécanique","domaine":"Ingénierie","duree_annees":3,"moyenne_min":12.5,"series_compatibles":["technique","maths"],"interets_associes":["tech","sciences"],"debouches":"Technicien supérieur, industrie","taux_emploi":75},
    {"nom":"Architecture","domaine":"Architecture","duree_annees":5,"moyenne_min":13.5,"series_compatibles":["sciences","technique"],"interets_associes":["art","tech"],"debouches":"Architecte, urbaniste","taux_emploi":75},
    {"nom":"Mathématiques","domaine":"Sciences","duree_annees":3,"moyenne_min":13.0,"series_compatibles":["maths","sciences"],"interets_associes":["sciences","tech"],"debouches":"Enseignant, actuaire, statisticien","taux_emploi":70},
    {"nom":"Physique","domaine":"Sciences","duree_annees":3,"moyenne_min":12.5,"series_compatibles":["maths","sciences","technique"],"interets_associes":["sciences","tech"],"debouches":"Enseignant, ingénieur, chercheur","taux_emploi":65},
    {"nom":"Chimie","domaine":"Sciences","duree_annees":3,"moyenne_min":12.0,"series_compatibles":["sciences"],"interets_associes":["sciences","agri"],"debouches":"Chimiste, laboratoire, industrie","taux_emploi":65},
    {"nom":"Biologie","domaine":"Sciences","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["sciences"],"interets_associes":["sciences","sante","agri"],"debouches":"Biologiste, laboratoire","taux_emploi":60},
    {"nom":"Biotechnologie","domaine":"Sciences","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["sciences"],"interets_associes":["sciences","sante","agri"],"debouches":"Biotechnologiste, industrie pharma","taux_emploi":75},
    {"nom":"Sciences de la nature","domaine":"Sciences","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["sciences"],"interets_associes":["sciences","agri"],"debouches":"Enseignant, chercheur","taux_emploi":55},
    {"nom":"Sciences économiques","domaine":"Économie","duree_annees":5,"moyenne_min":12.0,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Économiste, analyste financier","taux_emploi":72},
    {"nom":"Sciences de gestion","domaine":"Gestion","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["gestion","maths"],"interets_associes":["business","social"],"debouches":"Manager, RH, comptable","taux_emploi":68},
    {"nom":"Commerce international","domaine":"Commerce","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","langues"],"interets_associes":["business","social"],"debouches":"Trader, import-export, logistique","taux_emploi":70},
    {"nom":"Finance et comptabilité","domaine":"Finance","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","maths"],"interets_associes":["business"],"debouches":"Comptable, auditeur, banquier","taux_emploi":75},
    {"nom":"Marketing","domaine":"Commerce","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["gestion","langues"],"interets_associes":["business","art"],"debouches":"Marketeur, chef de produit","taux_emploi":65},
    {"nom":"Archivistique","domaine":"Gestion","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["gestion","lettres"],"interets_associes":["social","business"],"debouches":"Archiviste, bibliothécaire","taux_emploi":60},
    {"nom":"Droit","domaine":"Droit","duree_annees":4,"moyenne_min":12.0,"series_compatibles":["lettres","gestion"],"interets_associes":["droit","social"],"debouches":"Avocat, magistrat, notaire","taux_emploi":70},
    {"nom":"Sciences politiques","domaine":"Sciences sociales","duree_annees":4,"moyenne_min":11.5,"series_compatibles":["lettres","gestion"],"interets_associes":["social","droit"],"debouches":"Diplomate, analyste politique","taux_emploi":55},
    {"nom":"Sociologie","domaine":"Sciences sociales","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["lettres","gestion"],"interets_associes":["social"],"debouches":"Sociologue, travailleur social","taux_emploi":50},
    {"nom":"Psychologie","domaine":"Sciences sociales","duree_annees":5,"moyenne_min":11.0,"series_compatibles":["lettres","sciences"],"interets_associes":["sante","social"],"debouches":"Psychologue, conseiller","taux_emploi":60},
    {"nom":"Lettres arabes","domaine":"Lettres","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres"],"interets_associes":["social"],"debouches":"Enseignant, journaliste, traducteur","taux_emploi":55},
    {"nom":"Langue française","domaine":"Langues","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres","langues"],"interets_associes":["social","art"],"debouches":"Enseignant, traducteur, journaliste","taux_emploi":52},
    {"nom":"Langue anglaise","domaine":"Langues","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["langues","lettres"],"interets_associes":["social","business"],"debouches":"Traducteur, enseignant, interprète","taux_emploi":60},
    {"nom":"Traduction","domaine":"Langues","duree_annees":3,"moyenne_min":11.0,"series_compatibles":["langues","lettres"],"interets_associes":["social","business"],"debouches":"Traducteur, interprète, journaliste","taux_emploi":58},
    {"nom":"Langue italienne","domaine":"Langues","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["langues","lettres"],"interets_associes":["social","business"],"debouches":"Traducteur, import-export Italie","taux_emploi":55},
    {"nom":"Agronomie","domaine":"Agriculture","duree_annees":5,"moyenne_min":11.5,"series_compatibles":["sciences"],"interets_associes":["agri","sciences"],"debouches":"Ingénieur agronome, INRA","taux_emploi":65},
    {"nom":"Sciences vétérinaires","domaine":"Agriculture","duree_annees":5,"moyenne_min":13.0,"series_compatibles":["sciences"],"interets_associes":["agri","sante","sciences"],"debouches":"Vétérinaire, inspecteur","taux_emploi":78},
    {"nom":"Sciences islamiques","domaine":"Sciences religieuses","duree_annees":4,"moyenne_min":10.0,"series_compatibles":["lettres"],"interets_associes":["social"],"debouches":"Enseignant, imam, conseiller","taux_emploi":60},
    {"nom":"Histoire","domaine":"Sciences humaines","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres"],"interets_associes":["social"],"debouches":"Enseignant, chercheur, journaliste","taux_emploi":50},
    {"nom":"Philosophie","domaine":"Sciences humaines","duree_annees":3,"moyenne_min":10.0,"series_compatibles":["lettres"],"interets_associes":["social"],"debouches":"Enseignant, écrivain","taux_emploi":48},
    {"nom":"Entrepreneuriat artistique","domaine":"Arts","duree_annees":3,"moyenne_min":10.5,"series_compatibles":["lettres","gestion"],"interets_associes":["art","business"],"debouches":"Entrepreneur culturel, producteur","taux_emploi":55},
]


@router.post("/seed")
async def seed_database(db: AsyncSession = Depends(get_db)):
    # Nettoyage
    await db.execute(text("DELETE FROM offres"))
    await db.execute(text("DELETE FROM universites"))
    await db.execute(text("DELETE FROM filieres"))
    await db.execute(text("DELETE FROM wilayas"))
    await db.commit()

    # Wilayas
    for w in WILAYAS:
        db.add(Wilaya(id=w[0], nom=w[1], code=w[2], region=w[3]))
    await db.commit()

    # Filières
    filiere_map = {}
    for f in FILIERES_DATA:
        fid = uuid.uuid4()
        db.add(Filiere(id=fid, **f))
        filiere_map[f["nom"]] = fid
    await db.commit()

    # Universités + Offres
    annee = 2026
    nb_offres = 0
    for u in UNIVERSITES_DATA:
        uid = uuid.uuid4()
        wilaya_data = next((w for w in WILAYAS if w[0] == u["wilaya_id"]), None)
        db.add(Universite(
            id=uid, nom=u["nom"], wilaya_id=u["wilaya_id"],
            type=u["type"], latitude=u["lat"], longitude=u["lng"]
        ))
        await db.flush()
        for nom_filiere in u["filieres"]:
            if nom_filiere in filiere_map:
                moy = u["moyennes"].get(nom_filiere, 12.0)
                db.add(Offre(
                    id=uuid.uuid4(), universite_id=uid,
                    filiere_id=filiere_map[nom_filiere],
                    annee=annee, capacite=100, moyenne_derniere=moy
                ))
                nb_offres += 1
    await db.commit()

    return {
        "status": "ok",
        "wilayas": len(WILAYAS),
        "universites": len(UNIVERSITES_DATA),
        "filieres": len(FILIERES_DATA),
        "offres": nb_offres
    }
