import React, { useState } from "react";
import NashGame from "./components/NashGame";
import CSPSolver from "./components/CSPSolver";
import SearchStrategy from "./components/SearchStrategy";
import "./styles.css";

function App() {
  const [activeTab, setActiveTab] = useState("search"); // default: Search

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎓 SmarTest - AI Question Generator</h1>
        <p>Generare și evaluare întrebări pentru examenul de Inteligență Artificială</p>
      </header>

      <div className="tabs">
        <button
          className={activeTab === "search" ?  "tab active" : "tab"}
          onClick={() => setActiveTab("search")}
        >
          🔍 Search Strategies
        </button>
        <button
          className={activeTab === "nash" ? "tab active" : "tab"}
          onClick={() => setActiveTab("nash")}
        >
          🎮 Nash Equilibrium
        </button>
        <button
          className={activeTab === "csp" ? "tab active" : "tab"}
          onClick={() => setActiveTab("csp")}
        >
          🧩 CSP Solver
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "search" && <SearchStrategy />}
        {activeTab === "nash" && <NashGame />}
        {activeTab === "csp" && <CSPSolver />}
      </div>

      <footer className="app-footer">
        <p>Proiect realizat pentru cursul de Inteligență Artificială - 2025</p>
      </footer>
    </div>
  );
}

export default App;