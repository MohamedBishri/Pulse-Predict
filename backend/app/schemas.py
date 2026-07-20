from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    model_config = {"from_attributes": True}

class PredictionIn(BaseModel):
    age: int = Field(ge=18, le=100)
    sex: int = Field(ge=0, le=1, description="0=female, 1=male")
    chest_pain_type: int = Field(ge=0, le=3)
    resting_bp: int = Field(ge=70, le=240)
    cholesterol: int = Field(ge=80, le=700)
    fasting_blood_sugar: int = Field(ge=0, le=1)
    max_heart_rate: int = Field(ge=50, le=230)
    exercise_angina: int = Field(ge=0, le=1)
    oldpeak: float = Field(ge=0, le=8)

class Factor(BaseModel):
    feature: str
    impact: float
    direction: str

class PredictionOut(BaseModel):
    id: int
    probability: float
    risk_level: str
    factors: list[Factor]
    recommendations: list[str]
    created_at: datetime

class AdminStats(BaseModel):
    users: int
    predictions: int
    high_risk: int
    average_probability: float
