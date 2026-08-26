import ast
import tokenize
import io
from pathlib import Path
from core.interfaces import Rule
from core.models import Finding


class SastAnalyzer(ast.NodeVisitor):
    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.findings: list[Finding] = []
        self.current_file = ""
        self.ignored_lines = set()


    def _extract_ignored_lines(self, source_code: str):
        self.ignored_lines.clear()

        bytes_io = io.BytesIO(source_code.encode('utf-8'))
        tokens = tokenize.tokenize(bytes_io.readline)

        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                if "cryptoguard: ignore" in tok.string.lower():
                    self.ignored_lines.add(tok.start[0])

    def visit_Import(self, node: ast.Import):
        for rule in self.rules:
            finding = rule.check(node)
            if finding:
                if finding.line_number not in self.ignored_lines:
                    finding.file_path = self.current_file
                    self.findings.append(finding)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        for rule in self.rules:
            finding = rule.check(node)
            if finding:
                if finding.line_number not in self.ignored_lines:
                    finding.file_path = self.current_file
                    self.findings.append(finding)
        self.generic_visit(node)

    def analyze_file(self, file_path: str):
        self.current_file = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            self._extract_ignored_lines(source_code)

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
