import ast
from pathlib import Path
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

    def analyze_file(self, file_path: str):
        self.current_file = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            tree = ast.parse(source_code)
            self.visit(tree)
        except Exception as e:
            print(f"Skipping {file_path} due to error: {e}")

    def analyze_path(self, target_path: str) -> list[Finding]:
        path = Path(target_path)

        if not path.exists():
            print(f"Error: Path '{target_path}' does not exist.")
            return self.findings

        if path.is_file():
            if path.suffix == ".py":
                self.analyze_file(str(path))
            else:
                print("Target is not a .py file.")

        elif path.is_dir():
            for py_file in path.rglob("*.py"):
                self.analyze_file(str(py_file))

        return self.findings
