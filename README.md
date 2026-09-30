# Continuous Performance Benchmarking & Regression Detection Platform

A CI/CD-integrated performance engineering platform that continuously benchmarks APIs, measures latency and reliability metrics, compares results against approved performance baselines, and automatically detects performance regressions before they reach production.

---

## 🚀 Overview

Performance testing is often executed as a separate activity near the end of a development cycle. This project brings performance validation directly into the development and CI/CD workflow.

The platform automatically:

* Executes API tests
* Generates repeatable performance benchmarks
* Measures P50, P95 and P99 latency
* Tracks average, minimum and maximum response time
* Monitors request failures and success rate
* Compares current performance against a baseline
* Detects performance regressions
* Executes load tests using Locust
* Runs automatically through GitHub Actions
* Stores benchmark artifacts for analysis

The goal is to treat **performance as a continuous quality gate** rather than a one-time testing activity.

---

## 🏗️ Architecture

```text
                     Developer Push / Pull Request
                                |
                                v
                     +-----------------------+
                     |    GitHub Actions     |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     |     Pytest Tests      |
                     |     API Validation    |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     | Performance Benchmark |
                     |       Runner          |
                     +-----------+-----------+
                                 |
                                 v
              +----------------------------------------+
              |          Performance Metrics            |
              |                                        |
              |  Average | P50 | P95 | P99 | Min | Max |
              |  Failures | Success Rate              |
              +-------------------+--------------------+
                                  |
                                  v
                     +-----------------------+
                     | Baseline Comparison   |
                     +-----------+-----------+
                                 |
                     +-----------+-----------+
                     |                       |
                     v                       v
              Performance Pass       Regression Detected
                     |                       |
                     v                       v
                 CI Pass                  CI Fail
                                             |
                                             v
                                    Performance Artifact
```

---

## ✨ Features

### API Performance Benchmarking

The platform executes repeated HTTP requests against application endpoints and records response-time measurements.

Supported metrics include:

* Request count
* Average latency
* P50 latency
* P95 latency
* P99 latency
* Minimum latency
* Maximum latency
* Failure count
* Success rate

---

### 📊 Percentile-Based Performance Analysis

Instead of relying only on average response time, the platform measures latency percentiles.

```text
P50
 |
 +---- Typical request latency

P95
 |
 +---- Slow requests experienced by ~5% of requests

P99
 |
 +---- Tail latency experienced by ~1% of requests
```

This makes the benchmark more useful for identifying latency spikes and tail-performance problems.

---

### 🔍 Automated Regression Detection

Current performance is compared against an approved baseline.

Example:

```text
Baseline P95: 100 ms
Current P95:  125 ms

Increase:     +25%
Threshold:    10%

Result:
PERFORMANCE REGRESSION DETECTED
```

A regression can cause the CI pipeline to fail.

---

### ⚡ Load Testing with Locust

The project includes Locust-based load testing for simulating multiple API users.

The workload covers:

```text
GET /health
GET /api/products/{id}
GET /api/slow
```

Locust provides visibility into:

* Requests per second
* Response times
* Median latency
* P95 latency
* P99 latency
* Failure rate
* Concurrent user behavior

---

### 🔄 Continuous CI/CD Performance Validation

GitHub Actions automatically runs the performance workflow on:

* Push
* Pull Request
* Manual workflow execution

Pipeline:

```text
Checkout
   ↓
Install Dependencies
   ↓
Run Pytest
   ↓
Start Application
   ↓
Run Benchmark
   ↓
Compare Baseline
   ↓
Detect Regression
   ↓
Upload Results
```

---

## 🧪 Test Application

The project includes a FastAPI application specifically designed to provide deterministic endpoints for performance testing.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

### Product API

```http
GET /api/products/{product_id}
```

Example:

```http
GET /api/products/101
```

Example response:

```json
{
  "id": 101,
  "sku": "SKU-000101",
  "digest": "..."
}
```

---

### Item API

```http
POST /api/items
```

Example request:

```json
{
  "name": "Laptop",
  "value": 10
}
```

Example response:

```json
{
  "id": 10,
  "name": "Laptop",
  "status": "created"
}
```

---

### Slow Endpoint

```http
GET /api/slow
```

This endpoint intentionally introduces latency to demonstrate performance measurement and regression detection.

---

# 📁 Project Structure

```text
continuous-performance-benchmarking-platform/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── benchmark/
│   ├── __init__.py
│   ├── metrics.py
│   ├── runner.py
│   ├── regression.py
│   └── baseline.json
│
├── loadtests/
│   └── locustfile.py
│
├── tests/
│   └── test_api.py
│
├── data/
│
├── .github/
│   └── workflows/
│       └── performance.yml
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| Python         | Core implementation         |
| FastAPI        | Test API                    |
| Pytest         | API test automation         |
| HTTPX          | Benchmark HTTP client       |
| Locust         | Load testing                |
| Git            | Version control             |
| GitHub Actions | CI/CD automation            |
| JSON           | Benchmark and baseline data |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

```bash
cd continuous-performance-benchmarking-platform
```

---

## 2. Create virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Running Automated Tests

Run:

```bash
pytest -q
```

Example:

```text
3 passed
```

The tests validate:

* Health endpoint
* Product endpoint
* Item creation endpoint

---

# 📈 Running a Performance Benchmark

Run:

```bash
python -m benchmark.runner \
    --url http://127.0.0.1:8000 \
    --path /health \
    --requests 100 \
    --out data/latest.json
