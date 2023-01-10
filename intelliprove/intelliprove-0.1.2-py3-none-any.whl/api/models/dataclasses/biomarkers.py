from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from intelliprove.api.models.enums import MentalHealthRiskScore


@dataclass
class Biomarkers:
    """Data class that contains the extracted biomarkers"""
    timestamp: datetime
    mental_health_risk: Optional[MentalHealthRiskScore]
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    heart_rate_variability: Optional[int] = None
    ans_balance: Optional[int] = None
    morning_readiness: Optional[int] = None
    acute_mental_stress_score: Optional[int] = None
    resonant_breathing_score: Optional[int] = None
