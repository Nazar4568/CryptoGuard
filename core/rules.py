import ast
from core.interfaces import Rule
from core.models import Finding, Severity


class InsecureRandomRule(Rule):

    def __init__(self):
        super().__init__(id="CRYPTO001", severity=Severity.HIGH)

    def check(self, node: ast.AST) -> Finding | None:

        if isinstance(node, ast.Import):

            for alias in node.names:

                if alias.name == 'random':
                    return Finding(
                        rule_id=self.id,
                        severity=self.severity,
                        message="Found 'import random'. This module is not cryptographically secure.",
                        file_path="",
                        line_number=node.lineno,
                        remediation="Use the 'secrets' module instead."
                    )

        return None


class WeakHashRule(Rule):
    def __init__(self):
        # По умолчанию ставим HIGH, но мы будем динамически его менять
        super().__init__(id="CRYPTO002", severity=Severity.HIGH)

    def check(self, node: ast.AST) -> Finding | None:
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                if isinstance(node.func.value, ast.Name):
                    module_name = node.func.value.id

                    if module_name == 'hashlib' and method_name in ['md5', 'sha1']:

                        current_severity = Severity.LOW
                        message = f"Found weak hash '{method_name}'. Ensure it's not used for security."

                        sensitive_keywords = ['password', 'secret', 'token', 'key', 'credential', 'auth']

                        for arg in node.args:

                            for sub_node in ast.walk(arg):

                                if isinstance(sub_node, ast.Name):
                                    arg_name = sub_node.id.lower()

                                    if any(keyword in arg_name for keyword in sensitive_keywords):
                                        current_severity = Severity.HIGH
                                        message = f"CRITICAL: Weak hash '{method_name}' used on sensitive data ('{arg_name}')."
                                        break

                            if current_severity == Severity.HIGH:
                                break

                        return Finding(
                            rule_id=self.id,
                            severity=current_severity,
                            message=message,
                            file_path="",
                            line_number=node.lineno,
                            remediation="Use SHA-256 for integrity, or bcrypt/Argon2 for passwords."
                        )
        return None