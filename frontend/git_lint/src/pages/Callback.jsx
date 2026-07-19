import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Callback() {
    const navigate = useNavigate()
    const [debugMsg, setDebugMsg] = useState("Initializing callback...")

    useEffect(() => {
        const params = new URLSearchParams(window.location.search)
        const token = params.get("token")
        const error = params.get("error")

        if (error) {
            setDebugMsg(`GitHub OAuth Error: ${error}`)
            setTimeout(() => navigate("/"), 4000)
            return
        }

        if (token) {
            setDebugMsg(`Found token! Length: ${token.length}. Decoding...`)
            sessionStorage.setItem("devdeck_token", token)

            try {
                let base64Url = token.split(".")[1]
                let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/")
                while (base64.length % 4) {
                    base64 += "="
                }
                const payload = JSON.parse(atob(base64))
                sessionStorage.setItem("github_username", payload.github_username)

                setDebugMsg(`Success! Welcome ${payload.github_username}. Redirecting...`)
                setTimeout(() => {
                    navigate(`/audit/${payload.github_username}`)
                }, 1000)
            } catch (e) {
                setDebugMsg(`JWT Decode Failed: ${e.message}`)
                setTimeout(() => navigate("/"), 4000)
            }
        } else {
            setDebugMsg("No token found in URL! Were you redirected properly? Navigating home in 3s...")
            setTimeout(() => navigate("/"), 3000)
        }
    }, [navigate])

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            position: "relative",
            overflow: "hidden"
        }}>
            <div className="orb orb-1" />
            <div className="orb orb-2" />
            <div className="grid-overlay" />

            <div className="glass-panel" style={{
                padding: "3rem 4rem",
                textAlign: "center",
                zIndex: 10
            }}>
                <div style={{
                    width: "48px", height: "48px",
                    borderRadius: "12px",
                    background: "rgba(124,108,248,0.15)",
                    border: "1px solid rgba(124,108,248,0.3)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    margin: "0 auto 1.5rem"
                }}>
                    <svg width="24" height="24" viewBox="0 0 16 16" fill="#7c6cf8">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                        0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                        -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
                        .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
                        -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0
                        1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82
                        1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01
                        1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                </div>
                <p style={{ fontSize: "1.3rem", fontWeight: "700", marginBottom: "0.5rem" }}>
                    Authenticating...
                </p>
                <p style={{ color: "var(--brand-a)", fontSize: "0.9rem" }}>{debugMsg}</p>
            </div>
        </div>
    )
}