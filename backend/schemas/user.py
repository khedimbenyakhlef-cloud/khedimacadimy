from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID


class ProfilBacCreate(BaseModel):
    serie: str
    moyenne: float = Field(..., ge=0, le=20)
    annee_bac: Optional[int] = None
    interets: List[str] = []


class ProfilBacRead(ProfilBacCreate):
    id: UUID

    class Config:
        from_attributes = True


class UtilisateurCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    num_dossier_bac: Optional[str] = None
    wilaya_id: Optional[int] = None


class UtilisateurRead(BaseModel):
    id: UUID
    nom: str
    prenom: str
    email: str
    num_dossier_bac: Optional[str]
    wilaya_id: Optional[int]
    profil: Optional[ProfilBacRead]

    class Config:
        from_attributes = True


class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    wilaya_id: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    utilisateur: UtilisateurRead
