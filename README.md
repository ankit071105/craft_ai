# Hackathon: Hyper-Local E‑Commerce (Full Stack)

- **Backend:** FastAPI + SQLite + SQLAlchemy + scikit-learn (TF‑IDF)
- **Frontend:** React + Vite + Tailwind + React Router + Axios + Leaflet
- **Features:**
  - First-time user flow: ask location via browser, allow pin-adjust on a map, create **guest session**.
  - Recommendations by location for new users; hybrid personalization as they interact.
  - Log **view / click / wishlist / cart / purchase** interactions.
  - Ask for **feedback** (1–5 rating + comment) per product to improve future work.
  - Nearby products by radius.
  - Seed script with Indian cities and craft products.

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Seed demo data:
```bash
python -m app.seed
```

## Run frontend
```bash
cd frontend
npm i
npm run dev
```
Set `VITE_API_BASE` in `frontend/.env` if your backend runs on a different URL (default http://127.0.0.1:8000).
