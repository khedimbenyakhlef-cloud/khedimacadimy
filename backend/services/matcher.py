"""
Service de matching - Algorithme d'orientation universitaire
Score sur 100 points répartis en 4 critères :
  - Compatibilité de série      : 35 pts
  - Correspondance d'intérêts   : 30 pts
  - Marge sur la moyenne        : 25 pts
  - Taux d'emploi               : 10 pts
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
    accessible: bool  # moyenne >= moyenne_min
    confortable: bool  # marge >= 1.5 point


class MatcherService:

    POIDS_SERIE = 35
    POIDS_INTERETS = 30
    POIDS_MOYENNE = 25
    POIDS_EMPLOI = 10

    async def calculer_recommendations(
        self,
        profil: ProfilEtudiant,
        db: AsyncSession,
        annee: int,
        top_n: int = 10,
    ) -> List[ResultatMatch]:
        offres = await self._charger_offres(db, annee, profil.moyenne)
        resultats = []

        for offre, filiere, universite in offres:
            score_total = self._scorer(profil, filiere)
            if score_total < 20:
                continue

            marge = profil.moyenne - float(filiere.moyenne_min)
            resultats.append(ResultatMatch(
                offre_id=str(offre.id),
                filiere_nom=filiere.nom,
                universite_nom=universite.nom,
                wilaya_nom=universite.wilaya.nom if universite.wilaya else "",
                score=round(score_total, 2),
                score_serie=round(self._score_serie(profil.serie, filiere), 2),
                score_interets=round(self._score_interets(profil.interets, filiere), 2),
                score_moyenne=round(self._score_moyenne(profil.moyenne, filiere), 2),
                score_emploi=round(self._score_emploi(filiere), 2),
                rang=0,
                accessible=marge >= 0,
                confortable=marge >= 1.5,
            ))

        resultats.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(resultats[:top_n], start=1):
            r.rang = i

        return resultats[:top_n]

    def _scorer(self, profil: ProfilEtudiant, filiere: Filiere) -> float:
        if profil.moyenne < float(filiere.moyenne_min):
            return 0.0
        return (
            self._score_serie(profil.serie, filiere)
            + self._score_interets(profil.interets, filiere)
            + self._score_moyenne(profil.moyenne, filiere)
            + self._score_emploi(filiere)
        )

    def _score_serie(self, serie: str, filiere: Filiere) -> float:
        if not filiere.series_compatibles:
            return self.POIDS_SERIE * 0.5
        return self.POIDS_SERIE if serie in filiere.series_compatibles else 0.0

    def _score_interets(self, interets: List[str], filiere: Filiere) -> float:
        if not interets or not filiere.interets_associes:
            return 0.0
        matches = len(set(interets) & set(filiere.interets_associes))
        max_possible = max(len(filiere.interets_associes), 1)
        return self.POIDS_INTERETS * min(matches / max_possible, 1.0)

    def _score_moyenne(self, moyenne: float, filiere: Filiere) -> float:
        marge = moyenne - float(filiere.moyenne_min)
        # Plus la marge est grande, meilleur le score (plafonné à 4 points de marge)
        facteur = min(marge / 4.0, 1.0)
        return self.POIDS_MOYENNE * facteur

    def _score_emploi(self, filiere: Filiere) -> float:
        if filiere.taux_emploi is None:
            return self.POIDS_EMPLOI * 0.5
        return self.POIDS_EMPLOI * (filiere.taux_emploi / 100.0)

    async def _charger_offres(
        self, db: AsyncSession, annee: int, moyenne_etudiant: float
    ):
        stmt = (
            select(Offre, Filiere, Universite)
            .join(Filiere, Offre.filiere_id == Filiere.id)
            .join(Universite, Offre.universite_id == Universite.id)
            .where(Offre.annee == annee)
            .where(Filiere.moyenne_min <= moyenne_etudiant + 0.5)  # +0.5 marge pour montrer les "presque"
        )
        result = await db.execute(stmt)
        return result.fetchall()
