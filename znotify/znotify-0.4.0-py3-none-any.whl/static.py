import sys
from enum import Enum

ENDPOINT = "https://push.learningman.top" if 'unittest' not in sys.modules else "http://localhost:14444"


class Priority(Enum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
