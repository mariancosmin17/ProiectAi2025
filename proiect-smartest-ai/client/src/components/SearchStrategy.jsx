import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/search";

export default function SearchStrategy() {
  const [difficulty, setDifficulty] = useState("medium");
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [solution, setSolution] = useState(null);
  const [solutionShown, setSolutionShown] = useState(false);
  const [hasTried, setHasTried] = useState(false);

  // Generează întrebare
  const generateQuestion = async () => {
    try {
      const res = await axios.get(`${API_URL}/generate`, {
        params: { difficulty },
      });
      setQuestion(res.data);
      setAnswer("");
      setResult(null);
      setSolution(null);
      setSolutionShown(false);
      setHasTried(false);
    } catch (err) {
      alert("Eroare la generarea întrebării.");
      console.error(err);
    }
  };

  // Evaluează răspunsul
  const evaluateAnswer = async () => {
    if (!question) return;
    setHasTried(true);

    try {
      const res = await axios.post(`${API_URL}/evaluate`, {
        problem_name: question.problem_name,
        student_answer: answer,
        instance_description: question.instance_description,
      });
      setResult(res. data);
    } catch (err) {
      console.error("Eroare la evaluare:", err);
      setResult({
        score: 0,
        feedback: "A apărut o eroare la evaluare.",
        correct_answer: "N/A",
      });
    }
  };

  // Afișează soluția
  const showSolution = async () => {
    if (!question) return;

    try {
      const res = await axios.post(`${API_URL}/solve`, {
        problem_name: question.problem_name,
        instance_description: question.instance_description,
      });
      setSolution(res. data);
      setSolutionShown(true);
    } catch (err) {
      console.error("Eroare la /solve:", err);
      alert("Eroare la obținerea soluției.");
    }
  };

  return (
    <div className="container">
      <h2>🔍 Search Problem Identification</h2>
      <p className="subtitle">
        Identifică strategia de căutare optimă pentru probleme clasice de AI
      </p>

      <div className="controls">
        <label>
          <strong>Dificultate:</strong>
          <select value={difficulty} onChange={(e) => setDifficulty(e. target.value)}>
            <option value="easy">Easy (3 opțiuni)</option>
            <option value="medium">Medium (5 opțiuni)</option>
            <option value="hard">Hard (7 opțiuni + explicație)</option>
          </select>
        </label>
        <button onClick={generateQuestion}>Generează întrebare</button>
      </div>

      {question && (
        <div className="question-box">
          <h3>Întrebare:</h3>
          <div className="question-text">
            {question.question_text. split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>

          <textarea
            placeholder="Scrie răspunsul tău aici..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={difficulty === "hard" ? 6 : 3}
          />

          <div className="button-group">
            <button onClick={evaluateAnswer}>Evaluează răspunsul</button>
            <button
              onClick={showSolution}
              disabled={!hasTried}
              title={hasTried ? "" : "Răspunde mai întâi"}
            >
              Afișează soluția
            </button>
          </div>
        </div>
      )}

      {result && (
        <div className="result-box">
          <h3>📊 Rezultatul evaluării</h3>
          <div className="score-badge" data-score={result.score}>
            <strong>Scor:</strong> {result.score}/100
          </div>
          <div className="feedback">
            {result.feedback. split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
          {result.detailed_analysis && (
            <p className="analysis">
              <em>📝 {result.detailed_analysis}</em>
            </p>
          )}
        </div>
      )}

      {solutionShown && solution && (
        <div className="solution-box">
          <h3>✅ Soluție corectă</h3>
          <p>
            <strong>Strategie optimă:</strong> {solution.optimal_strategy}
          </p>
          <p>
            <strong>Alternative acceptabile:</strong>{" "}
            {solution. alternative_strategies.join(", ")}
          </p>
          <div className="explanation">
            <strong>Explicație:</strong>
            <p>{solution.explanation}</p>
          </div>
        </div>
      )}
    </div>
  );
}