```

Example output:

```json
{
  "count": 100,
  "avg_ms": 3.21,
  "p50_ms": 2.94,
  "p95_ms": 4.87,
  "p99_ms": 7.31,
  "min_ms": 2.21,
  "max_ms": 8.92,
  "url": "http://127.0.0.1:8000",
  "path": "/health",
  "failures": 0,
  "success_rate": 100.0
}
```

Actual measurements depend on the machine and environment.

---

# 🔎 Running Regression Detection

Run:

```bash
python -m benchmark.regression \
    --baseline benchmark/baseline.json \
    --current data/latest.json
```

The default P95 latency regression threshold is:

```text
10%
```

The command exits with a non-zero status when a regression is detected, allowing CI/CD to block the pipeline.

---

# ⚡ Running Locust

Start Locust:

```bash
locust \
    -f loadtests/locustfile.py \
    --host http://127.0.0.1:8000
```

Open the Locust interface and configure the desired:

* Number of users
* Spawn rate
* Test duration

The test provides real-time performance information including:

```text
Requests/s
Failure %
Median
P95
P99
Average Response Time
```

---

# 🔥 Performance Regression Demonstration

The project includes an intentionally slow endpoint so regression detection can be demonstrated.

A regression can also be simulated by adding latency to an existing endpoint.

For example:

```python
@app.get("/health")
def health():

    time.sleep(0.2)

    return {
        "status": "ok"
    }
```

Run the benchmark again:

```bash
python -m benchmark.runner \
    --url http://127.0.0.1:8000 \
    --path /health \
    --requests 100 \
    --out data/latest.json
```

Then:

```bash
python -m benchmark.regression \
    --baseline benchmark/baseline.json \
    --current data/latest.json
```

The CI-style result becomes:

```text
PERFORMANCE REGRESSION DETECTED
```

After the demonstration, remove the artificial delay.

---

# 🔄 CI/CD Workflow

The GitHub Actions workflow automatically executes the performance quality gate.

```text
Git Push
   |
   v
GitHub Actions
   |
   v
Install Python
   |
   v
Install Dependencies
   |
   v
Pytest
   |
   v
Start FastAPI
   |
   v
Benchmark API
   |
   v
Calculate P95
   |
   v
Compare Baseline
   |
   +------------------+
   |                  |
   v                  v
PASS              REGRESSION
   |                  |
   v                  v
CI PASS             CI FAIL
```

Performance results are uploaded as GitHub Actions artifacts for later inspection.

---

# 🎯 Performance Quality Gate

The current implementation uses P95 latency as the primary regression signal.

Conceptually:

```text
Current P95
     |
     v
Compare with baseline
     |
     v
Calculate percentage change
     |
     v
Compare against threshold
     |
     +--------+
     |        |
     v        v
 Within     Above
 threshold  threshold
     |        |
     v        v
   PASS    REGRESSION
```

This approach can later be extended to include:

* P99 latency
* Error rate
* Throughput
* Requests per second
* Endpoint-specific thresholds
* SLA validation

---

# 🧠 Engineering Principles

The platform is designed around several performance engineering principles:

### Performance as Code

Performance checks are represented as executable code rather than manual test steps.

### Repeatable Benchmarks

Benchmarks can be executed repeatedly against the same endpoint and compared over time.

### Baseline-Driven Validation

Performance is evaluated relative to an approved baseline instead of relying on arbitrary manual observation.

### Automated Quality Gates

A detected regression can fail the CI pipeline.

### Shift-Left Performance Testing

Performance validation happens during development and pull requests rather than only before production release.

---

# 📌 Future Enhancements

The current platform provides the foundation for a larger performance engineering system.

Planned enhancements include:

```text
PostgreSQL
     ↓
Historical Benchmark Storage
     ↓
Performance Trend Analysis
     ↓
React Dashboard
     ↓
Endpoint Comparison
     ↓
SLA Management
     ↓
AI Regression Analysis
     ↓
Automated Performance Reports
     ↓
Docker
     ↓
Advanced CI/CD Gates
```

### Planned Features

* Historical benchmark database
* Performance trend dashboard
* React-based visualization
* Endpoint-level performance comparison
* SLA/SLO configuration
* Throughput regression detection
* Error-rate regression detection
* Automated HTML reports
* Dockerized test environment
* Scheduled performance testing
* AI-generated regression explanations
* Historical performance charts

---

# 💼 SDET Skills Demonstrated

This project demonstrates practical experience with:

* Python automation
* REST API testing
* Pytest
* Performance engineering
* Load testing
* Locust
* HTTPX
* Latency analysis
* P50/P95/P99 metrics
* Baseline management
* Regression detection
* CI/CD
* GitHub Actions
* Automated quality gates
* Test automation architecture

---

# 📊 Example Performance Workflow

```text
100 API Requests
       |
       v
Collect Response Times
       |
       v
Calculate Metrics
       |
       +---- Average
       +---- P50
       +---- P95
       +---- P99
       +---- Min
       +---- Max
       |
       v
Compare Against Baseline
       |
       v
Regression Analysis
       |
       +---- PASS
       |
       +---- FAIL
```

---

# 👨‍💻 Author

**Yash**

Backend & SDET-focused software engineering portfolio project.

Core interests:

```text
Python
Backend Engineering
SDET
API Automation
Performance Testing
CI/CD
Test Engineering
Quality Engineering
```

---

## ⭐ Project Goal

The ultimate goal of this project is to demonstrate how performance testing can become an automated, repeatable and continuously enforced part of modern software delivery.
