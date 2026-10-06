import yaml
import csv


def load_config(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def detect_drift(expected, actual):
    drift = {}

    for key in expected:

        expected_value = expected[key]
        actual_value = actual.get(key)

        if expected_value != actual_value:
            drift[key] = {
                "expected": expected_value,
                "actual": actual_value
            }

    return drift


def get_risk_level(key):

    high_risk = [
        "python_version",
        "django_version",
        "mysql_version"
    ]

    medium_risk = [
        "port",
        "memory"
    ]

    if key in high_risk:
        return "HIGH"

    elif key in medium_risk:
        return "MEDIUM"

    else:
        return "LOW"


# Expected configuration
expected = load_config("config/expected.yaml")


# Environments
environments = {
    "Development": "config/dev.yaml",
    "Testing": "config/test.yaml",
    "Staging": "config/staging.yaml",
    "Production": "config/production.yaml"
}


# Store report data
report_data = []


# Check each environment
for environment, file_path in environments.items():

    actual = load_config(file_path)

    drift = detect_drift(expected, actual)

    for key, values in drift.items():

        risk = get_risk_level(key)

        report_data.append({
            "Environment": environment,
            "Configuration": key,
            "Expected": values["expected"],
            "Actual": values["actual"],
            "Risk": risk
        })


# Create CSV report
report_file = "reports/drift_report.csv"

with open(report_file, "w", newline="") as file:

    fieldnames = [
        "Environment",
        "Configuration",
        "Expected",
        "Actual",
        "Risk"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(report_data)


print("\nDrift report generated successfully!")
print(f"Report saved to: {report_file}")