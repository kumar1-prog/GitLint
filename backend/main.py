from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc
import os

from auth import router as auth_router
from github_client import fetch_all_data
from evaluate import generate_audit_report
from database import get_db, create_tables
from models import User, AuditReport

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

app = FastAPI(title="GitLint API")

create_tables()

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
async def get_profile(username: str, request: Request, db: Session = Depends(get_db)):
    # Extract JWT from headers
    import os
    github_token = os.getenv("GITHUB_TOKEN")
    print("DEFAULT FALLBACK TOKEN:", repr(github_token))

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            from jose import jwt
            payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            print("JWT DECODED SUCCESSFULLY. Payload:", payload.keys())
            if payload.get("github_token"):
                github_token = payload.get("github_token")
                print("USING OAUTH TOKEN FROM JWT:", repr(github_token))
        except Exception as e:
            print("JWT DECODE ERROR:", e)

    print("FINAL TOKEN FOR FETCHING:", repr(github_token))
    data = await fetch_all_data(github_token, username)
    print("FETCHED DATA REPOS COUNT:", data.get("total_repos"))
    report = generate_audit_report(data)

     # Check if user already exists in DB
    user = db.query(User).filter(
        User.github_username == username
    ).first()
    # .first() returns the first matching row or None
    # Without .first() you get a Query object, not actual data

    if not user:
        # First time this user ran an audit — create their record
        user = User(
            github_username=username,
        )
        db.add(user)       # stages the insert — not saved yet
        db.commit()        # NOW it's saved to PostgreSQL
        db.refresh(user)   # reloads user from DB so we get the auto-generated id

    # Save this audit report to DB every time
    # This builds up history — future benchmark calculations use this data

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

# Add this right after app = FastAPI(...)
create_tables()  # Creates tables on startup if they don't exist