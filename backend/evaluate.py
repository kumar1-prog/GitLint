import math

# ============================================================
# SIGNAL 1: Commit Consistency Score (0-100)
# ============================================================
def score_commit_consistency(repo_details: list) -> dict:
    all_weekly = []

    for repo in repo_details:
        weekly = repo.get("weekly_commits", [])
        all_weekly.extend(weekly)

    if not all_weekly or sum(all_weekly) == 0:
        return {"score": 0, "reason": "No commit history found", "improvement": "Push code to public repositories regularly. Even small, frequent commits are better than none at all."}

    active_weeks = sum(1 for w in all_weekly if w > 0)
    total_weeks = len(all_weekly)
    consistency_ratio = active_weeks / total_weeks

    mean = sum(all_weekly) / total_weeks
    variance = sum((w - mean) ** 2 for w in all_weekly) / total_weeks
    std_dev = math.sqrt(variance)

    consistency_penalty = min(std_dev / 10, 1.0)
    raw_score = (consistency_ratio * 0.6) + ((1 - consistency_penalty) * 0.4)
    final_score = round(raw_score * 100)

    if final_score >= 70:
        reason = f"Coding {active_weeks} out of {total_weeks} weeks - strong habit"
        improvement = "Excellent consistency! Keep maintaining this steady cadence, it shows great discipline to recruiters."
    elif final_score >= 40:
        reason = f"Coding {active_weeks} out of {total_weeks} weeks - somewhat sporadic"
        improvement = "Try to avoid 'batching' your code pushes. Commit and push your progress as you complete logical chunks."
    else:
        reason = f"Only {active_weeks} active weeks - looks like deadline-driven coding"
        improvement = "Your commit graph looks very bursty. Recuiters look for steady momentum. Try to make at least one meaningful commit every week."

    return {"score": final_score, "reason": reason, "improvement": improvement}


# ============================================================
# SIGNAL 2: Fork Ratio Score (0-100)
# ============================================================
def score_fork_ratio(total_repos: int, forked_repos: int, original_repos: int) -> dict:
    if total_repos == 0:
        return {"score": 0, "reason": "No repositories found", "improvement": "Start your first original project! It can be as simple as a to-do app."}

    original_ratio = original_repos / total_repos
    final_score = round(original_ratio * 100)

    if final_score >= 70:
        reason = f"{original_repos} original repos out of {total_repos} - solid original work"
        improvement = "You have a great ratio of original work. Keep focusing on building your own projects from scratch."
    elif final_score >= 40:
        reason = f"Only {original_repos} original repos - too many forks pulling score down"
        improvement = "You have quite a few forked repos. Consider pinning your original projects to your profile, or making old tutorial forks private."
    else:
        reason = f"Mostly forks ({forked_repos}) - recruiters want to see YOUR code, not copies"
        improvement = "Recruiters cannot evaluate your skills if your profile is mostly forked code. Build original projects or contribute explicitly to those forks."

    return {"score": final_score, "reason": reason, "improvement": improvement}


# ============================================================
# SIGNAL 3: README Quality Score (0-100)
# ============================================================
def score_readme_quality(repo_details: list) -> dict:
    if not repo_details:
        return {"score": 0, "reason": "No repositories to evaluate", "improvement": "Add a repository with a detailed README."}

    repo_scores = []
    for repo in repo_details:
        readme = repo.get("readme", "")
        repo_score = 0

        if len(readme) > 50: repo_score += 20
        if len(readme) > 300: repo_score += 20
        if any(word in readme.lower() for word in ["install", "setup", "getting started", "run", "usage"]): repo_score += 20
        if "```" in readme: repo_score += 20
        if any(word in readme.lower() for word in ["screenshot", "demo", "preview", "gif", "http", "https"]): repo_score += 20

        repo_scores.append(repo_score)

    avg_score = round(sum(repo_scores) / len(repo_scores))

    if avg_score >= 70:
        reason = "READMEs are detailed and professional"
        improvement = "Outstanding documentation! Your projects look highly professional and are easy for others to onboard onto."
    elif avg_score >= 40:
        reason = "READMEs exist but lack setup instructions or demos"
        improvement = "Your READMEs are a bit sparse. Add installation steps, usage examples with code blocks, and visual screenshots to grab attention."
    else:
        reason = "Most READMEs are empty or missing - biggest blind spot"
        improvement = "A missing README makes a project look abandoned. At minimum, add a functional description and setup instructions to your top 3 pinned repos."

    return {"score": avg_score, "reason": reason, "improvement": improvement}


# ============================================================
# SIGNAL 4: Language Diversity Score (0-100)
# ============================================================
def score_language_diversity(repo_details: list) -> dict:
    languages = set()
    for repo in repo_details:
        lang = repo.get("language")
        if lang:
            languages.add(lang)

    count = len(languages)
    final_score = min(count * 20, 100)

    if count == 0:
        reason = "No languages detected - repos may be empty"
        improvement = "Commit some source code to your repositories so GitHub can detect your tech stack."
    elif count == 1:
        reason = f"Only {list(languages)[0]} - consider showing breadth"
        improvement = "Being highly specialized is okay, but recruiters often look for adaptability. Consider completing a small side project in a secondary language."
    elif count <= 3:
        reason = f"Uses {', '.join(languages)} - decent range"
        improvement = "You show a solid, focused tech stack. Make sure you highlight your strongest language in your pinned repositories."
    else:
        reason = f"Works across {count} languages: {', '.join(languages)}"
        improvement = "Excellent breadth! You demonstrate high adaptability across different ecosystems. Be prepared to discuss architectural tradeoffs between them."

    return {"score": final_score, "reason": reason, "languages": list(languages), "improvement": improvement}


