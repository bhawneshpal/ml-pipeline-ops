import json
import sys

metadata_path = "model/metadata.json"

with open(metadata_path, "r") as f:
    metadata = json.load(f)

latest_version = metadata["latest_version"]
version_key = f"v{latest_version}"

# Set the latest version as active
metadata["active_version"] = version_key

with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Deployed: {version_key} is now the active model")
