u200B
u200B
 
# EcoTrack (version simple)

API FastAPI + SQLite pour suivre des indicateurs environnementaux (OpenAQ et Open-Meteo). Authentification JWT, rôles user/admin, CRUD de base.

## Installation rapide
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Copie `.env.example` en `.env` puis adapte :
- `JWT_SECRET` secret JWT
- `DATABASE_URL` (par défaut sqlite `./data/ecotrack.db`)

## Lancer l'API
```
uvicorn app.main:app --reload
```
Docs Swagger : http://localhost:8000/docs
Front minimal (HTML/JS) : http://localhost:8000/static/index.html

## Scripts
- Créer un admin : `python -m app.scripts.create_admin --email admin@example.com --username admin --password admin123`
- Seed données de base : `python -m app.scripts.seed`

## Endpoints clés
- Auth : `POST /api/v1/auth/register`, `POST /api/v1/auth/token`
- Zones : `GET /api/v1/zones`, CRUD admin
- Sources : `GET /api/v1/sources`, CRUD admin
- Indicateurs : `GET /api/v1/indicators` avec filtres from/to/zone/type/source, CRUD admin
- Stats simples : `GET /api/v1/stats/average?indicator_type=pm25&zone_id=1`
- Ingestion (admin) :
  - `POST /api/v1/ingest/openaq?zone_id=1` (utilise lat/lon de la zone, nécessite `OPENAQ_API_KEY` v3)
  - `POST /api/v1/ingest/openmeteo?lat=48.85&lon=2.35&zone_id=1&days=3`

## Données externes
- OpenAQ (qualité de l'air, v3 nécessite une clé) : utilise `locations/{id}/latest` autour d'une zone (env `OPENAQ_API_KEY`)
- Open-Meteo (météo) : https://api.open-meteo.com/v1/forecast



