"""
Scraper du site MESRS pour synchroniser les filières et offres chaque année.
Lancer manuellement : python -m app.services.scraper
Ou via Celery : celery -A app.tasks worker
"""
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from app.core.config import settings


class MESRSScraper:
    BASE_URL = settings.MESRS_BASE_URL
    HEADERS = {
        "User-Agent": "OrientationDZ-Bot/1.0 (contact: admin@orientation-dz.dz)",
    }

    async def scraper_filieres(self) -> List[Dict]:
        """
        Scrape la liste des filières disponibles sur le site MESRS.
        Retourne une liste de dicts normalisés.
        """
        async with httpx.AsyncClient(headers=self.HEADERS, timeout=30) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/fr/formations")
                resp.raise_for_status()
            except httpx.HTTPError as e:
                print(f"[MESRS Scraper] Erreur HTTP : {e}")
                return self._donnees_fallback()

            soup = BeautifulSoup(resp.text, "html.parser")
            return self._parser_filieres(soup)

    def _parser_filieres(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse le HTML du MESRS — à adapter selon la structure réelle du site."""
        filieres = []
        # Exemple de parsing — adapter aux sélecteurs réels du site MESRS
        for row in soup.select("table.formations tr"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            filieres.append({
                "nom": cells[0].get_text(strip=True),
                "domaine": cells[1].get_text(strip=True),
                "duree_annees": self._extraire_duree(cells[2].get_text(strip=True)),
                "moyenne_min": self._extraire_moyenne(cells[3].get_text(strip=True)),
            })
        return filieres

    def _extraire_duree(self, texte: str) -> int:
        import re
        match = re.search(r"(\d+)", texte)
        return int(match.group(1)) if match else 5

    def _extraire_moyenne(self, texte: str) -> float:
        import re
        match = re.search(r"(\d+[.,]\d+)", texte)
        if match:
            return float(match.group(1).replace(",", "."))
        return 10.0

    def _donnees_fallback(self) -> List[Dict]:
        """Données statiques en cas d'échec du scraping."""
        print("[MESRS Scraper] Utilisation des données fallback.")
        return [
            {"nom": "Médecine", "domaine": "Santé", "duree_annees": 7, "moyenne_min": 16.0},
            {"nom": "Génie informatique", "domaine": "Informatique", "duree_annees": 5, "moyenne_min": 14.0},
            {"nom": "Droit", "domaine": "Droit", "duree_annees": 4, "moyenne_min": 12.0},
        ]

    async def scraper_universites(self) -> List[Dict]:
        """Scrape la liste des universités algériennes avec leurs wilayas."""
        async with httpx.AsyncClient(headers=self.HEADERS, timeout=30) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/fr/etablissements")
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                return self._parser_universites(soup)
            except httpx.HTTPError:
                return []

    def _parser_universites(self, soup: BeautifulSoup) -> List[Dict]:
        universites = []
        for bloc in soup.select(".etablissement-card"):
            universites.append({
                "nom": bloc.select_one(".nom")?.get_text(strip=True) or "",
                "wilaya_code": bloc.select_one(".wilaya")?.get_text(strip=True) or "",
                "type": bloc.select_one(".type")?.get_text(strip=True) or "univ",
                "site_web": bloc.select_one("a")?.get("href", ""),
            })
        return universites


async def main():
    scraper = MESRSScraper()
    print("Scraping des filières MESRS...")
    filieres = await scraper.scraper_filieres()
    print(f"{len(filieres)} filières récupérées.")
    for f in filieres[:3]:
        print(f"  - {f['nom']} ({f['domaine']}, {f['duree_annees']} ans)")


if __name__ == "__main__":
    asyncio.run(main())
