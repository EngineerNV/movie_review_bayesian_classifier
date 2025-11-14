import { isAxiosError } from "axios";
import { useState } from "react";

import { classifyReview } from "../api";
import type { ClassifyResponse } from "../api/types";

interface HistoryItem extends ClassifyResponse {
  review: string;
  timestamp: number;
}

const ClassifierArcade = () => {
  const [review, setReview] = useState("");
  const [result, setResult] = useState<ClassifyResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const triggerClassification = async () => {
    if (!review.trim()) {
      setError("Type a review before launching the arcade!");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await classifyReview({ review });
      setResult(data);
      setHistory((prev) => [
        { ...data, review, timestamp: Date.now() },
        ...prev
      ].slice(0, 6));
    } catch (err) {
      if (isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as { detail?: string }).detail;
        setError(detail ?? "The arcade lights flickered—try again!");
      } else {
        setError(
          err instanceof Error
            ? err.message
            : "The arcade lights flickered—try again!"
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  const renderMeter = () => {
    if (!result) return null;
    const freshPercent = Math.round(result.fresh_probability * 100);
    const rottenPercent = Math.round(result.rotten_probability * 100);

    return (
      <div className="meter">
        <div className="meter-bar fresh" style={{ width: `${freshPercent}%` }}>
          <span>Fresh {freshPercent}%</span>
        </div>
        <div className="meter-bar rotten" style={{ width: `${rottenPercent}%` }}>
          <span>Rotten {rottenPercent}%</span>
        </div>
      </div>
    );
  };

  return (
    <section className="panel arcade-panel">
      <div className="panel-card">
        <h2>Classifier Arcade 🎯</h2>
        <p>
          Bring your most passionate takes and see how the Mood Arcade reacts. The Naive Bayes
          engine returns a probability duet—choose wisely which side to trust!
        </p>
        <textarea
          value={review}
          onChange={(event) => setReview(event.target.value)}
          placeholder="Type your cinematic masterpiece or rant..."
        />
        <button
          className="pill-button primary"
          onClick={triggerClassification}
          disabled={isLoading}
        >
          {isLoading ? "Crunching tokens..." : "Launch classification"}
        </button>
        {error && <p className="error-message">{error}</p>}

        {result && (
          <div className="arcade-results">
            <h3>
              Verdict: <span className={result.label.toLowerCase()}>{result.label}</span>
            </h3>
            {renderMeter()}
            <p className="token-display">
              Tokens analysed: {result.tokens_considered.length}
            </p>
            <p className="token-stream">
              {result.tokens_considered.join(" · ")}
            </p>
          </div>
        )}

        {history.length > 0 && (
          <div className="history">
            <h3>Recent plays</h3>
            <ul>
              {history.map((item) => (
                <li key={item.timestamp}>
                  <span className={`badge ${item.label.toLowerCase()}`}>
                    {item.label}
                  </span>
                  <blockquote>{item.review}</blockquote>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
};

export default ClassifierArcade;
