import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/graph";

function GraphView({ graph, start, goal }) {
  const nodes = Object.keys(graph).sort();
  return (
    <div style={{ textAlign: "left", marginTop: 12 }}>
      <div style={{ fontSize: 13, opacity: 0.85, marginBottom: 8 }}>
        <strong>START:</strong> {start} &nbsp; | &nbsp; <strong>GOAL:</strong> {goal}
      </div>

      <div style={{
        background: "#f9fafb",
        border: "1px solid #e5e7eb",
        borderRadius: 10,
        padding: 12,
        fontFamily: "monospace",
        fontSize: 13,
        lineHeight: 1.6
      }}>
        {nodes.map((u) => (
          <div key={u}>
            <strong>{u}</strong>: {graph[u].join(", ")}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function GraphBFSQuestion() {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [solution, setSolution] = useState(null);
  const [hasTried, setHasTried] = useState(false);

  const generateQuestion = async () => {
    try {
      const res = await axios.get(`${API_URL}/generate`);
      setQuestion(res.data);
      setAnswer("");
      setResult(null);
      setSolution(null);
      setHasTried(false);
    } catch (e) {
      alert("Eroare la generare.");
      console.error(e);
    }
  };

  const getSolution = async () => {
    if (!question) return;
    try {
      const res = await axios.post(`${API_URL}/solve`, question);
      setSolution(res.data);
    } catch (e) {
      alert("Eroare la /solve.");
      console.error(e);
    }
  };

  const evaluate = async () => {
    if (!question) return;
    setHasTried(true);

    try {
      let sol = solution;
      if (!sol) {
        const res = await axios.post(`${API_URL}/solve`, question);
        sol = res.data;
        setSolution(sol);
      }

      const resEval = await axios.post(`${API_URL}/evaluate`, {
        student_answer: answer,
        correct_distance: sol.has_path ? sol.distance : null,
        has_path: sol.has_path,
      });

      setResult(resEval.data);
    } catch (e) {
      console.error(e);
      setResult({ score: 0, feedback: "Eroare la evaluare." });
    }
  };

  return (
    <div className="container">
      <h1>🕸️ SmarTest — Graph BFS</h1>
      <button onClick={generateQuestion}>Generează întrebare</button>

      {question && (
        <>
          <p style={{ fontWeight: "bold", marginTop: 16, whiteSpace: "pre-line" }}>
            {question.question}
          </p>

          <GraphView graph={question.graph} start={question.start} goal={question.goal} />

          <textarea
            placeholder="Răspunde cu un număr (distanță) sau 'Nu există drum'."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <div style={{ display: "flex", gap: 10, justifyContent: "flex-end", marginTop: 10 }}>
            <button onClick={evaluate}>Evaluează răspunsul</button>
            <button onClick={getSolution} disabled={!hasTried} title={hasTried ? "" : "Răspunde mai întâi"}>
              Afișează răspunsul corect
            </button>
          </div>
        </>
      )}

      {result && (
        <div className="result-box">
          <h3>Rezultatul evaluării</h3>
          <p>✅ <strong>Scor:</strong> {result.score}%</p>
          <p>💬 {result.feedback}</p>
        </div>
      )}

      {solution && hasTried && (
        <div className="result-box" style={{ marginTop: 12 }}>
          <h3>Răspuns corect</h3>
          {solution.has_path ? (
            <>
              <p><strong>Distanță minimă:</strong> {solution.distance}</p>
              <p style={{ fontSize: 13, opacity: 0.85 }}>
                <strong>Un drum minim:</strong> {solution.path.join(" → ")}
              </p>
            </>
          ) : (
            <p>Nu există drum valid.</p>
          )}
        </div>
      )}
    </div>
  );
}
