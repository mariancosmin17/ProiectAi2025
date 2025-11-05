import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/nash";

export default function NashGame() {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [correctEquilibria, setCorrectEquilibria] = useState([]);

  // 1️⃣ Generează întrebare random
  const generateQuestion = async () => {
    try {
      const res = await axios.get(`${API_URL}/generate`);
      setQuestion(res.data);
      setResult(null);
      setAnswer("");
    } catch (err) {
      alert("Eroare la generarea întrebării.");
      console.error(err);
    }
  };

  // 2️⃣ Obține echilibrul corect
  const getCorrectAnswer = async () => {
    const res = await axios.post(`${API_URL}/solve`, {
      p1_payoffs: question.p1_payoffs,
      p2_payoffs: question.p2_payoffs,
      p1_strategies: question.p1_strategies,
      p2_strategies: question.p2_strategies,
    });
    const eq = res.data.equilibria.map((e) => e.name);
    setCorrectEquilibria(eq);
    return eq;
  };

  // 3️⃣ Evaluează răspunsul studentului
  const evaluateAnswer = async () => {
    const correct =
      correctEquilibria.length > 0 ? correctEquilibria : await getCorrectAnswer();

    const res = await axios.post(`${API_URL}/evaluate`, {
      student_answer: answer,
      correct_equilibria: correct,
    });
    setResult(res.data);
  };

  return (
    <div className="container">
      <h1>🎓 SmarTest — Nash Equilibrium</h1>

      <button onClick={generateQuestion}>Generează întrebare</button>

      {question && (
        <>
          <p style={{ fontWeight: "bold", marginTop: "20px" }}>
            {question.question}
          </p>

          <table>
            <thead>
              <tr>
                <th></th>
                {question.p2_strategies.map((s, j) => (
                  <th key={j}>{s}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {question.p1_strategies.map((s1, i) => (
                <tr key={i}>
                  <th>{s1}</th>
                  {question.p1_payoffs[i].map((p1, j) => (
                    <td key={j}>
                      ({p1}, {question.p2_payoffs[i][j]})
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <textarea
            placeholder="Scrie răspunsul tău aici, ex: (Sus, Stânga)"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <div style={{ textAlign: "right", marginTop: "10px" }}>
            <button onClick={evaluateAnswer}>Evaluează răspunsul</button>
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
    </div>
  );
}
