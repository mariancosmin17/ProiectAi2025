// client/src/components/NashGame.jsx
import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/nash";

/** Construieste un exemplu dinamic in formatul tabelului: "(<p1>, <p2>)" */
function exampleFromTable(p1 = [], p2 = []) {
  const a = p1[0] ?? "A";
  const b = p2[0] ?? "B";
  return `(${a}, ${b})`;
}

export default function NashGame() {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);

  const [correctEquilibria, setCorrectEquilibria] = useState([]);
  const [solutionShown, setSolutionShown] = useState(false);
  const [hasTried, setHasTried] = useState(false);

  // 1) Genereaza intrebare random
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

  // 2) Obtine echilibrul corect de la backend (si il salveaza si in state)
  const getCorrectAnswer = async () => {
    if (!question) return [];
    try {
      const res = await axios.post(`${API_URL}/solve`, {
        p1_payoffs: question.p1_payoffs,
        p2_payoffs: question.p2_payoffs,
        p1_strategies: question.p1_strategies,
        p2_strategies: question.p2_strategies,
      });
      const eq = res.data.equilibria.map((e) => e.name); // ex: "(D, R)"
      setCorrectEquilibria(eq);
      return eq;
    } catch (err) {
      console.error("Eroare la /solve:", err);
      return [];
    }
  };

  // 3) Evalueaza raspunsul studentului FOLOSIND /evaluate (backend face tot scorul)
  const evaluateAnswer = async () => {
    if (!question) return;
    setHasTried(true);

    try {
      // ne asiguram ca avem echilibrele corecte pentru jocul curent
      const correct = await getCorrectAnswer();

      // trimitem raspunsul brut + lista de echilibre la backend
      const res = await axios.post(`${API_URL}/evaluate`, {
        student_answer: answer,
        correct_equilibria: correct,
      });

      setResult(res.data);
    } catch (err) {
      console.error("Eroare la /evaluate:", err);
      setResult({
        score: 0,
        feedback: "A apărut o eroare la evaluare. Încearcă din nou.",
      });
    }
  };

  // 4) Afiseaza solutia (inclusiv cand nu exista NE pur)
  const handleShowSolution = async () => {
    if (!question) return;
    if (correctEquilibria.length === 0) {
      await getCorrectAnswer(); // poate întoarce []
    }
    setSolutionShown(true);
  };

  const dynamicPlaceholder = question
    ? `Scrie răspunsul tău aici, ex: ${exampleFromTable(
        question.p1_strategies,
        question.p2_strategies
      )} sau 'Nu există echilibru Nash pur.'`
    : "Scrie răspunsul tău aici…";

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
            placeholder={dynamicPlaceholder}
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

      {solutionShown && (
        <div className="result-box" style={{ marginTop: 12 }}>
          <h3>Răspuns corect</h3>
          <p>
            {correctEquilibria.length
              ? correctEquilibria.join(", ")
              : "Nu există echilibru Nash pur."}
          </p>
          <p style={{ fontSize: 13, opacity: 0.8 }}>
            (Echilibrul Nash în strategii pure există la intersecția
            răspunsurilor optime: pe fiecare coloană maximizăm payoff-ul
            Jucătorului 1, iar pe fiecare rând maximizăm payoff-ul Jucătorului
            2.)
          </p>
        </div>
      )}
    </div>
  );
}
