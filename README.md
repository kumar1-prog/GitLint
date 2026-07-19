# GitLint — GitHub Profile Audit Tool

> See your GitHub the way recruiters do.

GitLint analyzes your GitHub profile across 6 recruiter-relevant signals and generates a blind spot report — showing exactly what's helping and hurting your chances before a recruiter even reads your resume.

---

## The Problem

Every CS student has a GitHub. But most profiles silently fail recruiter review without the candidate knowing why. Recruiters spend ~30 seconds on a GitHub profile — GitLint simulates that scan and tells you what they see.

---

## How It Works


<img width="2720" height="2320" alt="devdeck_architecture" src="https://github.com/user-attachments/assets/89bf7116-f7db-4b1f-90e9-ddf53b7b4b68" />

1. Login with GitHub OAuth
2. GitLint fetches your public repositories, commit history, and README content
3. A scoring engine evaluates your profile across 6 signals
4. You receive a blind spot report with an overall recruiter score and peer benchmark

---

## 6 Scoring Signals

| Signal | What It Measures |
|---|---|
| **Commit Consistency** | Do you code regularly or only before deadlines? |
| **Original Work Ratio** | What % of repos are your own vs forked? |
| **README Quality** | Do your projects look professional and documented? |
| **Language Diversity** | Do you show breadth across multiple languages? |
| **Project Depth** | Do your projects have real weight — stars, issues, size? |
| **Peer Benchmark** | How do you compare to other GitLint users? |

---

## Tech Stack

**Backend**
- Python + FastAPI
- PostgreSQL + SQLAlchemy
- GitHub OAuth 2.0 + JWT authentication
- httpx for async GitHub API calls

**Frontend**
- React + Vite
- React Router for SPA navigation
- Axios for API calls
- SessionStorage for secure token handling

---

## Architecture

```
User
 │
 ▼
React Frontend (Vite)
 │  GitHub OAuth login
 │  Audit loading screen
 │  Report dashboard
 │
 ▼
FastAPI Backend
 │  /auth/login      → redirects to GitHub OAuth
 │  /auth/callback   → exchanges code for token, issues JWT
 │  /profile/{user}  → fetches GitHub data + runs scoring engine
 │  /benchmarks      → returns real peer averages from DB
 │
 ├──► GitHub REST API (repos, commits, READMEs)
 │
 └──► PostgreSQL (users, audit history, peer benchmarks)
```

---



## Security Design

- GitHub OAuth scoped to `read:user` and `public_repo` only — no private repo access
- GitHub access token wrapped in our own JWT — never exposed to the browser directly
- JWT expires in 24 hours
- Tokens stored in `sessionStorage` — cleared when tab closes
- Minimum permission principle applied throughout (Backend for Frontend pattern)

---

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-dotenv httpx sqlalchemy psycopg2-binary python-jose
```

Create `backend/.env`:
```
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
JWT_SECRET=your_random_secret_string
DATABASE_URL=postgresql://localhost/gitlint
FRONTEND_URL=http://127.0.0.1:5173
GITHUB_TEST_TOKEN=your_personal_access_token
```

```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend/git_lint
npm install
npm run dev
```

### GitHub OAuth App Setup

1. Go to `github.com/settings/developers`
2. New OAuth App
3. Homepage URL: `http://127.0.0.1:8000`
4. Callback URL: `http://127.0.0.1:8000/auth/callback`
5. Copy Client ID and Secret into `.env`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/auth/login` | Redirects to GitHub OAuth |
| GET | `/auth/callback` | Handles OAuth callback, issues JWT |
| GET | `/profile/{username}` | Runs full audit, saves to DB |
| GET | `/benchmarks` | Returns real peer average scores |

---

## Database Schema

**users** — GitHub username, avatar, created timestamp

**audit_reports** — Per-signal scores, overall score, full JSON report, timestamp

Peer benchmark scores are calculated as live SQL averages across all stored audits — not hardcoded values.

---

## Project Structure

```
gitlint/
├── backend/
│   ├── main.py          # FastAPI app, routes
│   ├── auth.py          # GitHub OAuth + JWT logic
│   ├── github_client.py # GitHub API data fetching
│   ├── evaluate.py      # 6 signal scoring engine
│   ├── database.py      # PostgreSQL connection + session
│   └── models.py        # SQLAlchemy table definitions
└── frontend/git_lint/
    └── src/
        └── pages/
            ├── Landing.jsx   # Login page
            ├── Callback.jsx  # OAuth token handler
            ├── Audit.jsx     # Loading screen
            └── Report.jsx    # Score dashboard
```

---

## Key Engineering Decisions

**Why JWT over raw GitHub token?**
Wrapping GitHub's token in our own JWT means we control expiry, can invalidate sessions, and never expose the raw GitHub token to the browser. This is the Backend for Frontend (BFF) security pattern.

**Why top 10 repos only?**
Each repo requires 2 API calls (README + commit stats). Analyzing 100 repos = 200 calls per request. Top 10 sorted by `updated_at` gives the most relevant signal while staying well within GitHub's rate limits.

**Why individual score columns + JSON blob?**
Individual columns allow fast SQL aggregations for peer benchmarks (`SELECT AVG(readme_score)`). The JSON blob stores the full report for frontend display without multiple joins.

---

## Author

**Krishna Kumar G**
B.Tech AI & Data Science — SASTRA Deemed University

[GitHub](https://github.com/kumar1-prog) · [LinkedIn](https://www.linkedin.com/in/g-krishna-kumar-731861218)
