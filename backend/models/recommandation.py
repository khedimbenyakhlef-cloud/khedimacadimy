from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.base import Base


class Wilaya(Base):
    __tablename__ = "wilayas"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    code = Column(String(2), nullable=False)
    region = Column(String(50))

    universites = relationship("Universite", back_populates="wilaya")
    utilisateurs = relationship("Utilisateur", back_populates="wilaya")


class Universite(Base):
    __tablename__ = "universites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(200), nullable=False)
    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))
    type = Column(String(20))  # univ, ecole, iut
    site_web = Column(String(255))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))

    wilaya = relationship("Wilaya", back_populates="universites")
    offres = relationship("Offre", back_populates="universite")


class Offre(Base):
    __tablename__ = "offres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    universite_id = Column(UUID(as_uuid=True), ForeignKey("universites.id"))
    filiere_id = Column(UUID(as_uuid=True), ForeignKey("filieres.id"))
    capacite = Column(Integer)
    annee = Column(SmallInteger, nullable=False)
    moyenne_derniere = Column(Numeric(4, 2))  # moyenne du dernier admis

    universite = relationship("Universite", back_populates="offres")
    filiere = relationship("Filiere", back_populates="offres")
    recommendations = relationship("Recommandation", back_populates="offre")


class Recommandation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    offre_id = Column(UUID(as_uuid=True), ForeignKey("offres.id"))
    score = Column(Numeric(5, 2))
    rang = Column(SmallInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    utilisateur = relationship("Utilisateur", back_populates="recommendations")
    offre = relationship("Offre", back_populates="recommendations")


class Temoignage(Base):
    __tablename__ = "temoignages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    filiere_id = Column(UUID(as_uuid=True), ForeignKey("filieres.id"))
    contenu = Column(Text, nullable=False)
    note = Column(SmallInteger)  # 1-5
    approuve = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    utilisateur = relationship("Utilisateur", back_populates="temoignages")
    filiere = relationship("Filiere", back_populates="temoignages")
