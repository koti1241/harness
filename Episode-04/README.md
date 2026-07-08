# Episode 4: Build Your First Enterprise CI Pipeline

## 🎯 Goal
Build a REAL production-ready CI pipeline that builds, tests, and pushes a Docker image.
Like building an assembly line in a factory.

---

## 📚 Topics Covered

### 1. Pipeline Concepts

```
┌─────────────────────────────────────────────────────────┐
│  PIPELINE                                                │
│  ════════                                                │
│                                                          │
│  A Pipeline = A series of steps to build & deploy code   │
│                                                          │
│  Think of it like a RECIPE:                              │
│  1. Get ingredients (Clone code)                         │
│  2. Mix them (Install dependencies)                      │
│  3. Taste test (Run tests)                               │
│  4. Bake (Build application)                             │
│  5. Package (Create Docker image)                        │
│  6. Deliver (Push to registry)                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

### 2. Pipeline Structure

```
Stage 1: build-cpp
  ├── Install Dependencies
  ├── Unit Tests
  ├── Build Application
  ├── Push to Docker Hub
  └── Verify Docker Hub

Stage 2: push-to-ecr
  ├── Push to ECR
  ├── Verify ECR Image (AWS CLI)
  └── Final Summary

Stage 3: cleanup-dockerhub
  ├── Wait 2 minutes
  └── Delete Docker Hub Repo + Verify

Stage 4: cleanup-ecr
  └── Delete ECR Images + Repo + Verify
```

```
Pipeline
├── Stage 1: "Build & Test"
│   ├── Step 1: Clone Repository
│   ├── Step 2: Install Dependencies
│   ├── Step 3: Run Unit Tests
│   ├── Step 4: Build Application
│   └── Step 5: Build & Push Docker Image
│
├── Stage 2: "Security Scan" (Episode 5)
│
└── Stage 3: "Deploy" (Episode 6)
```

**Key Terms:**
| Term | What it is | Analogy |
|------|-----------|---------|
| Pipeline | The whole workflow | The entire recipe |
| Stage | A group of related steps | A chapter in the recipe |
| Step | A single action | One instruction |
| Variable | A reusable value | An ingredient amount |
| Expression | Dynamic value | "Add salt to taste" |

---

### 3. Variables & Runtime Inputs

```
VARIABLES (Set once, use everywhere):
═════════
pipeline:
  variables:
    - name: docker_repo
      type: String
      value: "myuser/myapp"
    - name: docker_tag
      type: String
      value: "latest"

RUNTIME INPUTS (Ask user when pipeline runs):
══════════════
pipeline:
  variables:
    - name: environment
      type: String
      value: <+input>    ← This asks "which environment?" every run

EXPRESSIONS (Dynamic values from Harness):
═══════════
<+pipeline.sequenceId>     → Build number (1, 2, 3...)
<+trigger.commitSha>       → Git commit hash
<+codebase.branch>         → Current branch name
<+variable.docker_repo>    → Your variable value
```

---

### 4. Git Experience

```
┌─────────────────────────────────────────────────┐
│  GIT EXPERIENCE                                   │
│  ══════════════                                   │
│                                                   │
│  Store pipeline YAML in Git (not just in Harness) │
│                                                   │
│  Why?                                             │
│  • Version control for pipelines                  │
│  • Code review for pipeline changes              │
│  • Same Git workflow for code AND pipelines       │
│  • Rollback pipeline changes easily              │
│                                                   │
│  Where pipeline lives:                           │
│  your-repo/                                      │
│  └── .harness/                                   │
│      └── my-pipeline.yaml                        │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

### 5. Templates

```
Templates = Reusable pipeline pieces

Example: You have 10 microservices.
All need the same CI pipeline.

WITHOUT Templates:
  Copy-paste pipeline 10 times 😫
  Change one thing? Update all 10 😫😫

WITH Templates:
  Create 1 template
  Use it in all 10 projects 😊
  Change once → All 10 update 😊😊

Template Types:
  • Step Template (reuse a single step)
  • Stage Template (reuse a whole stage)
  • Pipeline Template (reuse entire pipeline)
```

---

## 🖥️ Deploy This Pipeline — Step by Step

---

### Prerequisites (Already Done in Previous Episodes)

