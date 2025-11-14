import { isAxiosError } from "axios";
import { useMemo, useState } from "react";

import { trainModel } from "../api";
import type { TrainResponse } from "../api/types";
import WordBadge from "../components/WordBadge";

const TrainingLab = () => {
  const [freshDraft, setFreshDraft] = useState("");
  const [rottenDraft, setRottenDraft] = useState("");
  const [freshSamples, setFreshSamples] = useState<string[]>([]);
  const [rottenSamples, setRottenSamples] = useState<string[]>([]);
  const [useDefault, setUseDefault] = useState(true);
  const [alpha, setAlpha] = useState(1);
  const [isTraining, setIsTraining] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<TrainResponse | null>(null);

  const totalSamples = useMemo(
    () => freshSamples.length + rottenSamples.length,
    [freshSamples, rottenSamples]
  );

  const addFreshSample = () => {
    if (!freshDraft.trim()) return;
    setFreshSamples((prev) => [...prev, freshDraft.trim()]);
    setFreshDraft("");
  };

  const addRottenSample = () => {
    if (!rottenDraft.trim()) return;
    setRottenSamples((prev) => [...prev, rottenDraft.trim()]);
    setRottenDraft("");
  };

  const handleTrain = async () => {
    setIsTraining(true);
    setError(null);
    try {
      const result = await trainModel({
        fresh_samples: freshSamples,
        rotten_samples: rottenSamples,
        use_default_dataset: useDefault,
        alpha
      });
      setSummary(result);
    } catch (err) {
      if (isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as { detail?: string }).detail;
        setError(detail ?? "Training ran into an unexpected glitch.");
      } else {
        setError(
          err instanceof Error
            ? err.message
            : "Training ran into an unexpected glitch."
        );
      }
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <section className="panel training-panel">
      <div className="panel-card">
        <h2>Training Lab 🧪</h2>
        <p>
          Toss in your own snippets to rewire the classifier. Combine them with the
          original dataset or go fully custom for chaotic vibes.
        </p>
        <div className="lab-grid">
          <div className="lab-column">
            <h3>Fresh snippets</h3>
            <textarea
              value={freshDraft}
              onChange={(event) => setFreshDraft(event.target.value)}
              placeholder="Write a joyful reaction..."
            />
            <button className="pill-button fresh" onClick={addFreshSample}>
              Add Fresh Sample
            </button>
            <ul className="sample-list">
              {freshSamples.map((sample, index) => (
                <li key={index}>{sample}</li>
              ))}
            </ul>
          </div>
          <div className="lab-column">
            <h3>Rotten snippets</h3>
            <textarea
              value={rottenDraft}
              onChange={(event) => setRottenDraft(event.target.value)}
              placeholder="Drop a dramatic burn..."
            />
            <button className="pill-button rotten" onClick={addRottenSample}>
              Add Rotten Sample
            </button>
            <ul className="sample-list">
              {rottenSamples.map((sample, index) => (
                <li key={index}>{sample}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="lab-controls">
          <label className="toggle">
            <input
              type="checkbox"
              checked={useDefault}
              onChange={(event) => setUseDefault(event.target.checked)}
            />
            <span>
              Blend with the original mega-dataset
              <small>({useDefault ? "enabled" : "disabled"})</small>
            </span>
          </label>
          <label className="slider">
            <span>Laplace smoothing: {alpha.toFixed(1)}</span>
            <input
              type="range"
              min={0.1}
              max={3}
              step={0.1}
              value={alpha}
              onChange={(event) => setAlpha(Number(event.target.value))}
            />
          </label>
          <div className="lab-summary">
            <span>Custom samples queued: {totalSamples}</span>
            {summary && (
              <span>
                Vocabulary: {summary.vocabulary_size} quirky tokens in play.
              </span>
            )}
          </div>
          <button
            className="pill-button primary"
            onClick={handleTrain}
            disabled={isTraining}
          >
            {isTraining ? "Mixing potions..." : "Retrain the model"}
          </button>
          {error && <p className="error-message">{error}</p>}
        </div>

        {summary && (
          <div className="training-results">
            <h3>Latest training results</h3>
            <p>
              {summary.message} Fresh tokens: {summary.fresh_token_count.toLocaleString()} | Rotten tokens: {" "}
              {summary.rotten_token_count.toLocaleString()}
            </p>
            <div className="word-stacks">
              <div>
                <h4>Fresh spotlight</h4>
                <div className="word-stack">
                  {summary.top_fresh_words.map((word) => (
                    <WordBadge key={word} word={word} tone="fresh" />
                  ))}
                </div>
              </div>
              <div>
                <h4>Rotten spotlight</h4>
                <div className="word-stack">
                  {summary.top_rotten_words.map((word) => (
                    <WordBadge key={word} word={word} tone="rotten" />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default TrainingLab;
