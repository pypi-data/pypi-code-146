from dataclasses import dataclass
from datetime import datetime
from typing import Optional


from intelliprove.api.models.enums import MentalHealthRiskScore
from intelliprove.api.models.dataclasses import Biomarkers


@dataclass
class BiomarkersResponse:
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

    @classmethod
    def from_json(cls, data: dict):
        mhr = MentalHealthRiskScore(data['mental_health_risk']) if ('mental_health_risk' in data and data['mental_health_risk'] is not None) else None
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            mental_health_risk=mhr,
            **{k:data[k] for k in data if k in cls.__dict__.keys()}
        )

    def to_dataclass(self) -> Biomarkers:
        return Biomarkers(**self.__dict__)