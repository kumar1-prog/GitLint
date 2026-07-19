import Logo from "../assets/logo.png"

export default function Landing() {
    const handleLogin = () => {
        const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
        window.location.href = `${apiUrl}/auth/login`
    }

    const handleSignup = () => {
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000"
        window.location.href = `${apiUrl}/auth/login?prompt=consent`
    }

    const features = [
        {
            icon: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
                </svg>
            ),
            title: "Recruiter Like Analysis",
            desc: "See exactly how hiring managers perceive your GitHub in the first 30 seconds.",
            color: "#7c6cf8"
        },
        {
            icon: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M18 20V10M12 20V4M6 20v-6" />
                </svg>
            ),
            title: "6 Signal Deep Analysis",
            desc: "From commit consistency to README quality — every dimension scored & explained.",
            color: "#56b7ff"
        },
        {
            icon: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" />
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
            ),
            title: "Global Peer Benchmark",
            desc: "Compare yourself against thousands of developers and see where you rank.",
            color: "#00e5a0"
        },
    ]

    return (
        <div style={{ position: "relative", minHeight: "100vh", zIndex: 1, overflow: "hidden" }}>
            {/* Ambient Background Orbs */}
            <div className="orb orb-1" />
            <div className="orb orb-2" />
            <div className="orb orb-3" />
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
                <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>

                    <button className="btn-ghost" onClick={handleLogin} style={{ fontSize: "0.85rem" }}>
                        Sign In
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <main style={{
                maxWidth: "1100px",
                margin: "0 auto",
                padding: "7rem 2rem 5rem",
                position: "relative",
                zIndex: 10
            }}>
                {/* Label Badge */}
                <div style={{ display: "flex", justifyContent: "center", marginBottom: "2rem" }} className="fade-up">
                    <span className="label-tag">
                        <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: "#7c6cf8", animation: "pulse-outline 2s infinite" }} />
                        Get Your GitHub Analysis
                    </span>
                </div>

                {/* Hero Title */}
                <div style={{ textAlign: "center", marginBottom: "1.5rem" }} className="fade-up-delay-1">
                    <h1 className="display-title">
                        Your GitHub,<br />through a recruiter's eyes.
                    </h1>
                </div>

                {/* Subtitle */}
                <p style={{
                    textAlign: "center",
                    fontSize: "1.2rem",
                    color: "var(--t-secondary)",
                    maxWidth: "600px",
                    margin: "0 auto 4rem",
                    lineHeight: "1.7",
                    fontWeight: "400"
                }} className="fade-up-delay-2">
                    GitLint analyzes your public repositories across 6 key signals and gives you an exact score — the same way technical recruiters evaluate candidates.
                </p>

                {/* Auth Box */}
                <div className="glass-panel fade-up-delay-3" style={{
                    padding: "3rem",
                    maxWidth: "480px",
                    margin: "0 auto 6rem",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: "0"
                }}>
                    <h2 style={{
                        fontSize: "1.3rem",
                        fontWeight: "700",
                        marginBottom: "0.5rem",
                        letterSpacing: "-0.02em"
                    }}>
                        Get your free profile score
                    </h2>
                    <p style={{ color: "var(--t-secondary)", fontSize: "0.9rem", marginBottom: "2rem" }}>
                        Connect once, never worry again.
                    </p>

                    {/* Signup Button */}
                    <button className="btn-primary" onClick={handleSignup} style={{ width: "100%", justifyContent: "center", fontSize: "1.05rem" }}>
                        <svg height="22" width="22" viewBox="0 0 16 16" fill="currentColor">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                            0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                            -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
                            .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
                            -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0
                            1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82
                            1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01
                            1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                        Continue with GitHub
                    </button>

                    <div className="divider" style={{ width: "100%" }} />

                    <p style={{ color: "var(--t-secondary)", fontSize: "0.9rem" }}>
                        Already a member?{" "}
                        <button
                            onClick={handleLogin}
                            style={{
                                background: "none",
                                border: "none",
                                color: "#7c6cf8",
                                fontWeight: "700",
                                cursor: "pointer",
                                fontSize: "0.9rem",
                                fontFamily: "inherit",
                                textDecoration: "none",
                                transition: "opacity 0.2s"
                            }}
                            onMouseOver={e => e.target.style.opacity = "0.7"}
                            onMouseOut={e => e.target.style.opacity = "1"}
                        >
                            Sign in instantly →
                        </button>
                    </p>

                    <p style={{
                        fontSize: "0.75rem",
                        color: "var(--t-tertiary)",
                        marginTop: "1.5rem",
                        lineHeight: "1.6"
                    }}>
                        Reads only your public repos, no code is stored
                    </p>
                </div>

                {/* Feature Cards */}
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: "1.5rem",
                    position: "relative",
                    zIndex: 10
                }}>
                    {features.map((f) => (
                        <div className="glass-card" key={f.title} style={{ padding: "2rem" }}>
                            <div style={{
                                width: "42px", height: "42px",
                                borderRadius: "12px",
                                background: `${f.color}18`,
                                border: `1px solid ${f.color}30`,
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                color: f.color,
                                marginBottom: "1.2rem"
                            }}>
                                {f.icon}
                            </div>
                            <h3 style={{
                                fontWeight: "700",
                                fontSize: "1rem",
                                marginBottom: "0.5rem",
                                letterSpacing: "-0.01em"
                            }}>
                                {f.title}
                            </h3>
                            <p style={{
                                color: "var(--t-secondary)",
                                fontSize: "0.9rem",
                                lineHeight: "1.6"
                            }}>
                                {f.desc}
                            </p>
                        </div>
                    ))}
                </div>
            </main>

            {/* Footer */}
            <footer style={{
                textAlign: "center",
                color: "var(--t-tertiary)",
                fontSize: "0.8rem",
                padding: "2rem",
                borderTop: "1px solid var(--border-subtle)",
                position: "relative",
                zIndex: 10
            }}>
                GitLint · Recruiters style analysis
            </footer>
        </div>
    )
}