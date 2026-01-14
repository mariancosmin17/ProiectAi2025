import React, { useState } from "react";
import axios from "axios";
import TreeView from "./TreeView";


const API_URL = "http://127.0.0.1:8000/api/v1/alphabeta";

// Render simplu: tree ca JSON (clar pentru laborator)
function PrettyJSON({ data }) {
  return (
    <pre
      style={{
        textAlign: "left",
        background: "#f3f4f6",
        padding: 12,
        borderRadius: 8,
        maxHeight: 300,
        overflow: "auto",
        fontSize: 12,
      }}
    >
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}

export default function AlphaBetaGame() {
  const [question, setQuestion] = useState(null);

  // răspuns varianta A
  const [rootValue, setRootValue] = useState("");
  const [visitedLeaves, setVisitedLeaves] = useState("");

  const [solution, setSolution] = useState(null); // {root_value, visited_leaves, trace}
  const [result, setResult] = useState(null);     // {score, feedback}
  const [hasTried, setHasTried] = useState(false);
  const [solutionShown, setSolutionShown] = useState(false);

  const generateQuestion = async () => {
    try {
      const res = await axios.post(`${API_URL}/generate`, {
        depth: 3,
        branching: 2,
        value_min: 0,
        value_max: 15,
      });

      setQuestion(res.data);
      setRootValue("");
      setVisitedLeaves("");
      setSolution(null);
      setResult(null);
      setHasTried(false);
      setSolutionShown(false);
    } catch (err) {
      console.error(err);
      alert("Eroare la generarea întrebării Alpha-Beta.");
    }
  };

  const getSolution = async () => {
    if (!question) return null;
    const res = await axios.post(`${API_URL}/solve`, { root: question.root });
    setSolution(res.data);
    return res.data;
  };

  const evaluateAnswer = async () => {
    if (!question) return;
    setHasTried(true);

    try {
      // calculează soluția corectă pentru arborele curent
      const sol = await getSolution();
      if (!sol) return;

      const student_root_value =
        rootValue.trim() === "" ? null : parseInt(rootValue, 10);
      const student_visited_leaves =
        visitedLeaves.trim() === "" ? null : parseInt(visitedLeaves, 10);

      const res = await axios.post(`${API_URL}/evaluate`, {
        student_root_value,
        student_visited_leaves,
        correct_root_value: sol.root_value,
        correct_visited_leaves: sol.visited_leaves,
      });

      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({
        score: 0,
        feedback: "A apărut o eroare la evaluare. Încearcă din nou.",
      });
    }
  };

  const handleShowSolution = async () => {
    if (!question) return;
    if (!solution) await getSolution();
    setSolutionShown(true);
  };

  return (
    <div className="container">
      <h1>🌳 SmarTest — MinMax + Alpha-Beta</h1>

      <button onClick={generateQuestion}>Generează întrebare</button>

      {question && (
        <>
          <p style={{ fontWeight: "bold", marginTop: 20 }}>{question.question}</p>

            <div style={{ marginTop: 12 }}>
                <h3 style={{ marginBottom: 8 }}>Arbore (vizual)</h3>

                {/* arbore frumos, expand/collapse */}
                    <TreeView tree={question.root} />

                {/* JSON doar pentru debug, opțional */}
                <details style={{ marginTop: 10, textAlign: "left" }}>
                    <summary style={{ cursor: "pointer" }}>Vezi JSON (debug)</summary>
                    <PrettyJSON data={question.root} />
                </details>

                <p style={{ fontSize: 12, opacity: 0.75, marginTop: 6 }}>
                    (Nod intern: type=MAX/MIN, frunză: value)
                 </p>
            </div>


          <div style={{ display: "flex", gap: 10, marginTop: 15, flexWrap: "wrap" }}>
            <div style={{ flex: 1, minWidth: 180, textAlign: "left" }}>
              <label style={{ fontWeight: "bold" }}>Valoarea din rădăcină:</label>
              <input
                type="number"
                value={rootValue}
                onChange={(e) => setRootValue(e.target.value)}
                placeholder="ex: 5"
                style={{
                  width: "100%",
                  padding: 10,
                  fontSize: 14,
                  border: "1px solid #ccc",
                  borderRadius: 8,
                  marginTop: 6,
                }}
              />
            </div>

            <div style={{ flex: 1, minWidth: 180, textAlign: "left" }}>
              <label style={{ fontWeight: "bold" }}>Frunze vizitate:</label>
              <input
                type="number"
                value={visitedLeaves}
                onChange={(e) => setVisitedLeaves(e.target.value)}
                placeholder="ex: 6"
                style={{
                  width: "100%",
                  padding: 10,
                  fontSize: 14,
                  border: "1px solid #ccc",
                  borderRadius: 8,
                  marginTop: 6,
                }}
              />
            </div>
          </div>

          <div style={{ display: "flex", gap: 10, justifyContent: "flex-end", marginTop: 12 }}>
            <button onClick={evaluateAnswer}>Evaluează răspunsul</button>
            <button
              onClick={handleShowSolution}
              disabled={!hasTried}
              title={hasTried ? "" : "Răspunde mai întâi, apoi poți vedea soluția"}
            >
              Afișează răspunsul corect
            </button>
          </div>
        </>
      )}

      {result && (
        <div className="result-box">
          <h3>Rezultatul evaluării</h3>
          <p>
            ✅ <strong>Scor:</strong> {result.score}%
          </p>
          <p>💬 {result.feedback}</p>
        </div>
      )}

      {solutionShown && solution && (
        <div className="result-box" style={{ marginTop: 12 }}>
          <h3>Răspuns corect</h3>
          <p>
            <strong>Valoare rădăcină:</strong> {solution.root_value}
          </p>
          <p>
            <strong>Frunze vizitate:</strong> {solution.visited_leaves}
          </p>

          <details style={{ marginTop: 10, textAlign: "left" }}>
            <summary style={{ cursor: "pointer" }}>Vezi trace (pași Alpha-Beta)</summary>
            <pre
              style={{
                background: "#f3f4f6",
                padding: 12,
                borderRadius: 8,
                maxHeight: 260,
                overflow: "auto",
                fontSize: 12,
              }}
            >
              {solution.trace.join("\n")}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}
