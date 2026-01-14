import React, { useState } from "react";
import NashGame from "./components/NashGame";
import CSPSolver from "./components/CSPSolver";
import SearchStrategy from "./components/SearchStrategy";
import AlphaBetaGame from "./components/AlphaBetaGame";
import PathQuestion from "./components/PathQuestion";
import GraphBFSQuestion from "./components/GraphBFSQuestion";
import "./styles.css";

function App() {
  const [activeTab, setActiveTab] = useState("search");

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="header-text">
            <h1>SmarTest Platform</h1>
            <p>AI Question Generator & Solver</p>
          </div>
        </div>
      </header>

      <nav className="tabs-container">
        <div className="tabs">
          <button
            className={activeTab === "search" ? "tab active" : "tab"}
            onClick={() => setActiveTab("search")}
          >
            <span className="tab-icon">🔍</span>
            <span className="tab-text">Search Strategies</span>
          </button>
          <button
            className={activeTab === "nash" ? "tab active" : "tab"}
            onClick={() => setActiveTab("nash")}
          >
            <span className="tab-icon">🎮</span>
            <span className="tab-text">Nash Equilibrium</span>
          </button>
          <button
            className={activeTab === "csp" ? "tab active" : "tab"}
            onClick={() => setActiveTab("csp")}
          >
            <span className="tab-icon">🧩</span>
            <span className="tab-text">CSP Solver</span>
          </button>
          <button
            className={activeTab === "alphabeta" ? "tab active" : "tab"}
            onClick={() => setActiveTab("alphabeta")}
          >
            <span className="tab-icon">🌳</span>
            <span className="tab-text">Alpha-Beta</span>
          </button>
          <button
            className={activeTab === "path" ? "tab active" : "tab"}
            onClick={() => setActiveTab("path")}
          >
            <span className="tab-icon">🧭</span>
            <span className="tab-text">A* Pathfinding</span>
          </button>
          <button
            className={activeTab === "graph" ? "tab active" : "tab"}
            onClick={() => setActiveTab("graph")}
          >
            <span className="tab-icon">🕸️</span>
            <span className="tab-text">Graph BFS</span>
          </button>
        </div>
      </nav>

      <main className="tab-content">
        <div className="content-wrapper">
          {activeTab === "search" && <SearchStrategy />}
          {activeTab === "nash" && <NashGame />}
          {activeTab === "csp" && <CSPSolver />}
          {activeTab === "alphabeta" && <AlphaBetaGame />}
          {activeTab === "path" && <PathQuestion />}
          {activeTab === "graph" && <GraphBFSQuestion />}
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <p>© 2025 SmarTest Platform</p>
          <p className="footer-subtitle">Proiect realizat pentru cursul de Inteligență Artificială</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
