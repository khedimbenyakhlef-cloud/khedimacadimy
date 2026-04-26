from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from pydantic import BaseModel, Field
from typing import List
from db.session import get_db
from services.matcher import MatcherService, ProfilEtudiant

router = APIRouter(prefix="/orientation", tags=["orientation"])
matcher = MatcherService()


class RequeteOrientation(BaseModel):
    moyenne: float = Field(..., ge=0, le=20, description="Moyenne bac sur 20")
    serie: str = Field(..., description="Ex: sciences, maths, technique, lettres, gestion")
    interets: List[str] = Field(default=[], description="Liste d'intérêts")
    wilaya_id: int | None = Field(None, description="Wilaya de préférence")
    top_n: int = Field(default=10, ge=1, le=20)


class ReponseOrientation(BaseModel):
    offre_id: str
    filiere_nom: str
    universite_nom: str
    wilaya_nom: str
    score: float
    rang: int
    accessible: bool
    confortable: bool
    details_score: dict


@router.post("/recommander", response_model=List[ReponseOrientation])
async def recommander(
    requete: RequeteOrientation,
    db: AsyncSession = Depends(get_db),
):
    """
    Calcule les filières recommandées pour un bachelier selon :
    - Sa moyenne
    - Sa série
    - Ses centres d'intérêt
    - Sa wilaya de préférence (optionnel)
    """
    annee_courante = date.today().year
    profil = ProfilEtudiant(
        moyenne=requete.moyenne,
        serie=requete.serie,
        interets=requete.interets,
        wilaya_id=requete.wilaya_id,
    )

    try:
        resultats = await matcher.calculer_recommendations(
            profil=profil,
            db=db,
            annee=annee_courante,
            top_n=requete.top_n,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur matching: {str(e)}")

    if not resultats:
        raise HTTPException(
            status_code=404,
            detail="Aucune filière trouvée pour ce profil. Vérifiez votre moyenne et série.",
        )

    return [
        ReponseOrientation(
            offre_id=r.offre_id,
            filiere_nom=r.filiere_nom,
            universite_nom=r.universite_nom,
            wilaya_nom=r.wilaya_nom,
            score=r.score,
            rang=r.rang,
            accessible=r.accessible,
            confortable=r.confortable,
            details_score={
                "serie": r.score_serie,
                "interets": r.score_interets,
                "moyenne": r.score_moyenne,
                "emploi": r.score_emploi,
            },
        )
        for r in resultats
    ]


@router.get("/series")
async def lister_series():
    """Retourne les séries bac disponibles."""
    return [
        {"code": "sciences", "label": "Sciences de la nature et de la vie"},
        {"code": "maths", "label": "Mathématiques"},
        {"code": "technique", "label": "Technique mathématique"},
        {"code": "lettres", "label": "Lettres et philosophie"},
        {"code": "gestion", "label": "Gestion et économie"},
        {"code": "langues", "label": "Langues étrangères"},
    ]


@router.get("/interets")
async def lister_interets():
    """Retourne les catégories d'intérêt disponibles."""
    return [
        {"code": "tech", "label": "Technologie & informatique"},
        {"code": "sante", "label": "Santé & médecine"},
        {"code": "business", "label": "Business & économie"},
        {"code": "art", "label": "Art & design"},
        {"code": "sciences", "label": "Sciences pures"},
        {"code": "social", "label": "Sciences sociales"},
        {"code": "droit", "label": "Droit & justice"},
        {"code": "agri", "label": "Agriculture & environnement"},
    ]
