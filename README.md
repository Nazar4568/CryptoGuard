# CryptoGuard 🛡️

A lightweight, extensible Static Application Security Testing (SAST) tool written in Python. CryptoGuard uses Abstract Syntax Tree (AST) parsing to analyze Python codebases for cryptographic vulnerabilities and secure coding violations.

Unlike simple regex-based scanners, CryptoGuard understands code context, reducing false positives through basic heuristic analysis.

## Core Features

* **AST-Based Analysis:** Safely parses Python code into syntax trees without executing it.
* **Context-Aware Heuristics:** Intelligently differentiates between safe and unsafe uses of algorithms (e.g., flagging `hashlib.md5` only when used with sensitive variables like `password` or `token`).
* **DevSecOps Ready:** Designed for CI/CD integration. Generates reports in **SARIF** (Static Analysis Results Interchange Format) for native integration with GitHub Code Scanning.
* **Extensible Rule Engine:** Built with OOP principles (SOLID), allowing new security rules to be added as isolated modules.

## Installation & Usage

No external dependencies are required for the core scanner (only standard Python libraries are used).

```bash
# Clone the repository
git clone [https://github.com/Nazar4568/CryptoGuard.git](https://github.com/Nazar4568/CryptoGuard.git)
cd CryptoGuard

# Run the scanner on a single file or a whole directory
python main.py /path/to/your/project
