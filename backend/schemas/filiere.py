from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class FiliereRead(BaseModel):
    id: UUID
    nom: str
    domaine: str
    duree_annees: int
    moyenne_min: float
    series_compatibles: List[str]
    interets_associes: List[str]
    debouches: Optional[str]
    taux_emploi: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True


class FiliereCreate(BaseModel):
    nom: str
    domaine: str
    duree_annees: int
    moyenne_min: float
    series_compatibles: List[str] = []
    interets_associes: List[str] = []
    debouches: Optional[str] = None
    taux_emploi: Optional[int] = None
    description: Optional[str] = None


class OffreRead(BaseModel):
    id: UUID
    filiere: FiliereRead
    universite_nom: str
    wilaya_nom: str
    capacite: Optional[int]
    annee: int
    moyenne_derniere: Optional[float]

    class Config:
        from_attributes = True
