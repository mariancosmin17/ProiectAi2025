import React, { useState } from "react";
import axios from "axios";



const API_URL = "http://127.0.0.1:8000/api/v1/path";

function Cell({ v, isStart, isGoal }) {
  const bg =
    isStart ? "#22c55e" : isGoal ? "#ef4444" : v === 1 ? "#111827" : "#e5e7eb";
  const text = isStart ? "S" : isGoal ? "G" : v === 1 ? "■" : "";
  return (
    <div
      style={{
        width: 34,
        height: 34,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 6,
        background: bg,
        color: "white",
        fontWeight: "bold",
        userSelect: "none",
      }}
    >
      {text}
    </div>
  );
}

export default function PathQuestion() {
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
      // ne asigurăm că avem soluția (cost + has_path) pentru evaluare
      let sol = solution;
      if (!sol) {
        const res = await axios.post(`${API_URL}/solve`, question);
        sol = res.data;
        setSolution(sol);
      }

      const resEval = await axios.post(`${API_URL}/evaluate`, {
        student_answer: answer,
        correct_cost: sol.has_path ? sol.cost : null,
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
      <h1>🧭 SmarTest — A* Pathfinding</h1>
      <button onClick={generateQuestion}>Generează întrebare</button>

      {question && (
        <>
          <p style={{ fontWeight: "bold", marginTop: 16 }}>{question.question}</p>

          <div style={{ marginTop: 12, display: "inline-block" }}>
            <div
              style={{
                display: "grid",
                gap: 6,
                gridTemplateColumns: `repeat(${question.grid[0].length}, 34px)`,
              }}
            >
              {question.grid.map((row, r) =>
                row.map((v, c) => (
                  <Cell
                    key={`${r}-${c}`}
                    v={v}
                    isStart={r === question.start[0] && c === question.start[1]}
                    isGoal={r === question.goal[0] && c === question.goal[1]}
                  />
                ))
              )}
            </div>
            <p style={{ fontSize: 12, opacity: 0.8, marginTop: 8 }}>
              Verde = START, Roșu = GOAL, Negru = obstacol
            </p>
          </div>

          <textarea
            placeholder="Răspunde cu un număr (cost) sau 'Nu există drum'."
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
            <p><strong>Cost minim:</strong> {solution.cost}</p>
          ) : (
            <p>Nu există drum valid.</p>
          )}
        </div>
      )}
    </div>
  );
}
