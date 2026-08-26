# CryptoGuard 

**Tech Stack:** Python 3 | `ast` | `tokenize` | `pytest` | GitHub Actions (CI/CD) | SARIF

A lightweight, extensible Static Application Security Testing (SAST) tool written in Python. CryptoGuard uses Abstract Syntax Tree (AST) parsing to analyze Python codebases for cryptographic vulnerabilities and secure coding violations.

Unlike simple regex-based scanners, CryptoGuard understands code context, reducing false positives through basic heuristic analysis.

## Core Features

* **AST-Based Analysis:** Safely parses Python code into syntax trees without executing it.
* **Context-Aware Heuristics:** Intelligently differentiates between safe and unsafe uses of algorithms (e.g., flagging `hashlib.md5` only when used with sensitive variables like `password` or `token`).
* **Inline Ignores:** Uses lexical scanning (`tokenize`) to respect `# cryptoguard: ignore` comments, allowing developers to easily bypass intended behavior.
* **DevSecOps Ready:** Designed for CI/CD integration. Generates reports in **SARIF** (Static Analysis Results Interchange Format) for native integration with GitHub Code Scanning.
* **Extensible Rule Engine:** Built with OOP principles (SOLID), allowing new security rules to be added as isolated modules.

## Installation & Usage

No external dependencies are required for the core scanner (only standard Python libraries are used).

```bash
# Clone the repository
git clone [https://github.com/Nazar4568/CryptoGuard.git](https://github.com/Nazar4568/CryptoGuard.git)
cd CryptoGuard
```

Run the Scanner
CryptoGuard automatically skips virtual environments (.venv) and testing directories to optimize performance and reduce noise.

```bash
# Scan a whole project directory
python main.py /path/to/your/project

# Or scan a single file
python main.py test_code.py
```

Run Unit Tests
The rule engine is covered by automated tests. You can run them using pytest:

```bash
pip install pytest
pytest
```
CI/CD Integration (GitHub Actions)
CryptoGuard is designed to act as a Quality Gate in your pipelines. If vulnerabilities are found, it exits with a non-zero status code (exit 1) to block vulnerable PRs.

It automatically generates a results.sarif file that can be uploaded to GitHub Security tabs using the github/codeql-action/upload-sarif action. Check the .github/workflows/security_gate.yml file for a working example.



