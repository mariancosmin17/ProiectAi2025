import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/nash";

/** Construieste un exemplu dinamic in formatul tabelului: "(<p1>, <p2>)" */
function exampleFromTable(p1 = [], p2 = []) {
  const a = p1[0] ?? "A";
  const b = p2[0] ?? "B";
  return `(${a}, ${b})`;
}

/** Cauta un token (case-insensitive) in lista de etichete si intoarce forma canonica (exact cum apare in tabel). */
function matchLabel(token, allowed) {
  if (!token) return null;
  const t = token.trim().toLowerCase();
  const idx = allowed.findIndex((x) => x.trim().toLowerCase() === t);
  return idx >= 0 ? allowed[idx] : null;
}

/** Parseaza raspunsul utilizatorului si intoarce [tokP1, tokP2] sau null. Accepta virgula sau spatii. */
function parseAnswer(raw) {
  if (!raw) return null;
  const s = raw.replace(/[()]/g, " ");
  // Incearca intai prin virgula
  let parts = s.split(",").map((x) => x.trim()).filter(Boolean);
  if (parts.length === 1) {
    // Daca nu e virgula, sparge prin spatii
    parts = s.split(/\s+/).map((x) => x.trim()).filter(Boolean);
  }
  if (parts.length >= 2) return [parts[0], parts[1]];
  return null;
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

  // 2) Obtine echilibrul corect de la backend
  const getCorrectAnswer = async () => {
    if (!question) return [];
    try {
      const res = await axios.post(`${API_URL}/solve`, {
        p1_payoffs: question.p1_payoffs,
        p2_payoffs: question.p2_payoffs,
        p1_strategies: question.p1_strategies,
        p2_strategies: question.p2_strategies,
      });
      const eq = res.data.equilibria.map((e) => e.name); // ex: "(D, R)" exact in etichetele tabelului
      setCorrectEquilibria(eq);
      return eq;
    } catch (err) {
      console.error("Eroare la /solve:", err);
      return [];
    }
  };

  // 3) Evalueaza raspunsul studentului
  const evaluateAnswer = async () => {
    setHasTried(true);

    // folosim mereu solutia curenta pentru jocul afisat
    const correct = await getCorrectAnswer();

    // daca nu exista NE pur -> acceptam orice raspuns care contine "nu"
    if (correct.length === 0) {
      const hasNu = (answer || "").trim().toLowerCase().includes("nu");
      setResult({
        score: hasNu ? 100 : 0,
        feedback: hasNu
          ? "Corect — nu există echilibru Nash pur."
          : "Răspuns incorect. Pentru acest joc nu există echilibru Nash pur.",
      });
      return;
    }

    // validare stricta pe etichetele din tabel
    const tokens = parseAnswer(answer);
    if (!tokens) {
      setResult({
        score: 0,
        feedback:
          "Format invalid. Scrie răspunsul ca în exemplu, de forma (P1, P2), folosind exact etichetele din tabel.",
      });
      return;
    }

    const [tokP1, tokP2] = tokens;

    const p1Canon = matchLabel(tokP1, question.p1_strategies);
    const p2Canon = matchLabel(tokP2, question.p2_strategies);

    if (!p1Canon || !p2Canon) {
      setResult({
        score: 0,
        feedback:
          "Folosește exact etichetele din tabel (inclusiv diacritice dacă apar). De ex: " +
          exampleFromTable(question.p1_strategies, question.p2_strategies),
      });
      return;
    }

    const normalizedUser = `(${p1Canon}, ${p2Canon})`;

    // match case-insensitive cu solutiile corecte
    const matched = correct.some(
      (x) => x.trim().toLowerCase() === normalizedUser.trim().toLowerCase()
    );

    setResult({
      score: matched ? 100 : 0,
      feedback: matched
        ? "Corect! Ai identificat echilibrul Nash."
        : "Răspuns incorect. Încearcă să identifici intersecția răspunsurilor optime.",
    });
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
            (Echilibrul Nash în strategii pure există la intersecția răspunsurilor
            optime: pe fiecare coloană maximizăm payoff-ul Jucătorului 1, iar pe
            fiecare rând maximizăm payoff-ul Jucătorului 2.)
          </p>
        </div>
      )}
    </div>
  );
}
