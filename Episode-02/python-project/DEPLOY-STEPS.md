# 🚀 Deploy Python App with Local Docker Runner

## What We Built

```
python-project/
├── app.py              ← Flask web app
├── test_app.py         ← Unit tests
├── requirements.txt    ← Dependencies
├── Dockerfile          ← Docker image
├── .gitignore
└── .harness/
    └── pipeline-docker.yaml  ← Harness pipeline (Local Docker)
```

---

## Prerequisites

1. Docker Desktop installed and running
2. Harness Delegate installed (see below)
3. Code pushed to GitHub

---

## Step 1: Install Harness Docker Delegate on Your Laptop

**Prerequisites:** Docker Desktop must be installed and running on your laptop.

**Download Docker Desktop (if not installed):**
- Go to: https://www.docker.com/products/docker-desktop
- Download for Windows
- Install and restart laptop
- Open Docker Desktop → make sure it shows "Docker is running" (green)

**Screenshots:**

![Local Docker Delegate](./images/0.local-docker-delegate.png)

![Docker Delegate Install](./images/1.Docker%20Delegate%20install.png)

![Enable Auto-Upgrade for Docker Delegate](./images/2..%20enable%20auto-upgrade%20for%20Docker%20Delegate.png)

![Delegate Docker PS](./images/3.%20Delegate%20Docker%20ps.png)

![Docker Delegate Images](./images/4.%20Docker%20Delegate%20images.png)

**Now install the Delegate:**

1. Go to Harness → Project Settings → Delegates
2. Click **+ New Delegate**
3. Choose **Docker**
4. Fill in:
   - Delegate Name: `local-docker-delegate`
   - Delegate Size: Small
5. Harness gives you a `docker-compose.yml` file. Download it.
6. Open terminal (Command Prompt or PowerShell) on your laptop
7. Go to the folder where you downloaded the file:
   ```
   cd Downloads
   ```
8. Run:
   ```
   docker compose -f docker-compose.yml up -d
   ```
9. Wait 2-3 minutes
10. Go back to Harness UI → Delegates page
11. You should see: `local-docker-delegate` → Status: **Connected** ✅

**Verify it's running:**
```
docker ps
```
You should see a container named `harness-ng-delegate` running.

**If it fails:**
- Make sure Docker Desktop is running (check system tray icon)
- Make sure you have internet connection
- Try: `docker compose -f docker-compose.yml down` then `up -d` again
- Check logs: `docker logs harness-ng-delegate`

---

## Step 2: Push Code to GitHub

```bash
git add .
git commit -m "Episode 2: Python project with Docker pipeline"
git push origin master
```

---

## Step 3: Create Pipeline in Harness

1. Pipelines → Import from Git
2. Connector: your GitHub connector
3. Repo: Harness-CI-CD-Zero-to-Hero
4. Branch: master
5. YAML Path: Episode-02/python-project/.harness/pipeline-docker.yaml
6. Click Import

---

## Step 4: Run Pipeline

1. Click Run
2. Branch: master
3. Click Run Pipeline
4. Watch 3 steps execute:
   - Install Dependencies ✅
   - Run Tests ✅
   - Run App ✅

---

## Expected Output

```
=== Running Unit Tests ===
test_app.py::test_home PASSED
test_app.py::test_health PASSED
test_app.py::test_info PASSED
=== All Tests Passed! ===

=== Starting Python App ===
{'message': 'Hello from Harness CI/CD Course!', 'episode': 2, ...}
{'status': 'healthy'}
=== App Works! Pipeline Success! ===
```

---

## Run Locally (to test before pushing)

```bash
cd Episode-02/python-project
pip install -r requirements.txt
pytest test_app.py -v
python app.py
# Open browser: http://localhost:5000
```