# ============================================================
# SIGNAL 5: Project Depth Score (0-100)
# ============================================================
def score_project_depth(repo_details: list) -> dict:
    if not repo_details:
        return {"score": 0, "reason": "No original repositories found", "improvement": "Host a fully fleshed out project on your GitHub to demonstrate depth."}

    depth_scores = []
    for repo in repo_details:
        repo_score = 0
        stars = repo.get("stars", 0)
        issues = repo.get("open_issues", 0)
        size = repo.get("size", 0) 
        description = repo.get("description", "")

        if stars > 0: repo_score += min(math.log(stars + 1) * 10, 40)
        if issues > 0: repo_score += 20
        if size > 100: repo_score += 20
        if description and len(description) > 10: repo_score += 20

        depth_scores.append(min(repo_score, 100))

    avg_depth = round(sum(depth_scores) / len(depth_scores))

    if avg_depth >= 70:
        reason = "Projects show real depth - stars, issues, substantial code"
        improvement = "Your repositories look like real-world, mature software. Keep fostering community engagement through issues and PRs!"
    elif avg_depth >= 40:
        reason = "Some depth but projects lack descriptions or community traction"
        improvement = "Your projects have some substance, but look a bit isolated. Add detailed GitHub repository descriptions and open a few generic 'good first issues'."
    else:
        reason = "Projects look shallow - small size, no stars, no descriptions"
        improvement = "Your projects look like fast tutorials or homework assignments. Try building one large, deeply integrated application to demonstrate architectural skills."

    return {"score": avg_depth, "reason": reason, "improvement": improvement}


# ============================================================
# SIGNAL 6: Peer Benchmark Score (0-100)
# ============================================================
def score_peer_benchmark(consistency, fork_ratio, readme, diversity, depth, avg_consistency=45, avg_fork_ratio=55, avg_readme=35, avg_diversity=50, avg_depth=40) -> dict:
    deltas = [
        consistency - avg_consistency,
        fork_ratio - avg_fork_ratio,
        readme - avg_readme,
        diversity - avg_diversity,
        depth - avg_depth,
    ]
    avg_delta = sum(deltas) / len(deltas)
    final_score = round(max(0, min(100, 50 + avg_delta)))

    if final_score >= 70:
        reason = "Above average compared to other DevDeck users"
        improvement = "You are currently ranking in the top percentiles. Use your GitHub as a strong focal point on your resume."
    elif final_score >= 45:
        reason = "Around average - room to stand out more"
        improvement = "You have a baseline profile. Pick one specific area (like READMEs or project depth) to polish to jump into the elite tier."
    else:
        reason = "Below average - focus on README quality and consistency"
        improvement = "Your profile is currently throwing multiple red flags compared to peers. Start by cleaning up your forks and writing one stellar README."

    return {"score": final_score, "reason": reason, "improvement": improvement}


# ============================================================
# MASTER FUNCTION - runs all 6 signals and returns full report
# ============================================================
def generate_audit_report(data: dict) -> dict:
    repo_details = data.get("repo_details", [])
    total_repos = data.get("total_repos", 0)
    forked_repos = data.get("forked_repos", 0)
    original_repos = data.get("original_repos", 0)

    consistency = score_commit_consistency(repo_details)
    fork_ratio = score_fork_ratio(total_repos, forked_repos, original_repos)
    readme = score_readme_quality(repo_details)
    diversity = score_language_diversity(repo_details)
    depth = score_project_depth(repo_details)

    benchmark = score_peer_benchmark(
        consistency["score"],
        fork_ratio["score"],
        readme["score"],
        diversity["score"],
        depth["score"],
    )

    overall = round(
        consistency["score"] * 0.20 +
        fork_ratio["score"] * 0.15 +
        readme["score"] * 0.25 +
        diversity["score"] * 0.15 +
        depth["score"] * 0.15 +
        benchmark["score"] * 0.10
    )

    blind_spots = []
    signals = {
        "Commit consistency": consistency,
        "Original work ratio": fork_ratio,
        "README quality": readme,
        "Language diversity": diversity,
        "Project depth": depth,
    }
    
    # Check score within the dictionary structure
    for signal_name, signal_data in signals.items():
        if signal_data["score"] < 50:
            blind_spots.append(signal_name)

    return {
        "username": data.get("username"),
        "overall_score": overall,
        "blind_spots": blind_spots,
        "signals": {
            "commit_consistency": consistency,
            "fork_ratio": fork_ratio,
            "readme_quality": readme,
            "language_diversity": diversity,
            "project_depth": depth,
            "peer_benchmark": benchmark,
        }
    }