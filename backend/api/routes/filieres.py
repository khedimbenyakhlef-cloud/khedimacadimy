from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from db.session import get_db
from models.filiere import Filiere
from models.recommandation import Temoignage, Offre, Universite
from schemas.filiere import FiliereRead
from core.security import get_current_user
from models.user import Utilisateur
from pydantic import BaseModel, Field
from uuid import UUID

router = APIRouter(prefix="/filieres", tags=["filières"])


@router.get("/", response_model=List[FiliereRead])
async def lister_filieres(
    domaine: Optional[str] = Query(None, description="Filtrer par domaine"),
    moyenne_min: Optional[float] = Query(None, description="Filières accessibles dès cette moyenne"),
    db: AsyncSession = Depends(get_db),
):
    """Liste toutes les filières avec filtres optionnels."""
    stmt = select(Filiere)
    if domaine:
        stmt = stmt.where(Filiere.domaine.ilike(f"%{domaine}%"))
    if moyenne_min is not None:
        stmt = stmt.where(Filiere.moyenne_min <= moyenne_min)
    stmt = stmt.order_by(Filiere.nom)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{filiere_id}", response_model=FiliereRead)
async def detail_filiere(filiere_id: UUID, db: AsyncSession = Depends(get_db)):
    """Détail complet d'une filière."""
    result = await db.execute(select(Filiere).where(Filiere.id == filiere_id))
    filiere = result.scalar_one_or_none()
    if not filiere:
        raise HTTPException(status_code=404, detail="Filière introuvable")
    return filiere


@router.get("/{filiere_id}/universites")
async def universites_par_filiere(
    filiere_id: UUID,
    annee: int = Query(2025),
    db: AsyncSession = Depends(get_db),
):
    """Liste les universités qui proposent cette filière."""
    stmt = (
        select(Offre, Universite)
        .join(Universite, Offre.universite_id == Universite.id)
        .where(Offre.filiere_id == filiere_id)
        .where(Offre.annee == annee)
        .order_by(Universite.nom)
    )
    result = await db.execute(stmt)
    rows = result.fetchall()

    return [
        {
            "universite_id": str(u.id),
            "nom": u.nom,
            "wilaya": u.wilaya.nom if u.wilaya else None,
            "capacite": o.capacite,
            "moyenne_derniere": float(o.moyenne_derniere) if o.moyenne_derniere else None,
            "latitude": float(u.latitude) if u.latitude else None,
            "longitude": float(u.longitude) if u.longitude else None,
        }
        for o, u in rows
    ]


class TemoignageCreate(BaseModel):
    contenu: str = Field(..., min_length=50, max_length=2000)
    note: int = Field(..., ge=1, le=5)


@router.post("/{filiere_id}/temoignages", status_code=201)
async def ajouter_temoignage(
    filiere_id: UUID,
    data: TemoignageCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Ajoute un témoignage étudiant sur une filière (nécessite d'être connecté)."""
    filiere_res = await db.execute(select(Filiere).where(Filiere.id == filiere_id))
    if not filiere_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Filière introuvable")

    temoignage = Temoignage(
        utilisateur_id=current_user.id,
        filiere_id=filiere_id,
        contenu=data.contenu,
        note=data.note,
        approuve=False,
    )
    db.add(temoignage)
    await db.commit()
    return {"message": "Témoignage soumis, en attente de validation."}


@router.get("/{filiere_id}/temoignages")
async def lire_temoignages(filiere_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retourne les témoignages approuvés d'une filière."""
    stmt = (
        select(Temoignage)
        .where(Temoignage.filiere_id == filiere_id)
        .where(Temoignage.approuve == True)
        .order_by(Temoignage.created_at.desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    temos = result.scalars().all()

    note_avg_stmt = (
        select(func.avg(Temoignage.note))
        .where(Temoignage.filiere_id == filiere_id)
        .where(Temoignage.approuve == True)
    )
    avg_result = await db.execute(note_avg_stmt)
    note_moyenne = avg_result.scalar()

    return {
        "note_moyenne": round(float(note_moyenne), 1) if note_moyenne else None,
        "total": len(temos),
        "temoignages": [
            {
                "id": str(t.id),
                "contenu": t.contenu,
                "note": t.note,
                "date": t.created_at.isoformat() if t.created_at else None,
            }
            for t in temos
        ],
    }
