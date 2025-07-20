.venv/scripts/activate
cd content-governance-suite
uvicorn api.main:app --reload

cd content-governance-suite/frontend
npm run dev
