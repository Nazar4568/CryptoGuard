import ast
from core.interfaces import Rule
from core.models import Finding


class SastAnalyzer(ast.NodeVisitor):

    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.findings: list[Finding] = []
        self.current_file = ""

    def visit_Import(self, node: ast.Import):

        for rule in self.rules:
            finding = rule.check(node)

            if finding:
                finding.file_path = self.current_file
                self.findings.append(finding)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        for rule in self.rules:
            finding = rule.check(node)
            if finding:
                finding.file_path = self.current_file
                self.findings.append(finding)
        self.generic_visit(node)

    def analyze_file(self, file_path: str) -> list[Finding]:
        self.current_file = file_path

        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        self.visit(tree)

        return self.findings
