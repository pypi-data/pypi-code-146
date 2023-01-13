from dataclasses import dataclass, field
from typing import List


@dataclass(init=True, repr=True, eq=True)
class JobDto:
    jobId: str = ""
    specs: str = ""
    status: str = ""
    messages: List[str] = field(default_factory=list)
    error: str = ""
    problemType: str = ""
    processor: str = ""
    problemFiles: List[str] = field(default_factory=list)
    specFiles: List[str] = field(default_factory=list)
