import React, { useState } from "react";
const API = "http://localhost:8000"; // backend URL

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [used, setUsed] = useState("");
  const [contexts, setContexts] = useState([]);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  const askQuestion = async () => {
    setAnswer("...");
    try {
      const res = await fetch(`${API}/solve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      setAnswer(data.answer || "No answer");
      setUsed(data.used || "solver");
      setContexts(data.contexts || []);
    } catch (err) {
      setAnswer("Error contacting backend");
    }
  };

  const sendFeedback = async () => {
    try {
      await fetch(`${API}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, rating, comment })
      });
      alert("Thanks for your feedback!");
      setRating(5);
      setComment("");
    } catch (err) {
      alert("Error sending feedback");
    }
  };

  return (
    <div className="container">
      <h1>📐 Math Routing Agent</h1>
      <textarea
        rows="4"
        placeholder="Ask any math question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={askQuestion}>Solve</button>

      {answer && (
        <div className="answer-box">
          <b>Answer ({used})</b>:
          <div>{answer}</div>
          {contexts.length > 0 && (
            <div className="context-box">
              <b>Contexts:</b>
              <ul>
                {contexts.map((c, i) => (
                  <li key={i}>
                    Q: {c.question} → A: {c.answer}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {answer && (
        <div className="feedback-box">
          <b>Human-in-the-Loop Feedback</b>
          <div>
            Rating: <input type="number" min="1" max="5" value={rating} onChange={(e)=>setRating(parseInt(e.target.value))}/>
          </div>
          <textarea
            rows="3"
            placeholder="Comments / Improvements"
            value={comment}
            onChange={(e)=>setComment(e.target.value)}
          />
          <button onClick={sendFeedback}>Submit Feedback</button>
        </div>
      )}
    </div>
  );
}
