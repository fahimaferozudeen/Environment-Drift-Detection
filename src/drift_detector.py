import yaml


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


# Load expected configuration
expected = load_config("config/expected.yaml")


# Environments to check
environments = {
    "Development": "config/dev.yaml",
    "Testing": "config/test.yaml",
    "Staging": "config/staging.yaml",
    "Production": "config/production.yaml"
}


# Check each environment
for environment, file_path in environments.items():

    actual = load_config(file_path)

    drift = detect_drift(expected, actual)

    print("\n" + "=" * 60)
    print(f"Environment: {environment}")
    print("=" * 60)

    if drift:

        print("DRIFT DETECTED!")

        for key, values in drift.items():

            risk = get_risk_level(key)

            print(f"\nConfiguration: {key}")
            print(f"Expected: {values['expected']}")
            print(f"Actual:   {values['actual']}")
            print(f"Risk:     {risk}")

    else:

        print("No Drift Detected - Configuration is Correct")