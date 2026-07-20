import json
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import Prediction, User
from .schemas import AdminStats, LoginIn, PredictionIn, PredictionOut, RegisterIn, TokenOut, UserOut
from .security import admin_user, create_token, current_user, hash_password, verify_password
from .ml import model_info, predict

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "https://pulse-predict-m5bz1vaes-mohamed-bishri.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/model/info")
def get_model_info(): return model_info()

@app.post("/auth/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    first_user = db.query(User).count() == 0
    user = User(name=data.name.strip(), email=data.email.lower(), password_hash=hash_password(data.password), is_admin=first_user)
    db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_token(user.id))

@app.post("/auth/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return TokenOut(access_token=create_token(user.id))

@app.get("/users/me", response_model=UserOut)
def me(user: User = Depends(current_user)): return user

@app.post("/predictions", response_model=PredictionOut)
def create_prediction(data: PredictionIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    payload = data.model_dump()
    probability, level, factors, recommendations = predict(payload)
    row = Prediction(user_id=user.id, probability=probability, risk_level=level, inputs_json=json.dumps(payload), explanation_json=json.dumps(factors))
    db.add(row); db.commit(); db.refresh(row)
    return PredictionOut(id=row.id, probability=round(probability,4), risk_level=level, factors=factors, recommendations=recommendations, created_at=row.created_at)

@app.get("/predictions", response_model=list[PredictionOut])
def history(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(Prediction).filter(Prediction.user_id == user.id).order_by(Prediction.created_at.desc()).all()
    recommendations = ["Review this result with a clinician when appropriate."]
    return [PredictionOut(id=r.id, probability=round(r.probability,4), risk_level=r.risk_level, factors=json.loads(r.explanation_json), recommendations=recommendations, created_at=r.created_at) for r in rows]

@app.get("/admin/stats", response_model=AdminStats)
def stats(_: User = Depends(admin_user), db: Session = Depends(get_db)):
    users = db.query(User).count(); total = db.query(Prediction).count()
    high = db.query(Prediction).filter(Prediction.risk_level == "High").count()
    avg = db.query(func.avg(Prediction.probability)).scalar() or 0
    return AdminStats(users=users, predictions=total, high_risk=high, average_probability=round(float(avg),4))
