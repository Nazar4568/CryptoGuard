import ast
from core.analyzer import SastAnalyzer
from core.rules import InsecureRandomRule, WeakHashRule
from core.models import Severity


def test_insecure_random_found():
    code = "import random\nx = 5"
    tree = ast.parse(code)
    analyzer = SastAnalyzer(rules=[InsecureRandomRule()])

    analyzer.visit(tree)

    assert len(analyzer.findings) == 1
    assert analyzer.findings[0].rule_id == "CRYPTO001"
    assert analyzer.findings[0].severity == Severity.HIGH


def test_weak_hash_safe_context():
    code = "import hashlib\nhashlib.md5(image_data).hexdigest()"
    tree = ast.parse(code)
    analyzer = SastAnalyzer(rules=[WeakHashRule()])

    analyzer.visit(tree)

    assert len(analyzer.findings) == 1
    assert analyzer.findings[0].rule_id == "CRYPTO002"
    assert analyzer.findings[0].severity == Severity.LOW