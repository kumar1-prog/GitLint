import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"

export default function Audit() {
    const { username } = useParams()
    // useParams() extracts URL parameters
    // If URL is /audit/kumar1-prog → username = "kumar1-prog"
    // Without useParams we'd have to manually parse window.location

    const navigate = useNavigate()
    const [step, setStep] = useState(0)

    // Loading messages shown one by one while API call happens
    // Makes the wait feel intentional, not broken
    const steps = [
        "Fetching your repositories...",
        "Analyzing commit patterns...",
        "Evaluating README quality...",
        "Calculating peer benchmark...",
        "Generating your report...",
    ]

    useEffect(() => {
        // Cycle through loading messages every 1.2 seconds
        const interval = setInterval(() => {
            setStep(prev => {
                if (prev < steps.length - 1) return prev + 1
                return prev  // stay on last message, don't loop
            })
        }, 1200)

        // Fetch the actual audit report from backend
        const fetchReport = async () => {
            try {
                const token = sessionStorage.getItem("devdeck_token")
                // Retrieve JWT we stored in Callback.jsx

                const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000"
                const response = await axios.get(
                    `${apiUrl}/profile/${username}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                            // Send JWT in Authorization header
                            // Backend will verify this token before responding
                            // If token missing/expired → backend returns 401
                        }
                    }
                )

                // Store report in sessionStorage so Report page can access it
                // We can't pass it via URL (too large)
                // We can't use React state (page navigation wipes it)
                // sessionStorage persists across page navigation within same tab
                sessionStorage.setItem(
                    "devdeck_report",
                    JSON.stringify(response.data)
                )

                // Small delay so user sees the final loading message
                setTimeout(() => navigate("/report"), 800)

            } catch (error) {
                console.error("Audit failed:", error)
                alert("Failed to fetch audit report from backend. " + error.message)
                navigate("/")  // Send back to landing if something breaks
            }
        }

        fetchReport()

        // Cleanup: stop the interval when component unmounts
        // Without this → interval keeps running even after navigation
        // → memory leak → app slows down over time
        return () => clearInterval(interval)
    }, [username])

    return (
        <div style={{
            minHeight: "100vh",
            background: "#0d1117",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontFamily: "'Segoe UI', sans-serif"
        }}>
            {/* Spinner */}
            <div style={{
                width: "48px",
                height: "48px",
                border: "3px solid #30363d",
                borderTop: "3px solid #58a6ff",
                borderRadius: "50%",
                animation: "spin 1s linear infinite",
                marginBottom: "2rem"
            }} />

            <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>

            <p style={{
                fontSize: "1rem",
                color: "#8b949e",
                marginBottom: "0.5rem"
            }}>
                Auditing <strong style={{ color: "#58a6ff" }}>@{username}</strong>
            </p>

            {/* Current loading step */}
            <p style={{
                fontSize: "0.95rem",
                color: "#c9d1d9",
                transition: "opacity 0.3s"
            }}>
                {steps[step]}
            </p>

            {/* Progress dots */}
            <div style={{
                display: "flex",
                gap: "8px",
                marginTop: "2rem"
            }}>
                {steps.map((_, i) => (
                    <div key={i} style={{
                        width: "8px",
                        height: "8px",
                        borderRadius: "50%",
                        background: i <= step ? "#58a6ff" : "#30363d",
                        transition: "background 0.3s"
                    }} />
                ))}
            </div>
        </div>
    )
}