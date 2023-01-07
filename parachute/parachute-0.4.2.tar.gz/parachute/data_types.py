import re
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass(order=True)
class Parameter:
    """Represent a MAVLink parameter."""

    name: str
    value: Any = None
    index: int = 0
    type: int = 10

    def __post_init__(self):
        if self.value is not None:
            if self.is_float:
                self.value = float(self.value)
            else:
                self.value = int(self.value)
        self.name = self.name.upper()

    @classmethod
    def from_message(cls, message) -> "Parameter":
        return Parameter(
            name=message["param_id"],
            value=message["param_value"],
            index=message["param_index"],
            type=message["param_type"],
        )

    @property
    def is_float(self):
        """Return whether the value of this parameter is a float."""
        return self.type in (9, 10)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "index": self.index,
            "type": self.type,
        }


@dataclass()
class Backup:
    """Represent an entire backup file."""

    status: List[str] = field(default_factory=list)
    schema: int = 1
    timestamp: datetime = field(default_factory=datetime.now)
    parameters: Dict[str, Parameter] = field(default_factory=dict)

    @property
    def status_str(self) -> str:
        """Construct a status comment string from a list of status messages."""
        if not self.status:
            return ""
        return "// " + "\n// ".join(self.status) + "\n\n"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Backup":
        d["timestamp"] = datetime.fromisoformat(d["timestamp"])
        d["parameters"] = {
            name: Parameter(name=name, **data) for name, data in d["parameters"].items()
        }
        backup = cls(**d)
        return backup

    def as_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "parameters": {
                name: param.as_dict() for name, param in sorted(self.parameters.items())
            },
        }

    def filter(self, regex: Optional[re.Pattern]) -> None:
        """
        Filter parameters based on a regex.

        Modifies the backup in-place.
        """
        if not regex:
            return

        self.parameters = {
            name: param for name, param in self.parameters.items() if regex.search(name)
        }
