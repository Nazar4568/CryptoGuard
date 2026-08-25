import json
from core.models import Finding
from core.reporters.base import Reporter


class SarifReporter(Reporter):
    def __init__(self, output_file: str = "results.sarif"):
        self.output_file = output_file

    def report(self, findings: list[Finding]):
        sarif_log = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "CryptoGuard SAST",
                            "informationUri": "https://github.com/Nazar4568/CryptoGuard",
                            "rules": []
                        }
                    },
                    "results": []
                }
            ]
        }

        for finding in findings:
            result = {
                "ruleId": finding.rule_id,
                "level": self._map_severity_to_sarif(finding.severity.value),
                "message": {
                    "text": finding.message
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": finding.file_path
                            },
                            "region": {
                                "startLine": finding.line_number
                            }
                        }
                    }
                ]
            }
            sarif_log["runs"][0]["results"].append(result)

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(sarif_log, f, indent=4)

        print(f"SARIF report successfully saved to {self.output_file}")

    def _map_severity_to_sarif(self, severity: str) -> str:
        mapping = {
            "CRITICAL": "error",
            "HIGH": "error",
            "MEDIUM": "warning",
            "LOW": "note"
        }
        return mapping.get(severity, "none")