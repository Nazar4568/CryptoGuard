import argparse
from core.rules import InsecureRandomRule, WeakHashRule
from core.analyzer import SastAnalyzer
from core.reporters.sarif import SarifReporter
import sys


def main():
    parser = argparse.ArgumentParser(
        description="CryptoGuard - AST-based Static Application Security Testing (SAST) tool."
    )

    parser.add_argument(
        "target",
        type=str,
        help="Path to the Python file you want to scan."
    )

    args = parser.parse_args()

    print(f"Starting CryptoGuard SAST Scanner on: {args.target}")

    active_rules = [
        InsecureRandomRule(),
        WeakHashRule()
    ]

    analyzer = SastAnalyzer(rules=active_rules)

    results = analyzer.analyze_path(args.target)
    if not results:
        print("No vulnerabilities found. Code is secure!")
        sys.exit(0)
    else:
        print(f"Found {len(results)} vulnerabilities.\n")
        reporter = SarifReporter()
        reporter.report(results)

        sys.exit(1)


if __name__ == "__main__":
    main()