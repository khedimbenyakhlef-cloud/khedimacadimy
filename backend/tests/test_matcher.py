"""
Tests unitaires pour le service de matching
Lancer avec : pytest tests/test_matcher.py -v
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.matcher import MatcherService, ProfilEtudiant
from app.models.filiere import Filiere


@pytest.fixture
def matcher():
    return MatcherService()


@pytest.fixture
def filiere_info():
    f = MagicMock(spec=Filiere)
    f.nom = "Génie informatique"
    f.moyenne_min = 14.0
    f.series_compatibles = ["sciences", "maths"]
    f.interets_associes = ["tech", "sciences"]
    f.taux_emploi = 88
    return f


class TestScoreSerie:
    def test_serie_compatible(self, matcher, filiere_info):
        score = matcher._score_serie("sciences", filiere_info)
        assert score == matcher.POIDS_SERIE

    def test_serie_incompatible(self, matcher, filiere_info):
        score = matcher._score_serie("lettres", filiere_info)
        assert score == 0.0

    def test_serie_vide(self, matcher, filiere_info):
        filiere_info.series_compatibles = []
        score = matcher._score_serie("sciences", filiere_info)
        assert score == matcher.POIDS_SERIE * 0.5


class TestScoreInterets:
    def test_correspondance_totale(self, matcher, filiere_info):
        score = matcher._score_interets(["tech", "sciences"], filiere_info)
        assert score == matcher.POIDS_INTERETS

    def test_correspondance_partielle(self, matcher, filiere_info):
        score = matcher._score_interets(["tech", "sante"], filiere_info)
        assert 0 < score < matcher.POIDS_INTERETS

    def test_aucun_interet(self, matcher, filiere_info):
        score = matcher._score_interets([], filiere_info)
        assert score == 0.0


class TestScoreMoyenne:
    def test_marge_grande(self, matcher, filiere_info):
        # moy 18 vs min 14 → marge 4 → score max
        score = matcher._score_moyenne(18.0, filiere_info)
        assert score == matcher.POIDS_MOYENNE

    def test_marge_faible(self, matcher, filiere_info):
        # moy 14.5 vs min 14 → marge 0.5
        score = matcher._score_moyenne(14.5, filiere_info)
        assert score < matcher.POIDS_MOYENNE

    def test_marge_nulle(self, matcher, filiere_info):
        score = matcher._score_moyenne(14.0, filiere_info)
        assert score == 0.0


class TestScorerGlobal:
    def test_profil_excellent(self, matcher, filiere_info):
        profil = ProfilEtudiant(moyenne=18.0, serie="sciences", interets=["tech", "sciences"])
        score = matcher._scorer(profil, filiere_info)
        assert score >= 90

    def test_profil_insuffisant(self, matcher, filiere_info):
        profil = ProfilEtudiant(moyenne=12.0, serie="sciences", interets=["tech"])
        score = matcher._scorer(profil, filiere_info)
        assert score == 0.0  # moyenne < min → rejeté

    def test_profil_moyen(self, matcher, filiere_info):
        profil = ProfilEtudiant(moyenne=15.0, serie="lettres", interets=["tech"])
        score = matcher._scorer(profil, filiere_info)
        assert 0 < score < 100
