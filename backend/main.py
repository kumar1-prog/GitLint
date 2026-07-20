import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from auth import router as auth_router
from github_client import fetch_all_data
from evaluate import generate_audit_report

from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from models import User, AuditReport

print("=== ENV DEBUG ===")
print("CLIENT ID:", os.getenv("GITHUB_CLIENT_ID"))
print("SECRET:", os.getenv("GITHUB_CLIENT_SECRET")[:5] if os.getenv("GITHUB_CLIENT_SECRET") else "None")
print("=================")
from dotenv import load_dotenv
import os
from pathlib import Path

# Instead of just load_dotenv() which searches randomly,
# we tell it EXACTLY where the .env file is
# Path(__file__) = path of main.py itself
# .parent = the folder containing main.py (backend/)
# / ".env" = the .env file inside that folder
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

print("CLIENT ID LOADED:", os.getenv("GITHUB_CLIENT_ID"))

print("=== ENV AFTER LOAD ===")
print("CLIENT ID:", os.getenv("GITHUB_CLIENT_ID"))
print("SECRET:", os.getenv("GITHUB_CLIENT_SECRET")[:5] if os.getenv("GITHUB_CLIENT_SECRET") else "None")
print("=================")  

app = FastAPI(title="GitLint API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "GitLint API is running"}

@app.get("/profile/{username}")
async def get_profile(username: str, db: Session = Depends(get_db)):
    
    # Check if audit exists within last 24 hours
    from datetime import datetime, timedelta
    recent = db.query(AuditReport).filter(
        AuditReport.github_username == username,
        AuditReport.created_at > datetime.utcnow() - timedelta(hours=24)
    ).first()

    if recent:
        # Serve from DB — no GitHub API call needed!
        return recent.full_report

    # No recent audit — fetch fresh from GitHub
    token = os.getenv("GITHUB_TEST_TOKEN")
    data = await fetch_all_data(token, username)
    report = generate_audit_report(data)

    # Save to DB as usual
    audit = AuditReport(
        github_username=username,
        overall_score=report["overall_score"],
        consistency_score=report["signals"]["commit_consistency"]["score"],
        fork_ratio_score=report["signals"]["fork_ratio"]["score"],
        readme_score=report["signals"]["readme_quality"]["score"],
        diversity_score=report["signals"]["language_diversity"]["score"],
        depth_score=report["signals"]["project_depth"]["score"],
        benchmark_score=report["signals"]["peer_benchmark"]["score"],
        full_report=report,
    )
    db.add(audit)
    db.commit()

    return report

@app.get("/benchmarks")
def get_benchmarks(db: Session = Depends(get_db)):
    from sqlalchemy import func as sqlfunc

    # AVG() across all stored audits = real peer averages
    # This is what makes the benchmark signal genuinely data-driven
    result = db.query(
        sqlfunc.avg(AuditReport.consistency_score),
        sqlfunc.avg(AuditReport.fork_ratio_score),
        sqlfunc.avg(AuditReport.readme_score),
        sqlfunc.avg(AuditReport.diversity_score),
        sqlfunc.avg(AuditReport.depth_score),
    ).first()

    return {
        "avg_consistency": round(result[0] or 45),
        "avg_fork_ratio": round(result[1] or 55),
        "avg_readme": round(result[2] or 35),
        "avg_diversity": round(result[3] or 50),
        "avg_depth": round(result[4] or 40),
        # "or 45" = fallback if table is empty (no audits yet)
    }

# Add this import at top
from database import create_tables

# Add this right after app = FastAPI(...)
create_tables()  # Creates tables on startup if they don't exist