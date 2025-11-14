const Home = () => {
  return (
    <section className="panel home-panel">
      <div className="panel-card">
        <h2>Welcome to the Mood Arcade 🎮</h2>
        <p>
          This experimental playground dusts off a classic Naive Bayes movie-review
          classifier and gives it a neon makeover. Bounce between tabs to learn the
          project&apos;s lore, remix the training data, and throw in your own dramatic monologues.
        </p>
        <p>
          Think of it as a quirky lab where probability meets popcorn. Every action you
          take updates the FastAPI backend, which keeps track of word vibes and shoots
          instant feedback to this React interface.
        </p>
        <div className="info-grid">
          <div className="info-card">
            <h3>📚 Lore Room</h3>
            <p>
              Peek at what this project is about, where the training data comes from, and how
              a Bayes classifier makes judgement calls with nothing but word counts.
            </p>
          </div>
          <div className="info-card">
            <h3>🧪 Training Lab</h3>
            <p>
              Mix in your own fresh and rotten snippets, tweak smoothing, and retrain the
              classifier in real time. We&apos;ll even spotlight the most distinctive words.
            </p>
          </div>
          <div className="info-card">
            <h3>🎯 Classifier Arcade</h3>
            <p>
              Drop a review, press launch, and watch the arcade lights declare whether it&apos;s
              Fresh or Rotten. Keep an eye on the probability meter and your token score.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Home;
