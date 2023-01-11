from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class CallStatuses:
    Started = "started"
    Ringing = "ringing"
    Answered = "answered"
    Completed = "completed"
