import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/csp";

export default function CSPSolver() {
  const [variables, setVariables] = useState("");
  const [domains, setDomains] = useState("");
  const [constraints, setConstraints] = useState("");
  const [solution, setSolution] = useState(null);
  const [solutionMRV, setSolutionMRV] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("backtracking");
  
  // State pentru generare random
  const [generateConfig, setGenerateConfig] = useState({
    problem_type: "random",
    num_variables: 6,
    domain_size_min: 1,
    domain_size_max: 3,
    num_constraints: 5,
    num_colors: 3,
    edge_probability: 0.4,
    num_time_slots: 4
  });
  const [showGenerateModal, setShowGenerateModal] = useState(false);

  // Exemplu predefinit pentru utilizatori
  const loadExample = () => {
    setVariables("V1, V2, V3, V4, V5, V6");
    setDomains(JSON.stringify({
      "V1": ["a", "b", "c"],
      "V2": ["a"],
      "V3": ["a", "b", "c"],
      "V4": ["a", "b"],
      "V5": ["a", "b", "c"],
      "V6": ["a", "b"]
    }, null, 2));
    setConstraints(JSON.stringify([
      ["V1", "V2"],
      ["V2", "V3"],
      ["V3", "V4"],
      ["V4", "V5"],
      ["V5", "V6"]
    ], null, 2));
  };

  // Generează problemă random
  const generateRandomProblem = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/generate`, generateConfig);
      
      // Setăm datele generate în formular
      setVariables(res.data.variables. join(", "));
      setDomains(JSON.stringify(res.data.domains, null, 2));
      setConstraints(JSON.stringify(res.data.constraints, null, 2));
      
      setSolution(null);
      setSolutionMRV(null);
      setShowGenerateModal(false);
      
      alert("✅ Problemă generată cu succes!  Poți acum să o rezolvi.");
    } catch (err) {
      alert("Eroare la generarea problemei:  " + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Parsează și validează input-ul utilizatorului
  const parseInput = () => {
    try {
      const varsArray = variables.split(",").map(v => v.trim()).filter(Boolean);
      const domainsObj = JSON.parse(domains);
      const constraintsArray = JSON.parse(constraints);

      return {
        variables: varsArray,
        domains: domainsObj,
        constraints: constraintsArray
      };
    } catch (err) {
      throw new Error("Format invalid.  Verifică sintaxa JSON pentru domenii și constrângeri.");
    }
  };

  // Helper function pentru a obține numărul de pași
  const getStepsCount = (stepsData) => {
    if (typeof stepsData === 'number') {
      return stepsData;
    }
    if (Array.isArray(stepsData)) {
      return stepsData.length;
    }
    return 0;
  };

  // Rezolvă cu Backtracking normal
  const solveBacktracking = async () => {
    setLoading(true);
    setSolution(null);
    try {
      const problem = parseInput();
      console.log("Sending to /solve:", problem);
      const res = await axios.post(`${API_URL}/solve`, problem);
      console.log("Response from /solve:", res.data);
      setSolution(res.data);
      setActiveTab("backtracking");
    } catch (err) {
      alert(err.response?.data?.detail || err.message || "Eroare la rezolvarea problemei.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Rezolvă cu Backtracking MRV
  const solveBacktrackingMRV = async () => {
    setLoading(true);
    setSolutionMRV(null);
    try {
      const problem = parseInput();
      console.log("Sending to /solve-mrv:", problem);
      const res = await axios.post(`${API_URL}/solve-mrv`, problem);
      console.log("Response from /solve-mrv:", res. data);
      setSolutionMRV(res.data);
      setActiveTab("mrv");
    } catch (err) {
      alert(err.response?.data?.detail || err. message || "Eroare la rezolvarea problemei (MRV).");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Rezolvă cu ambele metode
  const solveBoth = async () => {
    setLoading(true);
    setSolution(null);
    setSolutionMRV(null);
    try {
      const problem = parseInput();
      console.log("Sending to both endpoints:", problem);
      const [resNormal, resMRV] = await Promise. all([
        axios.post(`${API_URL}/solve`, problem),
        axios.post(`${API_URL}/solve-mrv`, problem)
      ]);
      console.log("Response from /solve:", resNormal.data);
      console.log("Response from /solve-mrv:", resMRV.data);
      setSolution(resNormal.data);
      setSolutionMRV(resMRV.data);
    } catch (err) {
      alert(err.response?.data?. detail || err.message || "Eroare la rezolvarea problemei.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setVariables("");
    setDomains("");
    setConstraints("");
    setSolution(null);
    setSolutionMRV(null);
  };

  return (
    <div className="container">
      <h1>🧩 SmarTest — CSP Solver</h1>
      <p style={{ fontSize: 14, opacity: 0.8 }}>
        Rezolvă probleme de satisfacție a constrângerilor (CSP) folosind Backtracking și MRV
      </p>

      <div style={{ marginBottom: 20 }}>
        <button onClick={loadExample} style={{ marginRight: 10 }}>
          📋 Încarcă exemplu
        </button>
        <button 
          onClick={() => setShowGenerateModal(true)} 
          style={{ marginRight: 10, background: "#059669", color: "white" }}
        >
          🎲 Generează problemă random
        </button>
        <button onClick={clearAll} style={{ background: "#666", color: "white" }}>
          🗑️ Șterge tot
        </button>
      </div>

      {/* Modal pentru configurarea generării */}
      {showGenerateModal && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0,0,0,0.5)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1000
        }}>
          <div style={{
            background: "white",
            padding: 30,
            borderRadius: 12,
            maxWidth: 600,
            width: "90%",
            maxHeight: "80vh",
            overflowY: "auto",
            boxShadow: "0 10px 40px rgba(0,0,0,0.3)"
          }}>
            <h2>🎲 Generează Problemă CSP</h2>
            
            <div style={{ marginBottom:  15 }}>
              <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                Tip problemă:
              </label>
              <select
                value={generateConfig.problem_type}
                onChange={(e) => setGenerateConfig({...generateConfig, problem_type: e.target.value})}
                style={{
                  width: "100%",
                  padding: 10,
                  fontSize: 14,
                  border: "1px solid #ccc",
                  borderRadius:  4
                }}
              >
                <option value="random">🎯 Random CSP</option>
                <option value="graph_coloring">🎨 Graph Coloring</option>
                <option value="scheduling">📅 Scheduling Problem</option>
              </select>
            </div>

            <div style={{ marginBottom: 15 }}>
              <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                Număr variabile:  {generateConfig.num_variables}
              </label>
              <input
                type="range"
                min="2"
                max="15"
                value={generateConfig. num_variables}
                onChange={(e) => setGenerateConfig({...generateConfig, num_variables: parseInt(e.target.value)})}
                style={{ width: "100%" }}
              />
            </div>

            {generateConfig.problem_type === "random" && (
              <>
                <div style={{ marginBottom: 15 }}>
                  <label style={{ fontWeight:  "bold", display: "block", marginBottom: 5 }}>
                    Mărime domeniu MIN:  {generateConfig.domain_size_min}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={generateConfig.domain_size_min}
                    onChange={(e) => setGenerateConfig({...generateConfig, domain_size_min: parseInt(e.target.value)})}
                    style={{ width: "100%" }}
                  />
                </div>

                <div style={{ marginBottom:  15 }}>
                  <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                    Mărime domeniu MAX: {generateConfig.domain_size_max}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={generateConfig.domain_size_max}
                    onChange={(e) => setGenerateConfig({...generateConfig, domain_size_max: parseInt(e. target.value)})}
                    style={{ width: "100%" }}
                  />
                </div>

                <div style={{ marginBottom: 15 }}>
                  <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                    Număr constrângeri: {generateConfig. num_constraints}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="30"
                    value={generateConfig.num_constraints}
                    onChange={(e) => setGenerateConfig({...generateConfig, num_constraints: parseInt(e.target. value)})}
                    style={{ width: "100%" }}
                  />
                </div>
              </>
            )}

            {generateConfig.problem_type === "graph_coloring" && (
              <>
                <div style={{ marginBottom: 15 }}>
                  <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                    Număr culori: {generateConfig.num_colors}
                  </label>
                  <input
                    type="range"
                    min="2"
                    max="8"
                    value={generateConfig.num_colors}
                    onChange={(e) => setGenerateConfig({...generateConfig, num_colors: parseInt(e.target. value)})}
                    style={{ width: "100%" }}
                  />
                </div>

                <div style={{ marginBottom:  15 }}>
                  <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                    Probabilitate muchii: {(generateConfig.edge_probability * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="90"
                    value={generateConfig. edge_probability * 100}
                    onChange={(e) => setGenerateConfig({...generateConfig, edge_probability: parseInt(e.target.value) / 100})}
                    style={{ width: "100%" }}
                  />
                </div>
              </>
            )}

            {generateConfig.problem_type === "scheduling" && (
              <div style={{ marginBottom: 15 }}>
                <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
                  Număr time slots: {generateConfig.num_time_slots}
                </label>
                <input
                  type="range"
                  min="2"
                  max="10"
                  value={generateConfig.num_time_slots}
                  onChange={(e) => setGenerateConfig({...generateConfig, num_time_slots: parseInt(e.target.value)})}
                  style={{ width: "100%" }}
                />
              </div>
            )}

            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button
                onClick={generateRandomProblem}
                disabled={loading}
                style={{ flex: 1, background: "#059669", color: "white", padding: "12px", fontSize: 16, fontWeight: "bold", borderRadius: 6, border: "none", cursor: loading ? "not-allowed" : "pointer" }}
              >
                {loading ?  "⏳ Se generează..." : "✨ Generează"}
              </button>
              <button
                onClick={() => setShowGenerateModal(false)}
                disabled={loading}
                style={{ flex: 1, background: "#666", color: "white", padding:  "12px", fontSize: 16, fontWeight: "bold", borderRadius: 6, border: "none", cursor: "pointer" }}
              >
                ❌ Anulează
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input pentru Variabile */}
      <div style={{ marginBottom: 15 }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
          Variabile (separate prin virgulă):
        </label>
        <input
          type="text"
          placeholder="ex: V1, V2, V3"
          value={variables}
          onChange={(e) => setVariables(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            fontSize: 14,
            border: "1px solid #ccc",
            borderRadius: 4
          }}
        />
      </div>

      {/* Input pentru Domenii */}
      <div style={{ marginBottom: 15 }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
          Domenii (JSON - variabilă:  listă de valori):
        </label>
        <textarea
          placeholder='ex: {"V1": ["a", "b", "c"], "V2": ["a"], "V3": ["a", "b"]}'
          value={domains}
          onChange={(e) => setDomains(e.target.value)}
          rows={6}
          style={{
            width: "100%",
            padding: 10,
            fontSize:  13,
            fontFamily: "monospace",
            border: "1px solid #ccc",
            borderRadius: 4
          }}
        />
      </div>

      {/* Input pentru Constrângeri */}
      <div style={{ marginBottom:  15 }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: 5 }}>
          Constrângeri (JSON - liste de perechi):
        </label>
        <textarea
          placeholder='ex: [["V1", "V2"], ["V2", "V3"], ["V3", "V4"]]'
          value={constraints}
          onChange={(e) => setConstraints(e.target.value)}
          rows={6}
          style={{
            width: "100%",
            padding: 10,
            fontSize:  13,
            fontFamily:  "monospace",
            border:  "1px solid #ccc",
            borderRadius: 4
          }}
        />
        <p style={{ fontSize: 12, opacity: 0.7, marginTop: 5 }}>
          ℹ️ Fiecare constrângere este o pereche [var1, var2] care înseamnă var1 ≠ var2
        </p>
      </div>

      {/* Butoane de rezolvare */}
      <div style={{ display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
        <button
          onClick={solveBacktracking}
          disabled={loading}
          style={{ flex: 1, minWidth: 150, padding: "12px", fontSize: 15, fontWeight: "bold" }}
        >
          {loading ? "⏳ Se rezolvă..." : "🔄 Rezolvă (Backtracking)"}
        </button>
        <button
          onClick={solveBacktrackingMRV}
          disabled={loading}
          style={{ flex: 1, minWidth: 150, padding: "12px", fontSize: 15, fontWeight:  "bold", background: "#2563eb", color: "white" }}
        >
          {loading ? "⏳ Se rezolvă..." : "🎯 Rezolvă (MRV)"}
        </button>
        <button
          onClick={solveBoth}
          disabled={loading}
          style={{ flex: 1, minWidth:  150, padding: "12px", fontSize: 15, fontWeight: "bold", background: "#16a34a", color: "white" }}
        >
          {loading ? "⏳ Se rezolvă..." : "⚡ Compară ambele"}
        </button>
      </div>

      {/* Afișarea rezultatelor */}
      {(solution || solutionMRV) && (
        <div style={{ marginTop: 30 }}>
          <div style={{ borderBottom: "2px solid #ddd", marginBottom: 20 }}>
            {solution && (
              <button
                onClick={() => setActiveTab("backtracking")}
                style={{
                  padding: "10px 20px",
                  marginRight: 10,
                  background: activeTab === "backtracking" ?  "#4f46e5" : "#ddd",
                  color: activeTab === "backtracking" ?  "white" : "black",
                  border: "none",
                  borderRadius: "4px 4px 0 0",
                  cursor: "pointer",
                  fontWeight: "bold"
                }}
              >
                Backtracking Standard
              </button>
            )}
            {solutionMRV && (
              <button
                onClick={() => setActiveTab("mrv")}
                style={{
                  padding: "10px 20px",
                  background: activeTab === "mrv" ? "#4f46e5" : "#ddd",
                  color: activeTab === "mrv" ? "white" : "black",
                  border: "none",
                  borderRadius: "4px 4px 0 0",
                  cursor: "pointer",
                  fontWeight:  "bold"
                }}
              >
                Backtracking MRV
              </button>
            )}
          </div>

          {/* Rezultat Backtracking Standard */}
          {activeTab === "backtracking" && solution && (
            <div className="result-box">
              <h3>📊 Rezultat - Backtracking Standard</h3>
              <p style={{ fontSize: 16, marginBottom: 10 }}>
                <strong>Status:</strong> {solution.message}
              </p>

              {solution.solution && Object.keys(solution.solution).length > 0 ? (
                <>
                  <h4>Soluție găsită:</h4>
                  <div style={{
                    background: "#f0fdf4",
                    padding:  15,
                    borderRadius:  8,
                    fontFamily: "monospace",
                    fontSize: 14
                  }}>
                    {Object.entries(solution.solution).map(([variable, value]) => (
                      <div key={variable} style={{ marginBottom:  5 }}>
                        <strong>{variable}</strong> = {value}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p style={{ color: "#dc2626", fontWeight: "bold" }}>
                  ❌ Nu există o soluție validă pentru această problemă CSP. 
                </p>
              )}

              <div style={{ marginTop: 20 }}>
                <h4>Număr de pași executați:  <span style={{ color: "#4f46e5", fontSize: 24 }}>{getStepsCount(solution. steps)}</span></h4>
              </div>

              {Array.isArray(solution.steps) && solution.steps.length > 0 && (
                <>
                  <h4 style={{ marginTop: 20 }}>Detalii pași de execuție:</h4>
                  <div style={{
                    maxHeight: 300,
                    overflowY: "auto",
                    background: "#f9fafb",
                    padding: 10,
                    borderRadius: 8,
                    fontSize: 13
                  }}>
                    {solution.steps.map((step, idx) => (
                      <div key={idx} style={{
                        padding: "8px 0",
                        borderBottom: idx < solution.steps.length - 1 ? "1px solid #e5e7eb" : "none"
                      }}>
                        <strong>Pasul {idx + 1}: </strong> {step}
                      </div>
                    ))}
                  </div>
                </>
              )}

              {/* Debug info */}
              <details style={{ marginTop: 10, fontSize: 12, opacity: 0.7 }}>
                <summary style={{ cursor: "pointer" }}>🐛 Debug Info</summary>
                <pre style={{ background: "#f3f4f6", padding: 10, borderRadius: 4, overflow: "auto" }}>
                  {JSON.stringify(solution, null, 2)}
                </pre>
              </details>
            </div>
          )}

          {/* Rezultat Backtracking MRV */}
          {activeTab === "mrv" && solutionMRV && (
            <div className="result-box">
              <h3>🎯 Rezultat - Backtracking MRV</h3>
              <p style={{ fontSize: 16, marginBottom:  10 }}>
                <strong>Status:</strong> {solutionMRV.message}
              </p>

              {solutionMRV.solution && Object.keys(solutionMRV.solution).length > 0 ? (
                <>
                  <h4>Soluție găsită:</h4>
                  <div style={{
                    background: "#eff6ff",
                    padding: 15,
                    borderRadius: 8,
                    fontFamily: "monospace",
                    fontSize: 14
                  }}>
                    {Object.entries(solutionMRV.solution).map(([variable, value]) => (
                      <div key={variable} style={{ marginBottom: 5 }}>
                        <strong>{variable}</strong> = {value}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p style={{ color:  "#dc2626", fontWeight:  "bold" }}>
                  ❌ Nu există o soluție validă pentru această problemă CSP.
                </p>
              )}

              <div style={{ marginTop: 20 }}>
                <h4>Număr de pași executați:  <span style={{ color: "#2563eb", fontSize: 24 }}>{getStepsCount(solutionMRV.steps)}</span></h4>
              </div>

              {Array. isArray(solutionMRV.steps) && solutionMRV.steps.length > 0 && (
                <>
                  <h4 style={{ marginTop: 20 }}>Detalii pași de execuție:</h4>
                  <div style={{
                    maxHeight: 300,
                    overflowY: "auto",
                    background: "#f9fafb",
                    padding: 10,
                    borderRadius: 8,
                    fontSize: 13
                  }}>
                    {solutionMRV.steps. map((step, idx) => (
                      <div key={idx} style={{
                        padding:  "8px 0",
                        borderBottom: idx < solutionMRV.steps.length - 1 ? "1px solid #e5e7eb" : "none"
                      }}>
                        <strong>Pasul {idx + 1}:</strong> {step}
                      </div>
                    ))}
                  </div>
                </>
              )}

              {/* Debug info */}
              <details style={{ marginTop: 10, fontSize: 12, opacity: 0.7 }}>
                <summary style={{ cursor:  "pointer" }}>🐛 Debug Info</summary>
                <pre style={{ background: "#f3f4f6", padding:  10, borderRadius: 4, overflow: "auto" }}>
                  {JSON.stringify(solutionMRV, null, 2)}
                </pre>
              </details>
            </div>
          )}

          {/* Comparație când ambele sunt rezolvate */}
          {solution && solutionMRV && (
            <div className="result-box" style={{ marginTop: 20, background: "#fef3c7" }}>
              <h3>⚡ Comparație performanță</h3>
              <div style={{ display: "flex", gap: 20, justifyContent: "space-around", flexWrap: "wrap" }}>
                <div style={{ textAlign: "center" }}>
                  <p><strong>Backtracking Standard:</strong></p>
                  <p style={{ fontSize: 32, fontWeight: "bold", color: "#4f46e5" }}>
                    {getStepsCount(solution.steps)}
                  </p>
                  <p style={{ fontSize: 14, opacity: 0.7 }}>pași</p>
                </div>
                <div style={{ textAlign: "center" }}>
                  <p><strong>Backtracking MRV:</strong></p>
                  <p style={{ fontSize: 32, fontWeight: "bold", color: "#2563eb" }}>
                    {getStepsCount(solutionMRV.steps)}
                  </p>
                  <p style={{ fontSize: 14, opacity: 0.7 }}>pași</p>
                </div>
              </div>
              <p style={{ fontSize: 14, opacity: 0.9, marginTop: 15, textAlign: "center", fontWeight: "bold" }}>
                {(() => {
                  const normalSteps = getStepsCount(solution.steps);
                  const mrvSteps = getStepsCount(solutionMRV. steps);
                  
                  if (normalSteps > mrvSteps) {
                    const improvement = ((normalSteps - mrvSteps) / normalSteps * 100).toFixed(1);
                    return `🎯 MRV este mai eficient cu ${improvement}% mai puțini pași! `;
                  } else if (normalSteps < mrvSteps) {
                    const improvement = ((mrvSteps - normalSteps) / mrvSteps * 100).toFixed(1);
                    return `📊 Backtracking standard este mai eficient cu ${improvement}% mai puțini pași!`;
                  } else {
                    return "⚖️ Ambele metode au aceeași eficiență pentru această problemă!";
                  }
                })()}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Info despre CSP */}
      <div style={{
        marginTop: 40,
        padding: 20,
        background: "#f3f4f6",
        borderRadius: 8,
        fontSize: 13
      }}>
        <h4>ℹ️ Despre CSP Solver</h4>
        <p>
          <strong>Backtracking Standard:</strong> Explorează variabilele în ordinea dată, 
          încercând fiecare valoare din domeniu până găsește o soluție validă.
        </p>
        <p style={{ marginTop: 10 }}>
          <strong>Backtracking MRV (Minimum Remaining Values):</strong> Euristica care 
          selectează întâi variabila cu cele mai puține valori rămase în domeniu, 
          reducând spațiul de căutare și îmbunătățind performanța.
        </p>
      </div>
    </div>
  );
}