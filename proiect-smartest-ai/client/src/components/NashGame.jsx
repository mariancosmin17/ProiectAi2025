import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/nash";

export default function NashGame() {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);

  // lista echilibrelor corecte (ex: ["(D, R)"])
  const [correctEquilibria, setCorrectEquilibria] = useState([]);
  // controlăm când dezvăluim soluția
  const [solutionShown, setSolutionShown] = useState(false);
  // a încercat să răspundă?
  const [hasTried, setHasTried] = useState(false);

  // 1) Generează întrebare random
  const generateQuestion = async () => {
    try {
      const res = await axios.get(`${API_URL}/generate`);
      setQuestion(res.data);
      setResult(null);
      setAnswer("");
      setCorrectEquilibria([]);
      setSolutionShown(false);
      setHasTried(false);
    } catch (err) {
      alert("Eroare la generarea întrebării.");
      console.error(err);
    }
  };

  // 2) Obține echilibrul corect de la backend
  const getCorrectAnswer = async () => {
    if (!question) return [];
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

  // 3) Evaluează răspunsul studentului
  const evaluateAnswer = async () => {
    setHasTried(true);
    const correct =
      correctEquilibria.length > 0 ? correctEquilibria : await getCorrectAnswer();

    const res = await axios.post(`${API_URL}/evaluate`, {
      student_answer: answer,
      correct_equilibria: correct,
    });
    setResult(res.data);
  };

  // 4) Afișează soluția (inclusiv când nu există NE pur)
  const handleShowSolution = async () => {
    if (!question) return;
    if (correctEquilibria.length === 0) {
      await getCorrectAnswer(); // poate întoarce []
    }
    setSolutionShown(true); // arată oricum secțiunea
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
            placeholder="Scrie răspunsul tău aici, ex: (Jos, Dreapta)"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <div
            style={{
              display: "flex",
              gap: 10,
              justifyContent: "flex-end",
              marginTop: 10,
            }}
          >
            <button onClick={evaluateAnswer}>Evaluează răspunsul</button>
            <button
              onClick={handleShowSolution}
              disabled={!hasTried} // dezvăluie doar după încercare
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

      {solutionShown && (
        <div className="result-box" style={{ marginTop: 12 }}>
          <h3>Răspuns corect</h3>
          <p>
            {correctEquilibria.length
              ? correctEquilibria.join(", ")
              : "Nu există echilibru Nash pur."}
          </p>
          <p style={{ fontSize: 13, opacity: 0.8 }}>
            (Echilibrul Nash în strategii pure există la intersecția răspunsurilor
            optime: pe fiecare coloană maximizăm payoff-ul Jucătorului 1, iar pe
            fiecare rând maximizăm payoff-ul Jucătorului 2.)
          </p>
        </div>
      )}
    </div>
  );
}
