"""
Deployment Risk Agent — Analyzes pipeline context and decides if deployment is safe.

What it checks:
  1. Security scan results (any CRITICAL vulnerabilities?)
  2. Test results (all tests passed?)
  3. Code changes (how many files changed? high-risk files?)
  4. Environment (production = stricter checks)
  5. Time of day (deploying at 5 PM Friday? risky!)

Usage in pipeline:
  python deployment_risk_agent.py --environment production --test-status passed --security-status passed --changes 5

Output: SAFE / RISKY / BLOCK with explanation
"""

import argparse
import json
import os
import sys
from datetime import datetime
from ai_provider import get_ai_response


def assess_risk(environment, test_status, security_status, files_changed, 
                deploy_time=None, trivy_critical=0, secrets_found=0):
    """
    Assess deployment risk based on multiple factors.
    Returns risk score and recommendation.
    """
    
    # Current time risk
    if deploy_time is None:
        deploy_time = datetime.now()
    
    hour = deploy_time.hour
    weekday = deploy_time.weekday()  # 0=Monday, 6=Sunday
    
    context = {
        "environment": environment,
        "test_status": test_status,
        "security_status": security_status,
        "files_changed": files_changed,
        "deploy_hour": hour,
        "deploy_day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][weekday],
        "trivy_critical_vulns": trivy_critical,
        "secrets_found": secrets_found,
        "is_friday_evening": weekday == 4 and hour >= 16,
        "is_weekend": weekday >= 5,
        "is_after_hours": hour < 6 or hour > 22
    }

    prompt = f"""You are a Deployment Risk Assessment Agent for enterprise CI/CD.
Analyze this deployment context and provide a risk assessment.

## Deployment Context
{json.dumps(context, indent=2)}

## Risk Rules:
- BLOCK if: secrets found > 0, or CRITICAL vulnerabilities > 0, or tests failed
- RISKY if: deploying to production on Friday evening/weekend, or > 20 files changed, or HIGH vulnerabilities
- SAFE if: all tests pass, no critical/high vulns, < 20 files changed, business hours

Provide:
1. RISK LEVEL: SAFE ✅ / RISKY ⚠️ / BLOCK ❌
2. RISK SCORE: 1-10 (1=no risk, 10=extreme risk)
3. DECISION: "PROCEED WITH DEPLOYMENT" or "DELAY DEPLOYMENT" or "BLOCK DEPLOYMENT"
4. REASONS: bullet points explaining why
5. RECOMMENDATIONS: what to do before deploying (if risky/blocked)

Be concise. Max 15 lines."""

    print("=" * 60)
    print("  🎯 AI DEPLOYMENT RISK AGENT — ASSESSMENT")
    print("=" * 60)
    print()
    print(f"  Environment:     {environment}")
    print(f"  Tests:           {test_status}")
    print(f"  Security:        {security_status}")
    print(f"  Files Changed:   {files_changed}")
    print(f"  Deploy Time:     {context['deploy_day']} {hour}:00")
    print(f"  Critical Vulns:  {trivy_critical}")
    print(f"  Secrets Found:   {secrets_found}")
    print()
    
    response = get_ai_response(prompt)
    print(response)
    
    print()
    print("=" * 60)
    
    # Determine exit code for pipeline
    if "BLOCK" in response.upper() and "BLOCK DEPLOYMENT" in response.upper():
        print("  ❌ Pipeline should STOP here.")
        return 1  # Non-zero = fail pipeline
    elif "RISKY" in response.upper():
        print("  ⚠️  Proceed with caution. Manual approval recommended.")
        return 0
    else:
        print("  ✅ Safe to deploy.")
        return 0


def main():
    parser = argparse.ArgumentParser(description="AI Deployment Risk Agent")
    parser.add_argument("--environment", default="development", 
                       choices=["development", "testing", "staging", "production"])
    parser.add_argument("--test-status", default="passed", choices=["passed", "failed"])
    parser.add_argument("--security-status", default="passed", choices=["passed", "failed"])
    parser.add_argument("--changes", type=int, default=5, help="Number of files changed")
    parser.add_argument("--trivy-critical", type=int, default=0, help="Critical vulnerabilities count")
    parser.add_argument("--secrets-found", type=int, default=0, help="Secrets found by Gitleaks")
    args = parser.parse_args()

    print("🎯 Deployment Risk Agent starting...")
    print()

    exit_code = assess_risk(
        environment=args.environment,
        test_status=args.test_status,
        security_status=args.security_status,
        files_changed=args.changes,
        trivy_critical=args.trivy_critical,
        secrets_found=args.secrets_found
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
