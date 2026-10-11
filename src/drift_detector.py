
import yaml
import sys


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

    medium_risk = ["port", "memory"]

    if key in high_risk:
        return "HIGH"
    elif key in medium_risk:
        return "MEDIUM"
    else:
        return "LOW"


def main():
    expected = load_config("config/expected.yaml")

    environments = {
        "Development": "config/dev.yaml",
        "Testing": "config/test.yaml",
        "Staging": "config/staging.yaml",
        "Production": "config/production.yaml"
    }

    production_drift_found = False

    for environment, file_path in environments.items():
        actual = load_config(file_path)
        drift = detect_drift(expected, actual)

        print("\n" + "=" * 60)
        print(f"Environment: {environment}")
        print("=" * 60)

        if drift:
            print("DRIFT DETECTED!")

            if environment == "Production":
                production_drift_found = True

            for key, values in drift.items():
                risk = get_risk_level(key)
                print(f"\nConfiguration: {key}")
                print(f"Expected: {values['expected']}")
                print(f"Actual:   {values['actual']}")
                print(f"Risk:     {risk}")
        else:
            print("No Drift Detected - Configuration is Correct")

    if production_drift_found:
        print("\nPIPELINE STATUS: FAILED - Production drift detected!")
        sys.exit(1)

    print("\nPIPELINE STATUS: PASSED - No production drift detected!")


if __name__ == "__main__":
    main()
