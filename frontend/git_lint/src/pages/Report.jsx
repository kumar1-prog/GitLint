import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import Logo from "../assets/logo.png"


// ── Score color utility ─────────────────────────────────────
const getScore = (s) => ({
    color: s >= 70 ? "var(--green)" : s >= 50 ? "var(--yellow)" : "var(--red)",
    shadow: s >= 70 ? "var(--shadow-green)" : s >= 50 ? "0 0 20px rgba(255,182,39,0.3)" : "var(--shadow-red)",
    grade: s >= 80 ? "Excellent" : s >= 60 ? "Good" : s >= 40 ? "Fair" : "Needs Work",
})

// ── Signal Card ─────────────────────────────────────────────
function SignalCard({ title, score, reason, improvement, isBlindSpot }) {
    const sc = getScore(score)

    return (
        <div className="glass-card" style={{
            padding: "1.75rem",
            display: "flex",
            flexDirection: "column",
            gap: "0",
            border: isBlindSpot
                ? "1px solid rgba(255,77,109,0.3)"
                : "1px solid var(--border-subtle)",
            boxShadow: isBlindSpot ? "var(--shadow-red)" : "var(--shadow-card)",
        }}>
            {/* Glow orb top-right */}
            <div style={{
                position: "absolute",
                top: "-20px", right: "-20px",
                width: "80px", height: "80px",
                background: sc.color,
                filter: "blur(40px)",
                opacity: 0.18,
                pointerEvents: "none"
            }} />

            {/* Title + Score Row */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem" }}>
                <div>
                    {isBlindSpot && (
                        <span className="blind-spot-badge" style={{ display: "block", marginBottom: "0.5rem", fontSize: "0.7rem" }}>
                            ⚠ Blind Spot
                        </span>
                    )}
                    <span style={{ fontWeight: "600", fontSize: "0.95rem", color: "var(--t-primary)" }}>
                        {title}
                    </span>
                </div>
                <div style={{ textAlign: "right", flexShrink: 0, marginLeft: "1rem" }}>
                    <div style={{
                        fontSize: "1.8rem",
                        fontWeight: "800",
                        color: sc.color,
                        lineHeight: 1,
                        filter: `drop-shadow(0 0 8px ${sc.color}80)`
                    }}>
                        {score}
                    </div>
                    <div style={{ fontSize: "0.7rem", color: "var(--t-tertiary)", fontWeight: "500", marginTop: "0.15rem" }}>
                        {sc.grade}
                    </div>
                </div>
            </div>

            {/* Progress Bar */}
            <div className="progress-track" style={{ marginBottom: "1rem" }}>
                <div className="progress-fill" style={{
                    width: `${score}%`,
                    background: `linear-gradient(90deg, ${sc.color}80, ${sc.color})`,
                    boxShadow: `0 0 8px ${sc.color}60`
                }} />
            </div>

            {/* Reason */}
            <p style={{
                color: "var(--t-secondary)",
                fontSize: "0.875rem",
                lineHeight: "1.55",
                marginBottom: improvement ? "1rem" : "0"
            }}>
                {reason}
            </p>

            {/* Improvement Panel */}
            {improvement && (
                <div className="advice-panel">
                    <p style={{
                        fontSize: "0.7rem",
                        fontWeight: "700",
                        letterSpacing: "0.07em",
                        textTransform: "uppercase",
                        color: "#7c6cf8",
                        marginBottom: "0.4rem"
                    }}>
                        💡 How to improve
                    </p>
                    <p style={{ fontSize: "0.85rem", color: "var(--t-primary)", lineHeight: "1.5" }}>
                        {improvement}
                    </p>
                </div>
            )}
        </div>
    )
}

// ── Report Page ─────────────────────────────────────────────
export default function Report() {
    const [report, setReport] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        const stored = sessionStorage.getItem("devdeck_report")
        if (!stored) { navigate("/"); return }
        setReport(JSON.parse(stored))
    }, [])

    if (!report) return null

    const { overall_score, blind_spots, signals, username } = report
    const sc = getScore(overall_score)

    const signalList = [
        { key: "commit_consistency", title: "Commit Consistency" },
        { key: "fork_ratio", title: "Original Work Ratio" },
        { key: "readme_quality", title: "README Quality" },
        { key: "language_diversity", title: "Language Diversity" },
        { key: "project_depth", title: "Project Depth" },
        { key: "peer_benchmark", title: "Peer Benchmark" },
    ]

    return (
        <div style={{ position: "relative", minHeight: "100vh", zIndex: 1 }}>
            {/* Ambient orbs */}
            <div className="orb orb-1" />
            <div className="orb orb-2" />
            <div className="grid-overlay" />

            {/* Navbar */}
            <nav className="navbar">
                <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
                    <img
                        src={Logo}
                        alt="GitLint logo"
                        style={{ height: "70px", width: "auto", objectFit: "contain" }}
                    />
                    <span style={{ fontWeight: "800", fontSize: "1.5rem", letterSpacing: "-0.02em" }}>
                        Git<span className="gradient-text">Lint</span>
                    </span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                    <span style={{
                        fontSize: "0.875rem",
                        color: "var(--t-secondary)",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.4rem"
                    }}>
                        <div style={{
                            width: "8px", height: "8px",
                            borderRadius: "50%",
                            background: "var(--green)",
                            boxShadow: "var(--shadow-green)"
                        }} />
                        @{username}
                    </span>
                    <button
                        className="btn-ghost"
                        onClick={() => { sessionStorage.clear(); navigate("/") }}
                    >
                        Log out
                    </button>
                </div>
            </nav>

            {/* Main Content */}
            <div style={{
                maxWidth: "1100px",
                margin: "0 auto",
                padding: "3rem 2rem 6rem",
                position: "relative",
                zIndex: 10

            }}>
                {/* Hero Score Card */}
                <div className="spotlight-card fade-up" style={{ padding: "4rem 3rem", textAlign: "center", marginBottom: "3rem" }}>
                    {/* Score glow */}
                    <div style={{
                        position: "absolute",
                        inset: 0,
                        background: `radial-gradient(circle at 50% 70%, ${sc.color}14 0%, transparent 60%)`,
                        pointerEvents: "none"
                    }} />

                    <div style={{ position: "relative", zIndex: 1 }}>
                        <div style={{ marginBottom: "1.5rem" }}>
                            <span className="label-tag">GitLint Recruiter Report</span>
                        </div>

                        {/* Big Score Number */}
                        <div style={{
                            fontSize: "clamp(5rem, 15vw, 9rem)",
                            fontWeight: "900",
                            lineHeight: 1,
                            color: sc.color,
                            filter: `drop-shadow(0 0 40px ${sc.color}50)`,
                            letterSpacing: "-0.04em",
                            marginBottom: "0.25rem"
                        }}>
                            {overall_score}
                        </div>
                        <div style={{
                            fontSize: "1rem",
                            color: "var(--t-tertiary)",
                            fontWeight: "500",
                            letterSpacing: "0.15em",
                            textTransform: "uppercase",
                            marginBottom: "0.75rem"
                        }}>
                            out of 100
                        </div>
                        <p style={{ color: "var(--t-secondary)", fontSize: "1.05rem" }}>
                            AI recruiter score for{" "}
                            <span style={{ color: "var(--t-primary)", fontWeight: "700" }}>@{username}</span>
                        </p>

                        {/* Grade Badge */}
                        <div style={{
                            display: "inline-block",
                            marginTop: "1.5rem",
                            padding: "0.5rem 1.5rem",
                            borderRadius: "100px",
                            background: `${sc.color}18`,
                            border: `1px solid ${sc.color}40`,
                            color: sc.color,
                            fontWeight: "700",
                            fontSize: "0.9rem",
                            letterSpacing: "0.05em"
                        }}>
                            {sc.grade}
                        </div>

                        {/* Blind spots */}
                        {blind_spots.length > 0 && (
                            <div style={{ marginTop: "2.5rem" }}>
                                <div className="divider" />
                                <p style={{
                                    color: "var(--red)",
                                    fontSize: "0.875rem",
                                    fontWeight: "600",
                                    marginBottom: "1rem",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    gap: "0.5rem"
                                }}>
                                    ⚠️ Recruiter will immediately notice these issues
                                </p>
                                <div style={{ display: "flex", gap: "0.6rem", flexWrap: "wrap", justifyContent: "center" }}>
                                    {blind_spots.map(spot => (
                                        <span className="blind-spot-badge" key={spot}>{spot}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Section Header */}
                <div style={{ marginBottom: "1.5rem" }} className="fade-up-delay-1">
                    <h2 style={{
                        fontSize: "1.3rem",
                        fontWeight: "700",
                        letterSpacing: "-0.02em",
                        marginBottom: "0.3rem"
                    }}>
                        Deep Diagnostic Breakdown
                    </h2>
                    <p style={{ color: "var(--t-secondary)", fontSize: "0.9rem" }}>
                        Every dimension analyzed, with expert advice on what to fix first.
                    </p>
                </div>

                {/* Signal Cards Grid */}
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(310px, 1fr))",
                    gap: "1.5rem",
                    position: "relative"
                }} className="fade-up-delay-2">
                    {signalList.map(({ key, title }) => (
                        <SignalCard
                            key={key}
                            title={title}
                            score={signals[key].score}
                            reason={signals[key].reason}
                            improvement={signals[key].improvement}
                            isBlindSpot={blind_spots.includes(title)}
                        />
                    ))}
                </div>

                {/* CTA Footer */}
                <div style={{
                    textAlign: "center",
                    marginTop: "5rem",
                    padding: "3rem",
                    borderTop: "1px solid var(--border-subtle)"
                }}>
                    <p style={{ color: "var(--t-secondary)", marginBottom: "1.5rem", fontSize: "0.95rem" }}>
                        Know someone whose profile needs sorting?
                    </p>
                    <button className="btn-primary" onClick={() => navigate("/")}>
                        Audit Another Profile
                    </button>
                </div>
            </div>
        </div>
    )
}