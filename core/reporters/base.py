from abc import ABC, abstractmethod
from core.models import Finding

class Reporter(ABC):
    @abstractmethod
    def report(self, findings: list[Finding]):
        ...