from sqlalchemy import Column, String, Numeric, SmallInteger, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class Filiere(Base):
    __tablename__ = "filieres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(150), nullable=False)
    domaine = Column(String(80), nullable=False)
    duree_annees = Column(SmallInteger, nullable=False)
    moyenne_min = Column(Numeric(4, 2), nullable=False)
    series_compatibles = Column(ARRAY(Text), nullable=False, default=[])
    interets_associes = Column(ARRAY(Text), nullable=False, default=[])
    debouches = Column(Text)
    taux_emploi = Column(SmallInteger)  # pourcentage 0-100
    description = Column(Text)

    offres = relationship("Offre", back_populates="filiere")
    temoignages = relationship("Temoignage", back_populates="filiere")

    def __repr__(self):
        return f"<Filiere {self.nom}>"
