from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.session import get_db
from models.user import Utilisateur, ProfilBac
from schemas.user import UtilisateurCreate, UtilisateurRead, TokenResponse, ProfilBacCreate, ProfilBacRead, UtilisateurUpdate
from core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["utilisateurs"])


@router.post("/inscription", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def inscrire(data: UtilisateurCreate, db: AsyncSession = Depends(get_db)):
    """Inscription d'un nouveau bachelier."""
    existing = await db.execute(select(Utilisateur).where(Utilisateur.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user = Utilisateur(
        nom=data.nom,
        prenom=data.prenom,
        email=data.email,
        hashed_password=hash_password(data.password),
        num_dossier_bac=data.num_dossier_bac,
        wilaya_id=data.wilaya_id,
    )
    db.add(user)
    await db.flush()  # obtenir l'id avant commit

    token = create_access_token({"sub": str(user.id)})
    await db.commit()
    await db.refresh(user)

    return TokenResponse(access_token=token, utilisateur=user)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Connexion avec email + mot de passe."""
    result = await db.execute(select(Utilisateur).where(Utilisateur.email == form.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Compte désactivé")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, utilisateur=user)


@router.get("/moi", response_model=UtilisateurRead)
async def mon_profil(current_user: Utilisateur = Depends(get_current_user)):
    """Retourne le profil de l'utilisateur connecté."""
    return current_user


@router.put("/moi", response_model=UtilisateurRead)
async def modifier_profil(
    data: UtilisateurUpdate,
    current_user: Utilisateur = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/moi/profil-bac", response_model=ProfilBacRead, status_code=201)
async def creer_profil_bac(
    data: ProfilBacCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Crée ou met à jour le profil bac de l'utilisateur."""
    if current_user.profil:
        for field, value in data.model_dump().items():
            setattr(current_user.profil, field, value)
        profil = current_user.profil
    else:
        profil = ProfilBac(utilisateur_id=current_user.id, **data.model_dump())
        db.add(profil)

    await db.commit()
    await db.refresh(profil)
    return profil
