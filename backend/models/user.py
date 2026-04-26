from sqlalchemy import Column, String, SmallInteger, Boolean, ForeignKey, Integer, Numeric, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    num_dossier_bac = Column(String(20), unique=True, index=True)
    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))
    is_active = Column(Boolean, default=True)

    profil = relationship("ProfilBac", back_populates="utilisateur", uselist=False)
    recommendations = relationship("Recommandation", back_populates="utilisateur")
    temoignages = relationship("Temoignage", back_populates="utilisateur")
    wilaya = relationship("Wilaya", back_populates="utilisateurs")


class ProfilBac(Base):
    __tablename__ = "profils_bac"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"), unique=True)
    serie = Column(String(50), nullable=False)
    moyenne = Column(Numeric(4, 2), nullable=False)
    annee_bac = Column(SmallInteger)
    interets = Column(ARRAY(Text), default=[])

    utilisateur = relationship("Utilisateur", back_populates="profil")
