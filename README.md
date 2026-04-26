# 🎓 Orientation DZ

> **Fondé par KHEDIM BENYAKHLEF dit Beny-Joe**

Plateforme d'orientation universitaire pour les bacheliers algériens.
Recommandations personnalisées selon la moyenne, la série du bac et les centres d'intérêt.

---

## 📁 Structure du projet

```
orientation_dz_complet/
├── backend/              ← API Python / FastAPI
│   ├── app/
│   │   ├── api/routes/   ← orientation.py, filieres.py, users.py
│   │   ├── core/         ← config.py, security.py (JWT)
│   │   ├── db/           ← session.py, base.py
│   │   ├── models/       ← SQLAlchemy : filiere, user, recommandation
│   │   ├── schemas/      ← Pydantic : validation des données
│   │   ├── services/     ← matcher.py (algo), scraper.py (MESRS)
│   │   └── main.py       ← Point d'entrée FastAPI
│   ├── scripts/
│   │   ├── seed_data.py  ← 48 wilayas + filières de base
│   │   └── 001_init.py   ← Migration Alembic
│   ├── tests/
│   │   └── test_matcher.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/             ← Next.js 14 / TypeScript
│   ├── app/
│   │   ├── page.tsx      ← Accueil (logo + Kinsta + fondateur)
│   │   ├── orientation/  ← Formulaire + résultats
│   │   ├── filieres/     ← Liste + détail filière
│   │   └── auth/         ← Connexion / Inscription
│   ├── components/
│   │   └── layout/       ← Navbar + Footer
│   ├── lib/
│   │   ├── api.ts        ← Client Axios
│   │   └── store.ts      ← Zustand auth
│   └── types/index.ts    ← Types TypeScript
│
├── docker-compose.yml    ← Tout en un commande
└── nginx.conf            ← Reverse proxy production
```

---

## 🚀 Lancer le projet

### 1. Backend

```bash
cd backend

# Installer les dépendances
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configurer la base de données (PostgreSQL requis)
cp .env.example .env   # éditer avec tes paramètres

# Initialiser la BDD
python scripts/seed_data.py

# Lancer l'API
uvicorn app.main:app --reload --port 8000
```

**Docs API :** http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend

npm install
cp .env.example .env.local

npm run dev
```

**App :** http://localhost:3000

### 3. Tout en un avec Docker

```bash
docker-compose up -d
```

---

## ⚙️ Algorithme de matching

Score sur **100 points** :

| Critère | Poids |
|---------|-------|
| Compatibilité de série | 35 pts |
| Correspondance intérêts | 30 pts |
| Marge sur la moyenne min | 25 pts |
| Taux d'emploi filière | 10 pts |

---

## ☁️ Hébergement recommandé

Ce projet est hébergeable sur **Kinsta** — plateforme cloud ultra-rapide
supportant Next.js et Python/FastAPI nativement.

👉 [https://kinsta.com/?kaid=HUFPGOMPMRPI](https://kinsta.com/?kaid=HUFPGOMPMRPI)

---

## 📄 Licence

MIT — Orientation DZ © 2025
Fondé par **KHEDIM BENYAKHLEF dit Beny-Joe**
