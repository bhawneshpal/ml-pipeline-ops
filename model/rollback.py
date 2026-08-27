import json
import sys

metadata_path = "model/metadata.json"

if len(sys.argv) != 2:
    print("Usage: python rollback.py <version>  (e.g. python rollback.py v1)")
    sys.exit(1)

target_version = sys.argv[1]

with open(metadata_path, "r") as f:
    metadata = json.load(f)

if target_version not in metadata["versions"]:
    print(f"FAILED: {target_version} does not exist in metadata")
    sys.exit(1)

metadata["active_version"] = target_version

with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Rolled back: {target_version} is now the active model")
