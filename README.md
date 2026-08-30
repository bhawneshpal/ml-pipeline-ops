

# ML Pipeline Ops

A production-ready pipeline that takes a trained ML model from a script on a laptop to a reliable, observable service — with automated validation, safe deployment, and instant rollback.

## Problem

Most ML projects stop at a trained model with good accuracy. They don't answer: How do you know the model is actually working in production? What happens when a bad model gets deployed? How do you recover without downtime?

This project closes that gap — treating model deployment as an operations problem, not just a machine learning problem.

## What it does

- **Trains and versions models** — every training run is saved as a new version, never overwritten
- **Validates before deploying** — checks both minimum accuracy and train/test accuracy gap (to catch overfitting) before a model is allowed to go live
- **Deploys safely** — a model only becomes "active" after passing validation
- **Rolls back instantly** — one command switches the live model back to any previous version, no retraining or downtime
- **Serves predictions via API** — with input validation (bad requests get a clean error, not a crash) and structured JSON logging
- **Tracks basic metrics** — request count, error count, and average latency via a `/metrics` endpoint
- **Runs in CI/CD** — every push automatically lints, trains, validates, tests, and builds a Docker image; a failing validation blocks deployment

## Architecture

Push code → Lint → Train model → Validate (accuracy + overfitting gate) → Deploy (if passed) → Run tests → Build Docker image

The live API always reads which model version is "active" from `metadata.json` — so deploying or rolling back is just updating a pointer, not restarting the service or retraining anything.

## Project structure

ml-pipeline-ops/
├── model/
│   ├── train.py            # Trains and saves a new versioned model
│   ├── validate_model.py    # Accuracy + overfitting gate
│   ├── deploy.py             # Marks a validated model as active
│   ├── rollback.py            # Switches active model to any previous version
│   └── serve.py                # FastAPI app: /predict, /health, /metrics
├── monitoring/
│   └── metrics.py               # Basic request/latency tracking
├── tests/
│   ├── test_model.py             # Model accuracy and overfitting tests
│   └── test_api.py                # API endpoint tests (valid + invalid input)
├── .github/workflows/ci-cd.yml     # CI/CD: lint → train → validate → deploy → test → build
├── Dockerfile                       # Multi-stage build with healthcheck
└── requirements.txt

## Running locally

Install dependencies:
```
pip install -r requirements.txt
```

Train a model:
```
python model/train.py
```

Validate it:
```
python model/validate_model.py
```

Deploy it (only if validation passed):
```
python model/deploy.py
```

Start the API:
```
uvicorn model.serve:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### Rolling back

```
python model/rollback.py v1
```

## Running with Docker

```
docker build -t ml-pipeline-ops .
docker run -p 8000:8000 ml-pipeline-ops
```

## Running tests

```
pytest tests/ -v
```

## What can fail, and how it's handled

| Failure | How it's handled |
|---|---|
| Malformed or invalid API input | Pydantic validation returns a clean 422 error, service doesn't crash |
| A retrained model performs worse | Validation gate blocks deployment if accuracy drops below threshold |
| A retrained model overfits | Validation checks the train/test accuracy gap, not just raw accuracy |
| A bad model somehow reaches production | One command (`rollback.py`) switches back to the last known-good version, no downtime |
| Silent service degradation | `/metrics` exposes request count, error count, and latency for visibility |

## CI/CD

Every push to `main` triggers:

1. Lint (`ruff`)
2. Train a fresh model
3. Validate it (accuracy + overfitting gate)
4. Deploy if validation passes
5. Run the full test suite
6. Build the Docker image

If validation fails, the pipeline stops — a bad model never reaches the point where it could be deployed.