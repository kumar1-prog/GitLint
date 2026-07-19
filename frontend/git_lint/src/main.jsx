import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Landing from "./pages/Landing"
import Audit from "./pages/Audit"
import Report from "./pages/Report"
import Callback from "./pages/Callback"
import "./index.css"

// BrowserRouter = enables URL-based navigation in React
// Without this, React has no idea what /report or /audit means
// Routes = container that holds all route definitions
// Route = maps a URL path to a component
// When user visits /report → React renders <Report /> component
// No page reload happens — React swaps components instantly (SPA behavior)

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/audit/:username" element={<Audit />} />
        <Route path="/report" element={<Report />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
)