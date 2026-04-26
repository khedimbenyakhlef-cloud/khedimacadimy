"""
Service de matching - Algorithme d'orientation universitaire
Score sur 100 points + bonus proximité géographique :
  - Compatibilité de série      : 35 pts
  - Correspondance d'intérêts   : 30 pts
  - Marge sur la moyenne        : 25 pts
  - Taux d'emploi               : 10 pts
  - Bonus proximité             : +10 pts (bonus, pas pénalité)
"""
from dataclasses import dataclass, field
from typing import List, Optional
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.filiere import Filiere
from models.recommandation import Offre, Universite, Wilaya


@dataclass
class ProfilEtudiant:
    moyenne: float
    serie: str
    interets: List[str]
    wilaya_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class ResultatMatch:
    offre_id: str
    filiere_nom: str
    universite_nom: str
    wilaya_nom: str
    score: float
    score_serie: float
    score_interets: float
    score_moyenne: float
    score_emploi: float
    score_proximite: float
    distance_km: Optional[float]
    rang: int
    accessible: bool
    confortable: bool


def haversine(lat1, lng1, lat2, lng2) -> float:
    """Calcule la distance en km entre deux points GPS."""
    R = 6371.0
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# Coordonnées GPS des wilayas (centre)
WILAYA_COORDS = {
    1:(27.8741,0.2822), 2:(36.1647,1.3317), 3:(33.8000,2.8667),
    4:(35.8833,7.1167), 5:(35.5561,6.1744), 6:(36.7508,5.0564),
    7:(34.8500,5.7333), 8:(31.6167,-2.2167), 9:(36.4800,2.8289),
    10:(36.3731,3.9003), 11:(22.7850,5.5228), 12:(35.4042,8.1244),
    13:(34.8828,-1.3167), 14:(35.3706,1.3214), 15:(36.7169,4.0497),
    16:(36.7372,3.0869), 17:(34.6731,3.2631), 18:(36.8222,5.7656),
    19:(36.1898,5.4103), 20:(34.8306,0.1542), 21:(36.8761,6.9064),
    22:(35.1897,-0.6306), 23:(36.9000,7.7667), 24:(36.4617,7.4328),
    25:(36.3650,6.6147), 26:(36.2642,2.7542), 27:(35.9317,0.0892),
    28:(35.7064,4.5444), 29:(35.3958,0.1408), 30:(31.9492,5.3239),
    31:(35.6969,-0.6331), 32:(33.6831,1.0069), 33:(26.5000,8.4833),
    34:(36.0736,4.7633), 35:(36.7667,3.4667), 36:(36.7678,8.3133),
    37:(27.6744,-8.1472), 38:(35.6075,1.8136), 39:(33.3678,6.8536),
    40:(35.4292,7.1439), 41:(36.2864,7.9514), 42:(36.5881,2.4475),
    43:(36.4503,6.2636), 44:(36.2572,1.9658), 45:(33.2672,-0.3156),
    46:(35.2989,-1.1408), 47:(32.4908,3.6739), 48:(35.7381,0.5564),
    49:(29.2639,0.2311), 50:(21.3333,0.9500), 51:(34.4167,5.0667),
    52:(30.1289,-2.1603), 53:(27.1967,2.4797), 54:(19.5667,5.7667),
    55:(33.1000,6.0667), 56:(24.5500,9.4833), 57:(33.9500,5.9167),
    58:(30.5833,2.8833),
}


