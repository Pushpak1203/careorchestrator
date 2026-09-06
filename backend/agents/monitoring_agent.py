from datetime import datetime, timedelta, timezone
from statistics import mean
from db.supabase_client import get_supabase
from models.schemas import RiskAssessment

def _severity_rank(level: str) -> int:
    return {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}[level]

def assess_patient(patient_id: str) -> RiskAssessment:
    db = get_supabase()
    since = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    rows = db.table("vitals").select("*").eq("patient_id", patient_id).gte("recorded_at", since).order("recorded_at", desc=False).execute().data
    if not rows:
        return RiskAssessment(risk_level="MEDIUM", score=30, reasons=["No vital readings were recorded in the last 3 days."], latest_vitals={}, biomarker_drift={"data_gap": True})

    reasons, score, drift = [], 0, {}
    latest = rows[-1]

    glucose = [float(r["blood_glucose"]) for r in rows if r.get("blood_glucose") is not None]
    if glucose:
        avg = mean(glucose)
        increasing = len(glucose) >= 3 and glucose[-1] > glucose[0] * 1.1
        drift["blood_glucose"] = {"values": glucose, "average": round(avg, 2), "increasing": increasing}
        if latest["blood_glucose"] is not None and float(latest["blood_glucose"]) >= 300:
            score += 70; reasons.append("Latest blood glucose is critically elevated (>=300 mg/dL).")
        elif avg >= 250 or increasing and glucose[-1] >= 220:
            score += 45; reasons.append("Blood glucose shows sustained high values or upward drift over 3 days.")
        elif avg >= 180:
            score += 20; reasons.append("Blood glucose is above the common monitoring target range.")

    systolic = [int(r["systolic_bp"]) for r in rows if r.get("systolic_bp") is not None]
    if systolic:
        drift["systolic_bp"] = {"values": systolic, "average": round(mean(systolic), 1)}
        if systolic[-1] >= 180:
            score += 70; reasons.append("Latest systolic blood pressure is severely elevated (>=180 mmHg).")
        elif mean(systolic) >= 160:
            score += 35; reasons.append("Systolic blood pressure is persistently high.")

    oxygen = [float(r["oxygen_saturation"]) for r in rows if r.get("oxygen_saturation") is not None]
    if oxygen:
        drift["oxygen_saturation"] = {"values": oxygen, "minimum": min(oxygen)}
        if oxygen[-1] < 90:
            score += 80; reasons.append("Latest oxygen saturation is below 90%.")
        elif oxygen[-1] < 94:
            score += 35; reasons.append("Latest oxygen saturation is below 94%.")

    heart = [int(r["heart_rate"]) for r in rows if r.get("heart_rate") is not None]
    if heart:
        drift["heart_rate"] = {"values": heart, "latest": heart[-1]}
        if heart[-1] >= 130 or heart[-1] <= 40:
            score += 50; reasons.append("Latest heart rate is outside a high-risk threshold.")

    if score >= 70: level = "CRITICAL"
    elif score >= 45: level = "HIGH"
    elif score >= 20: level = "MEDIUM"
    else: level = "LOW"

    if not reasons:
        reasons.append("No configured high-risk drift threshold was triggered.")

    return RiskAssessment(risk_level=level, score=min(score, 100), reasons=reasons, latest_vitals=latest, biomarker_drift=drift)
