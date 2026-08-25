from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class Finding:
    rule_id: str
    severity: Severity
    message: str
    file_path: str
    line_number: int
    remediation: str | None = None