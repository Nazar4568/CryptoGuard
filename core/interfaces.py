import ast
from abc import ABC, abstractmethod
from typing import Protocol

from core.models import Finding, Severity


class Rule(ABC):
    def __init__(self, id: str, severity: Severity):
        self.id = id
        self.severity = severity

    @abstractmethod
    def check(self, node: ast.AST) -> Finding | None:
        ...


class Analyzer(Protocol):
    def analyze(self, target_path: str) -> list[Finding]:
        ...