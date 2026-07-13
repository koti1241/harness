# Episode 10: AI-Powered Enterprise CI/CD Agents

## What Are These Agents?

AI agents that **automate what humans do manually** in CI/CD pipelines:

| Agent | What It Does | Replaces |
|-------|-------------|----------|
| `security_agent.py` | Reads Trivy/Gitleaks/OWASP results → generates report | Security engineer reviewing scans |
| `deployment_risk_agent.py` | Analyzes context → decides SAFE/RISKY/BLOCK | Release manager approval |
| `code_review_agent.py` | Reviews code changes → finds bugs/security issues | Senior developer code review |
| `log_analysis_agent.py` | Reads logs → finds errors/anomalies | DevOps engineer debugging |

## How They Work

```
Pipeline runs security scans (Episode 5)
         ↓
AI Security Agent reads scan results JSON
         ↓
AI analyzes: "3 CRITICAL CVEs, 0 secrets, 2 HIGH dependencies"
         ↓
AI generates: prioritized fix list + compliance status
         ↓
AI Deployment Risk Agent: "BLOCK - 3 CRITICAL vulnerabilities"
         ↓
Pipeline stops (or proceeds if SAFE)
```

## Setup (One Secret Needed)

### Option A: OpenAI (GPT-4o-mini — cheapest, ~$0.01 per pipeline run)
1. Go to: https://platform.openai.com/api-keys
2. Create API key
3. In Harness: Project Settings → Secrets → + New Secret → Text
   - Name: `openai_api_key`
   - Value: `sk-...`

### Option B: Google Gemini (Free tier — 15 requests/minute)
1. Go to: https://aistudio.google.com/apikey
2. Create API key
3. In Harness: Project Settings → Secrets → + New Secret → Text
   - Name: `gemini_api_key`
   - Value: `AIza...`

## Pipeline Flow (5 Stages)

```
Stage 1: Build & Security Scan
  ├── npm install + test
  ├── Gitleaks (secrets) ┐
  ├── Trivy (CVEs)       ├── PARALLEL
  └── npm audit (deps)   ┘

Stage 2: 🛡️ AI Security Agent
  └── Reads all scan results → generates security report

Stage 3: 🔍 AI Code Review Agent
  └── Reviews git diff → finds bugs/security issues

Stage 4: 🎯 AI Deployment Risk Agent
  └── Assesses risk → SAFE/RISKY/BLOCK decision

Stage 5: Deploy to ECR (only if AI says safe)
  ├── Create ECR repo
  └── Push image
```

## Run Locally (Test Agents)

```bash
# Set API key
export OPENAI_API_KEY="sk-your-key-here"
# OR
export GEMINI_API_KEY="AIza-your-key-here"

# Test security agent
python security_agent.py --trivy sample-trivy.json --gitleaks sample-gitleaks.json

# Test deployment risk agent
python deployment_risk_agent.py --environment production --test-status passed --changes 15

# Test code review agent
python code_review_agent.py --files "../Episode-05/node-project/src/index.js"

# Test log analysis agent
python log_analysis_agent.py --logs /var/log/syslog --type system
```

## Cost

| Provider | Model | Cost per Pipeline Run |
|----------|-------|----------------------|
| OpenAI | gpt-4o-mini | ~$0.01 (4 agent calls) |
| Gemini | gemini-1.5-flash | FREE (15 req/min limit) |

## Files

```
Episode-10/ai-agents/
├── ai_provider.py              ← Connects to OpenAI or Gemini
├── security_agent.py           ← Analyzes security scan results
├── deployment_risk_agent.py    ← Decides if deployment is safe
├── code_review_agent.py        ← Reviews code changes
├── log_analysis_agent.py       ← Analyzes logs for errors
├── requirements.txt            ← No dependencies (stdlib only!)
├── README.md                   ← This file
└── .harness/
    └── ai-agents-pipeline.yaml ← Pipeline using all agents
```

## Key Points for Video

1. **No extra dependencies** — pure Python stdlib (urllib, json, argparse)
2. **Supports both OpenAI and Gemini** — auto-detects from env var
3. **Runs in pipeline** — just `python agent.py` in a Run step
4. **Costs almost nothing** — Gemini free, OpenAI $0.01/run
5. **Replaces manual work** — what took 30 min review now takes 10 seconds
