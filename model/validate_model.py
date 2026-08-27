import json
import sys

# Thresholds
MIN_TEST_ACCURACY = 0.80
MAX_TRAIN_TEST_GAP = 0.15

# Load metadata
with open("model/metadata.json", "r") as f:
    metadata = json.load(f)

# Get the latest version's info
latest_version = metadata["latest_version"]
version_key = f"v{latest_version}"
version_info = metadata["versions"][version_key]

train_accuracy = version_info["train_accuracy"]
test_accuracy = version_info["test_accuracy"]
gap = train_accuracy - test_accuracy

print(f"Validating {version_key}")
print(f"Train accuracy: {train_accuracy:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Gap: {gap:.4f}")

# Check 1: Minimum accuracy
if test_accuracy < MIN_TEST_ACCURACY:
    print(f"FAILED: test accuracy ({test_accuracy:.4f}) below threshold ({MIN_TEST_ACCURACY})")
    sys.exit(1)

# Check 2: Overfitting gap
if gap > MAX_TRAIN_TEST_GAP:
    print(f"FAILED: overfitting detected, gap ({gap:.4f}) exceeds max allowed ({MAX_TRAIN_TEST_GAP})")
    sys.exit(1)

print(f"PASSED: {version_key} is safe to deploy")
sys.exit(0)
