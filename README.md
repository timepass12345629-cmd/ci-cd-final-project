# CI/CD Tools and Practices Final Project Template

## Project Name: ci-cd-final-project

[![CI Workflow](https://github.com/timepass12345629-cmd/ci-cd-final-project/actions/workflows/workflow.yml/badge.svg)](https://github.com/timepass12345629-cmd/ci-cd-final-project/actions)

## Project Overview

This repository contains the complete implementation for the **CI/CD Tools and Practices Final Project** (part of the Coursera / IBM DevOps and Software Engineering Professional Certificate).

The project demonstrates an enterprise-grade Continuous Integration and Continuous Delivery (CI/CD) pipeline for a cloud-native microservice using:
* **GitHub Actions** for automated Continuous Integration (code style linting with `flake8` and unit testing with `nose`).
* **Tekton Pipelines** for cloud-native Continuous Delivery on **Red Hat OpenShift**.
* **Containerization** with Docker / Buildah, deploying into an OpenShift cluster with automated health checks on port 8000.

---

## Architecture and Pipeline Flow

```
[ Developer Push ]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│               GitHub Actions CI Workflow               │
│  - Checkout Code                                       │
│  - Set up Python 3.9 & Install Dependencies            │
│  - Lint with flake8                                    │
│  - Run unit tests with nose                            │
└────────────────────────────────────────────────────────┘
       │
       ▼ (Webhook / Trigger)
┌────────────────────────────────────────────────────────┐
│             Tekton / OpenShift CD Pipeline             │
│                                                        │
│  [1. cleanup]                                          │
│         │                                              │
│         ▼                                              │
│  [2. git-clone]                                        │
│         │                                              │
│         ▼                                              │
│  [3. flake8 (Lint)]                                    │
│         │                                              │
│         ▼                                              │
│  [4. nose (Unit Tests)]                                │
│         │                                              │
│         ▼                                              │
│  [5. buildah (Build & Push Image)]                     │
│         │                                              │
│         ▼                                              │
│  [6. deploy (OpenShift Deployment)]                    │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│         Red Hat OpenShift Cluster Deployment           │
│  - Deployment: cd-app                                  │
│  - Service & Route: Port 8000                          │
│  - Status: SERVICERUNNING                              │
└────────────────────────────────────────────────────────┘
```

---

## Technology Stack

* **Backend Framework:** Python 3.9, Flask 2.2, Werkzeug
* **Code Quality & Linter:** Flake8
* **Unit Testing & Coverage:** Nose (`nosetests`), Coverage.py
* **Containerization:** Docker / Buildah
* **CI/CD Automation:** GitHub Actions
* **Cloud-Native CD:** Tekton Pipelines (`tekton.dev/v1beta1`)
* **Deployment Platform:** Red Hat OpenShift Container Platform

---

## Repository Structure

```
├── .github/
│   └── workflows/
│       └── workflow.yml         # GitHub Actions CI workflow (flake8 + nose)
├── .tekton/
│   ├── pvc.yml                  # OpenShift PersistentVolumeClaim (1Gi)
│   ├── tasks.yml                # Tekton tasks (cleanup, flake8, nose, deploy)
│   └── pipeline.yml             # Tekton 6-step pipeline definition
├── service/
│   ├── __init__.py              # Flask app entrypoint & startup logging
│   ├── routes.py                # REST API endpoints (CRUD + /health)
│   ├── models.py                # In-memory Product data model with validation
│   └── common/
│       └── status.py            # Standard HTTP status code constants
├── tests/
│   ├── __init__.py
│   ├── test_models.py           # Unit tests for data models
│   └── test_routes.py           # Unit tests for API endpoints
├── Dockerfile                   # Production container definition (Port 8000)
├── requirements.txt             # Python dependencies
├── setup.cfg                    # Configuration for flake8 & nosetests
├── cicd-github-validate         # Validation output of GitHub Actions run
├── oc-pipeline-application-logs # OpenShift pod startup logs (SERVICERUNNING)
└── README.md                    # Project documentation
```

---

## Local Setup & Execution

### 1. Prerequisites
* Python 3.9 or higher
* Git

### 2. Installation
```bash
# Clone the repository
git clone git@github-college:timepass12345629-cmd/ci-cd-final-project-.git
cd ci-cd-final-project-

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Linting & Tests
```bash
# Run Flake8 linter
flake8 service --count --max-complexity=10 --max-line-length=127 --statistics

# Run unit tests with nose or unittest
python -m unittest discover tests
```

### 4. Run Application Locally
```bash
python -m flask --app service:app run --port 8000
```
Navigate to `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/health`.

---

## OpenShift Pipeline Deployment Guide

### Step 1: Create Persistent Volume Claim
```bash
oc apply -f .tekton/pvc.yml
```

### Step 2: Install Tekton Tasks
```bash
# Install git-clone and buildah from Tekton Hub / OpenShift Cluster Catalog
tkn hub install task git-clone
tkn hub install task buildah

# Apply custom tasks (cleanup, flake8, nose, deploy)
oc apply -f .tekton/tasks.yml
```

### Step 3: Apply and Trigger Pipeline
```bash
# Apply pipeline definition
oc apply -f .tekton/pipeline.yml

# Start pipeline execution
tkn pipeline start cd-pipeline \
    -w name=pipeline-workspace,claimName=pipelinerun-pvc \
    -p git-url="https://github.com/timepass12345629-cmd/ci-cd-final-project-.git" \
    -p git-revision="master" \
    -p image-name="image-registry.openshift-image-registry.svc:5000/$(oc project -q)/cd-app:latest" \
    --showlog
```

---

## Coursera Final Project Checklist Mapping

| Criteria | Artifact / Question | Status |
| :--- | :--- | :---: |
| Q1 | Public GitHub URL of `README.md` | Completed |
| Q2 | GitHub URL of `.github/workflows/workflow.yml` (flake8 & nose) | Completed |
| Q3 | GitHub URL of `.tekton/tasks.yml` (cleanup & nose tasks) | Completed |
| Q4 | Terminal output from `cicd-github-validate` | Completed |
| Q5 | Screenshot: `oc-pipelines-console-pvc-details` | Ready |
| Q6 | Screenshot: `oc-pipelines-oc-final` (6 tasks flow) | Ready |
| Q7 | Screenshot: `oc-pipelines-oc-green` (all successful) | Ready |
| Q8 | Application logs text: `oc-pipeline-application-logs` (SERVICERUNNING on port 8000) | Completed |

---

## License

This project is licensed under the Apache 2.0 License.

