import yaml
import os


def read_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    return config


# Project config folder
config_folder = "config"

# Configuration files
files = [
    "expected.yaml",
    "dev.yaml",
    "test.yaml",
    "staging.yaml",
    "production.yaml"
]


for file_name in files:

    file_path = os.path.join(config_folder, file_name)

    config = read_config(file_path)

    print("\n" + "=" * 40)
    print(file_name)
    print("=" * 40)

    for key, value in config.items():
        print(f"{key}: {value}")