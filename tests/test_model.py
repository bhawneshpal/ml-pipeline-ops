import json

import joblib


def test_model_file_exists_and_loads():
    with open("model/metadata.json", "r") as f:
        metadata = json.load(f)
    
    active_version = metadata["active_version"]
    model_path = metadata["versions"][active_version]["file"]
    
    model = joblib.load(model_path)
    assert model is not None


def test_active_model_meets_accuracy_threshold():
    with open("model/metadata.json", "r") as f:
        metadata = json.load(f)
    
    active_version = metadata["active_version"]
    test_accuracy = metadata["versions"][active_version]["test_accuracy"]
    
    MIN_ACCURACY = 0.80
    assert test_accuracy >= MIN_ACCURACY, f"Active model accuracy {test_accuracy} below threshold"


def test_no_severe_overfitting():
    with open("model/metadata.json", "r") as f:
        metadata = json.load(f)
    
    active_version = metadata["active_version"]
    version_info = metadata["versions"][active_version]
    
    gap = version_info["train_accuracy"] - version_info["test_accuracy"]
    MAX_GAP = 0.15
    assert gap <= MAX_GAP, f"Train-test gap {gap} indicates overfitting"