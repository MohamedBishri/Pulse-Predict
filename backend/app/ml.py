from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from .config import settings

FEATURES = ["age","sex","chest_pain_type","resting_bp","cholesterol","fasting_blood_sugar","max_heart_rate","exercise_angina","oldpeak"]
LABELS = {
    "age":"Age", "sex":"Sex", "chest_pain_type":"Chest pain pattern", "resting_bp":"Resting blood pressure",
    "cholesterol":"Cholesterol", "fasting_blood_sugar":"Fasting blood sugar", "max_heart_rate":"Maximum heart rate",
    "exercise_angina":"Exercise-induced angina", "oldpeak":"ST depression (oldpeak)"
}

MODEL_METRICS = []

def _dataset(seed=42, n=6000):
    rng = np.random.default_rng(seed)
    age = rng.integers(18, 91, n); sex = rng.integers(0, 2, n); cp = rng.integers(0, 4, n)
    bp = np.clip(rng.normal(130, 22, n), 80, 230); chol = np.clip(rng.normal(235, 55, n), 90, 650)
    fbs = rng.binomial(1, .18, n); mhr = np.clip(rng.normal(155 - .45*(age-45), 22, n), 55, 220)
    angina = rng.binomial(1, np.clip(.12 + (age-40)/180, .05, .55), n); oldpeak = np.clip(rng.gamma(1.4, .8, n), 0, 7)
    X = np.column_stack([age,sex,cp,bp,chol,fbs,mhr,angina,oldpeak])
    logit = -8 + .055*age + .35*sex + .28*cp + .012*(bp-120) + .004*(chol-200) + .45*fbs - .018*(mhr-140) + 1.15*angina + .7*oldpeak
    y = rng.binomial(1, 1/(1+np.exp(-logit)))
    return X, y

def _train_models(path: str):
    global MODEL_METRICS
    X, y = _dataset(); Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.22, random_state=42, stratify=y)
    models = {
        "Logistic Regression": Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1200))]),
        "Random Forest": RandomForestClassifier(n_estimators=180, max_depth=9, random_state=42, class_weight="balanced"),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    }
    fitted = {}
    for name, model in models.items():
        model.fit(Xtr, ytr); fitted[name] = model
        prob = model.predict_proba(Xte)[:,1]; pred = (prob >= .5).astype(int)
        MODEL_METRICS.append({"name":name,"accuracy":round(accuracy_score(yte,pred),3),"precision":round(precision_score(yte,pred,zero_division=0),3),"recall":round(recall_score(yte,pred,zero_division=0),3),"f1":round(f1_score(yte,pred,zero_division=0),3),"auc":round(roc_auc_score(yte,prob),3)})
    best = max(fitted, key=lambda n: next(m["auc"] for m in MODEL_METRICS if m["name"]==n))
    bundle = {"model":fitted[best], "name":best, "metrics":MODEL_METRICS}
    joblib.dump(bundle, path)
    return bundle

def load_model():
    global MODEL_METRICS
    path = Path(settings.model_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True); return _train_models(str(path))
    bundle = joblib.load(path); MODEL_METRICS = bundle.get("metrics", []); return bundle

BUNDLE = load_model(); MODEL = BUNDLE["model"]

def model_info():
    return {"selected_model":BUNDLE.get("name","Model"),"metrics":MODEL_METRICS,"dataset":"Synthetic demonstration dataset","records":6000,"clinical_status":"Prototype only — not clinically validated"}

def predict(payload: dict):
    x = np.array([[payload[f] for f in FEATURES]], dtype=float)
    probability = float(MODEL.predict_proba(x)[0,1])
    # Stable, human-readable local contribution proxy for hackathon explainability.
    baselines = np.array([50,.5,1.5,120,200,.2,150,.2,.8]); scales = np.array([18,.5,1.2,25,65,.4,30,.4,1.4])
    weights = np.array([.8,.25,.35,.45,.28,.25,-.42,.9,.75])
    impacts = ((x[0]-baselines)/scales)*weights
    order = np.argsort(np.abs(impacts))[::-1][:5]
    factors = [{"feature":LABELS[FEATURES[i]],"impact":round(float(abs(impacts[i])),3),"direction":"increases risk" if impacts[i] > 0 else "reduces risk"} for i in order]
    level = "Low" if probability < .30 else "Moderate" if probability < .65 else "High"
    recommendations = [
        "Discuss the result with a qualified clinician if symptoms or concerns are present.",
        "Track blood pressure, cholesterol, glucose, activity, sleep, and smoking status over time.",
        "Seek urgent medical care for chest pressure, severe shortness of breath, fainting, or pain spreading to the arm or jaw."
    ]
    return probability, level, factors, recommendations
