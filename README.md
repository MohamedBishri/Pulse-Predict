# PulsePredict — Explainable Disease Prediction Platform

PulsePredict is a polished, bilingual, full-stack hackathon prototype for explainable heart-disease risk screening.

## Product features
- Premium responsive Arabic/English UI
- Registration and login with hashed passwords and JWT
- Guided heart-risk assessment from nine inputs
- Probability plus Low / Moderate / High risk level
- Explainable top contributing factors
- Personalized recommendations and urgent-symptom guidance
- Prediction history
- Printable result report
- Model Lab with Accuracy, Precision, Recall, F1 and AUC
- Admin statistics dashboard
- One-click demo data for live judging
- Docker Compose startup

## Run with Docker
```bash
docker compose up --build
```
Open:
- App: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

The first registered account becomes Admin.

## Run without Docker
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Main API routes
- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`
- `POST /predictions`
- `GET /predictions`
- `GET /model/info`
- `GET /admin/stats`
- `GET /health`

## Important scientific statement
The packaged model uses synthetic demonstration data to make the prototype run immediately. It is not clinically validated and must not be used for diagnosis or real treatment decisions. A production version requires an approved clinical dataset, external validation, calibration, subgroup fairness evaluation, security review, and regulatory assessment.

## Presentation files
- `HACKATHON_PITCH.md`
- `DEMO_SCRIPT.md`
- `JUDGING_GUIDE.md`
