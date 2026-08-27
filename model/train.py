import joblib
import json
import os
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = load_iris()
X, y = data.data, data.target

# Split into train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate accuracies (for overfitting check later)
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print(f"Train accuracy: {train_accuracy:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")

# Determine next version number
metadata_path = "model/metadata.json"
if os.path.exists(metadata_path):
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    next_version = metadata["latest_version"] + 1
else:
    metadata = {"active_version": None, "latest_version": 0, "versions": {}}
    next_version = 1

# Save model with version number
model_filename = f"model/model_v{next_version}.pkl"
joblib.dump(model, model_filename)

# Update metadata
metadata["latest_version"] = next_version
metadata["versions"][f"v{next_version}"] = {
    "file": model_filename,
    "train_accuracy": train_accuracy,
    "test_accuracy": test_accuracy,
    "trained_at": datetime.now().isoformat()
}

with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Model saved as {model_filename}")
print(f"Metadata updated at {metadata_path}")