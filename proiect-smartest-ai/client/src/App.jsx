import React, { useState } from "react";
import NashGame from "./components/NashGame";
import CSPSolver from "./components/CSPSolver";
import AlphaBetaGame from "./components/AlphaBetaGame";
import "./styles.css";

function App() {
  const [activeComponent, setActiveComponent] = useState("nash");

  return (
    <div>
      <div style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        padding: "20px",
        textAlign: "center",
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
      }}>
        <h1 style={{ color: "white", margin: "0 0 20px 0", fontSize: 32 }}>
          🎓 SmarTest Platform
        </h1>
        <div style={{ display: "flex", gap: 15, justifyContent: "center", flexWrap: "wrap" }}>
          <button
            onClick={() => setActiveComponent("nash")}
            style={{
              padding: "12px 24px",
              fontSize: 16,
              fontWeight: "bold",
              background: activeComponent === "nash" ? "#ffffff" : "rgba(255,255,255,0.3)",
              color: activeComponent === "nash" ? "#667eea" : "white",
              border: "2px solid white",
              borderRadius: 8,
              cursor: "pointer",
              transition: "all 0.3s ease",
              boxShadow: activeComponent === "nash" ? "0 4px 6px rgba(0,0,0,0.2)" : "none"
            }}
          >
            🎯 Nash Equilibrium
          </button>
          <button
            onClick={() => setActiveComponent("csp")}
            style={{
              padding: "12px 24px",
              fontSize: 16,
              fontWeight: "bold",
              background: activeComponent === "csp" ? "#ffffff" : "rgba(255,255,255,0.3)",
              color: activeComponent === "csp" ? "#667eea" : "white",
              border: "2px solid white",
              borderRadius: 8,
              cursor: "pointer",
              transition: "all 0.3s ease",
              boxShadow: activeComponent === "csp" ? "0 4px 6px rgba(0,0,0,0.2)" : "none"
            }}
          >
            🧩 CSP Solver
          </button>
          <button
            onClick={() => setActiveComponent("alphabeta")}
             style={{
              padding: "12px 24px",
              fontSize: 16,
              fontWeight: "bold",
              background: activeComponent === "alphabeta" ? "#ffffff" : "rgba(255,255,255,0.3)",
              color: activeComponent === "alphabeta" ? "#667eea" : "white",
              border: "2px solid white",
              borderRadius: 8,
              cursor: "pointer",
              transition: "all 0.3s ease",
              boxShadow: activeComponent === "alphabeta" ? "0 4px 6px rgba(0,0,0,0.2)" : "none"
            }}
          >   
            🌳 Alpha-Beta
            </button>          
        </div>
      </div>

      <div style={{ minHeight: "calc(100vh - 140px)" }}>
        {activeComponent === "nash" && <NashGame />}
        {activeComponent === "csp" && <CSPSolver />}
        {activeComponent === "alphabeta" && <AlphaBetaGame />}
      </div>

      <footer style={{
        background: "#f3f4f6",
        padding: "15px",
        textAlign: "center",
        fontSize: 13,
        color: "#6b7280",
        borderTop: "1px solid #e5e7eb"
      }}>
        <p style={{ margin: 0 }}>
          © 2025 SmarTest Platform - Rezolvare probleme de teorie a jocurilor și CSP
        </p>
      </footer>
    </div>
  );
}

export default App;