| What | Where to Find Steps |
|------|-------------------|
| GitHub Connector | [Episode 1 — DEPLOY-STEPS.md](../Episode-01/hello-world-app/DEPLOY-STEPS.md#step-3-create-a-github-connector-first-time-only) |
| Docker Hub Secret + Variable | [Episode 2 — README.md (Step 3-4)](../Episode-02/README.md#step-3-add-a-secret) |
| Docker Hub Connector | [Episode 2 — README.md (Step 5)](../Episode-02/README.md#step-5-create-docker-hub-connector) |
| AWS Connector (OIDC) | [Episode 3 — README.md (Connector 3)](../Episode-03/README.md#connector-3-aws--🆕-create-now-using-oidc--no-access-keys) |
| AWS Access Key Secrets | [Episode 3 — Terraform README (Step 2-3)](../Episode-03/terraform-project/README.md#step-2-get-aws-access-key--secret-key) |

---

### Step 1: Add Variable `aws_account_id` in Harness

1. Go to Project Settings → Variables → + New Variable
2. Name: `aws_account_id`
3. Value: your 12-digit AWS account ID (e.g. `713939171080`)
4. Save

---

### Step 2: Push Code to GitHub

```bash
cd Harness-CI-CD-Zero-to-Hero
git add .
git commit -m "Episode 4: C++ enterprise CI pipeline"
git push origin master
```

---

### Step 3: Import Pipeline in Harness

1. Pipelines → Import from Git
2. Connector: Github
3. Repo: Harness-CI-CD-Zero-to-Hero
4. Branch: master
5. YAML Path: `Episode-04/cpp-project/.harness/pipeline.yaml`
6. Click Import

---

### Step 4: Run the Pipeline

1. Click Run
2. Fill in runtime inputs:
   - `deploy_version`: type `1.0.0`
   - `environment`: select `development` (or any)
   - Branch: `master`
3. Click Run Pipeline

---

### Step 5: Watch 5 Stages Execute

```
Stage 1: build-cpp
  ├── Install Dependencies ✅
  ├── Unit Tests ✅
  ├── Build Application ✅
  ├── Push to Docker Hub ✅
  └── Verify Docker Hub ✅

Stage 2: push-to-ecr
  ├── Create ECR Repo ✅
  ├── Push to ECR ✅
  ├── Verify ECR Image ✅
  └── Final Summary ✅

Stage 3: approval-to-delete ⏸️
  └── Approve Cleanup (click Approve or Reject)

Stage 4 & 5 (Parallel — runs only after Approval):
  ├── cleanup-dockerhub (delete repo) ✅
  └── cleanup-ecr (delete images + repo) ✅
```

---

### Expected Output (Final Summary)

```
=========================================
  ENTERPRISE CI PIPELINE COMPLETE!

  Version: 1.0.0
  Environment: development

  Stage 1: Build + Docker Hub ✅
  Stage 2: Amazon ECR ✅

  Docker Hub: yaswanth111/cpp-harness-app:1.0.0-development
  ECR: 713939171080.dkr.ecr.us-east-1.amazonaws.com/cpp-harness-app:1.0.0-development

  All Tags:
    - 1.0.0-development
    - 1
    - latest
=========================================
```

---

### Connectors & Secrets Summary

| Resource | Name | Type | Created In |
|----------|------|------|-----------|
| GitHub Connector | `Github` | Account level | Episode 1 |
| Docker Hub Connector | `dockerhub` | Project level | Episode 2 |
| AWS Connector (OIDC) | `aws_account` | Project level | Episode 3 |
| Secret: Docker Hub token | `docker-hub-password` | Project | Episode 2 |
| Secret: AWS Access Key | `aws_access_key_id` | Project | Episode 3 |
| Secret: AWS Secret Key | `aws_secret_access_key` | Project | Episode 3 |
| Variable: Docker username | `docker_username` | Project | Episode 2 |
| Variable: AWS Account ID | `aws_account_id` | Project | Episode 4 |

---

### Project Structure

```
Episode-04/cpp-project/
├── src/main.cpp                  ← C++ HTTP server
├── tests/test_main.cpp           ← Unit tests
├── CMakeLists.txt                ← Build system
├── Dockerfile                    ← Multi-stage Docker build
├── Templates.md                  ← Template documentation
├── .gitignore
└── .harness/
    ├── pipeline.yaml             ← Main pipeline (5 stages)
    └── template-pipeline.yaml    ← Reusable template (any language)
```

---

> 🎬 Next Episode: [Episode 5 - Advanced CI & DevSecOps](../Episode-05/README.md)
