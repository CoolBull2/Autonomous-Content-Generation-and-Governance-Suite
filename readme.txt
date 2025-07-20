.venv/scripts/activate
cd content-governance-suite
uvicorn api.main:app --reload

cd content-governance-suite/frontend
npm run dev
@coderabbitai can you create a redme file that documents all my code