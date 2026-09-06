from datetime import date, datetime
from typing import Any, Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
AlertStatus = Literal["OPEN", "ACKNOWLEDGED", "RESOLVED"]

class PatientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    date_of_birth: Optional[date] = None
    phone: str = Field(min_length=5, max_length=32)
    preferred_language: Literal["en", "es"] = "en"
    assigned_clinician: Optional[str] = None
    clinician_phone: Optional[str] = None
    chronic_conditions: list[str] = Field(default_factory=list)

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    preferred_language: Optional[Literal["en", "es"]] = None
    assigned_clinician: Optional[str] = None
    clinician_phone: Optional[str] = None
    chronic_conditions: Optional[list[str]] = None
    risk_level: Optional[RiskLevel] = None
    last_check_in_at: Optional[datetime] = None

class VitalCreate(BaseModel):
    patient_id: UUID
    blood_glucose: Optional[float] = Field(default=None, ge=0, le=1000)
    systolic_bp: Optional[int] = Field(default=None, ge=40, le=300)
    diastolic_bp: Optional[int] = Field(default=None, ge=20, le=200)
    heart_rate: Optional[int] = Field(default=None, ge=20, le=300)
    oxygen_saturation: Optional[float] = Field(default=None, ge=50, le=100)
    weight_kg: Optional[float] = Field(default=None, ge=1, le=500)
    source: str = Field(default="manual", max_length=50)
    recorded_at: Optional[datetime] = None

class VitalOut(VitalCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime

class AlertUpdate(BaseModel):
    status: AlertStatus

class CaregiverCreate(BaseModel):
    patient_id: UUID
    full_name: str = Field(min_length=2, max_length=120)
    relationship: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=5, max_length=32)
    preferred_language: Literal["en", "es"] = "en"

class CaregiverUpdate(BaseModel):
    full_name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[Literal["en", "es"]] = None
    active: Optional[bool] = None

class AgentRunRequest(BaseModel):
    patient_id: UUID

class RiskAssessment(BaseModel):
    risk_level: RiskLevel
    score: int
    reasons: list[str]
    latest_vitals: dict[str, Any]
    biomarker_drift: dict[str, Any]