class MatcherService:

    POIDS_SERIE = 35
    POIDS_INTERETS = 30
    POIDS_MOYENNE = 25
    POIDS_EMPLOI = 10
    BONUS_PROXIMITE = 10  # bonus max pour proximité

    async def calculer_recommendations(
        self,
        profil: ProfilEtudiant,
        db: AsyncSession,
        annee: int,
        top_n: int = 10,
    ) -> List[ResultatMatch]:

        # Résoudre les coordonnées du bachelier
        lat_etudiant, lng_etudiant = self._get_coords_etudiant(profil)

        offres = await self._charger_offres(db, annee, profil.moyenne)
        resultats = []

        for offre, filiere, universite in offres:
            score_base = self._scorer(profil, filiere)
            if score_base < 20:
                continue

            # Score proximité
            score_prox, distance = self._score_proximite(
                lat_etudiant, lng_etudiant, universite
            )

            score_total = score_base + score_prox
            marge = profil.moyenne - float(filiere.moyenne_min)
            wilaya_nom = universite.wilaya.nom if universite.wilaya else ""

            resultats.append(ResultatMatch(
                offre_id=str(offre.id),
                filiere_nom=filiere.nom,
                universite_nom=universite.nom,
                wilaya_nom=wilaya_nom,
                score=round(score_total, 2),
                score_serie=round(self._score_serie(profil.serie, filiere), 2),
                score_interets=round(self._score_interets(profil.interets, filiere), 2),
                score_moyenne=round(self._score_moyenne(profil.moyenne, filiere), 2),
                score_emploi=round(self._score_emploi(filiere), 2),
                score_proximite=round(score_prox, 2),
                distance_km=round(distance, 1) if distance is not None else None,
                rang=0,
                accessible=marge >= 0,
                confortable=marge >= 1.5,
            ))

        resultats.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(resultats[:top_n], start=1):
            r.rang = i

        return resultats[:top_n]

    def _get_coords_etudiant(self, profil: ProfilEtudiant):
        """Récupère les coordonnées GPS du bachelier."""
        if profil.latitude and profil.longitude:
            return profil.latitude, profil.longitude
        if profil.wilaya_id and profil.wilaya_id in WILAYA_COORDS:
            return WILAYA_COORDS[profil.wilaya_id]
        return None, None

    def _score_proximite(self, lat, lng, universite) -> tuple:
        """Calcule le bonus de proximité (0 à 10 pts)."""
        if lat is None or lng is None:
            return 5.0, None  # score neutre si pas de localisation

        univ_lat = float(universite.latitude) if universite.latitude else None
        univ_lng = float(universite.longitude) if universite.longitude else None

        if univ_lat is None or univ_lng is None:
            return 5.0, None

        distance = haversine(lat, lng, univ_lat, univ_lng)

        # Bonus dégressif :
        # 0-50 km   → 10 pts (même wilaya / très proche)
        # 50-200 km → 7 pts
        # 200-500 km→ 4 pts
        # +500 km   → 1 pt
        if distance <= 50:
            bonus = self.BONUS_PROXIMITE
        elif distance <= 200:
            bonus = 7.0
        elif distance <= 500:
            bonus = 4.0
        else:
            bonus = 1.0

        return bonus, distance

    def _scorer(self, profil, filiere) -> float:
        if profil.moyenne < float(filiere.moyenne_min):
            return 0.0
        return (
            self._score_serie(profil.serie, filiere)
            + self._score_interets(profil.interets, filiere)
            + self._score_moyenne(profil.moyenne, filiere)
            + self._score_emploi(filiere)
        )

    def _score_serie(self, serie, filiere) -> float:
        if not filiere.series_compatibles:
            return self.POIDS_SERIE * 0.5
        return self.POIDS_SERIE if serie in filiere.series_compatibles else 0.0

    def _score_interets(self, interets, filiere) -> float:
        if not interets or not filiere.interets_associes:
            return 0.0
        matches = len(set(interets) & set(filiere.interets_associes))
        return self.POIDS_INTERETS * min(
            matches / max(len(filiere.interets_associes), 1), 1.0
        )

    def _score_moyenne(self, moyenne, filiere) -> float:
        marge = moyenne - float(filiere.moyenne_min)
        return self.POIDS_MOYENNE * min(marge / 4.0, 1.0)

    def _score_emploi(self, filiere) -> float:
        if filiere.taux_emploi is None:
            return self.POIDS_EMPLOI * 0.5
        return self.POIDS_EMPLOI * (filiere.taux_emploi / 100.0)

    async def _charger_offres(self, db, annee, moyenne_etudiant):
        stmt = (
            select(Offre, Filiere, Universite)
            .join(Filiere, Offre.filiere_id == Filiere.id)
            .join(Universite, Offre.universite_id == Universite.id)
            .options(
                joinedload(Offre.universite).joinedload(Universite.wilaya)
            )
            .where(Offre.annee == annee)
            .where(Filiere.moyenne_min <= moyenne_etudiant + 0.5)
        )
        result = await db.execute(stmt)
        return result.unique().all()
