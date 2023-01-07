from dataclasses import dataclass

@dataclass
class SummaryResults:
    exact_match: bool
    score: float
    a_valid: bool
    b_valid: bool
    matches: dict
