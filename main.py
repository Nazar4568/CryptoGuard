from core.rules import InsecureRandomRule,WeakHashRule
from core.analyzer import SastAnalyzer


def main():
    print("Starting CryptoGuard SAST Scanner...")

    active_rules = [
        InsecureRandomRule(),WeakHashRule()
    ]

    analyzer = SastAnalyzer(rules=active_rules)

    target_file = "test_code.py"

    results = analyzer.analyze_file(target_file)

    if not results:
        print("No vulnerabilities found. Code is secure!")
    else:
        print(f"Found {len(results)} vulnerabilities:\n")
        for finding in results:
            print(finding)


if __name__ == "__main__":
    main()