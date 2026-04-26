"""
Service de matching - Algorithme d'orientation universitaire
"""
from dataclasses import dataclass
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.filiere import Filiere
from models.recommandation import Offre, Universite


@dataclass
class ProfilEtudiant:
    moyenne: float
    serie: str
    interets: List[str]
    wilaya_id: int | None = None


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
    rang: int
    accessible: bool
    confortable: bool


class MatcherService:
    POIDS_SERIE = 35
    POIDS_INTERETS = 30
    POIDS_MOYENNE = 25
    POIDS_EMPLOI = 10

    async def calculer_recommendations(self, profil, db, annee, top_n=10):
        offres = await self._charger_offres(db, annee, profil.moyenne)
        resultats = []
        for offre, filiere, universite in offres:
            score_total = self._scorer(profil, filiere)
            if score_total < 20:
                continue
            marge = profil.moyenne - float(filiere.moyenne_min)
            wilaya_nom = universite.wilaya.nom if universite.wilaya else ""
            resultats.append(ResultatMatch(
                offre_id=str(offre.id), filiere_nom=filiere.nom,
                universite_nom=universite.nom, wilaya_nom=wilaya_nom,
                score=round(score_total, 2),
                score_serie=round(self._score_serie(profil.serie, filiere), 2),
                score_interets=round(self._score_interets(profil.interets, filiere), 2),
                score_moyenne=round(self._score_moyenne(profil.moyenne, filiere), 2),
                score_emploi=round(self._score_emploi(filiere), 2),
                rang=0, accessible=marge >= 0, confortable=marge >= 1.5,
            ))
        resultats.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(resultats[:top_n], start=1):
            r.rang = i
        return resultats[:top_n]

    def _scorer(self, profil, filiere):
        if profil.moyenne < float(filiere.moyenne_min):
            return 0.0
        return (self._score_serie(profil.serie, filiere)
                + self._score_interets(profil.interets, filiere)
                + self._score_moyenne(profil.moyenne, filiere)
                + self._score_emploi(filiere))

    def _score_serie(self, serie, filiere):
        if not filiere.series_compatibles:
            return self.POIDS_SERIE * 0.5
        return self.POIDS_SERIE if serie in filiere.series_compatibles else 0.0

    def _score_interets(self, interets, filiere):
        if not interets or not filiere.interets_associes:
            return 0.0
        matches = len(set(interets) & set(filiere.interets_associes))
        return self.POIDS_INTERETS * min(matches / max(len(filiere.interets_associes), 1), 1.0)

    def _score_moyenne(self, moyenne, filiere):
        marge = moyenne - float(filiere.moyenne_min)
        return self.POIDS_MOYENNE * min(marge / 4.0, 1.0)

    def _score_emploi(self, filiere):
        if filiere.taux_emploi is None:
            return self.POIDS_EMPLOI * 0.5
        return self.POIDS_EMPLOI * (filiere.taux_emploi / 100.0)

    async def _charger_offres(self, db, annee, moyenne_etudiant):
        stmt = (
            select(Offre, Filiere, Universite)
            .join(Filiere, Offre.filiere_id == Filiere.id)
            .join(Universite, Offre.universite_id == Universite.id)
            .options(joinedload(Offre.universite).joinedload(Universite.wilaya))
            .where(Offre.annee == annee)
            .where(Filiere.moyenne_min <= moyenne_etudiant + 0.5)
        )
        result = await db.execute(stmt)
        return result.unique().all()
