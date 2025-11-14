import { NavLink, Route, Routes } from "react-router-dom";

import ClassifierArcade from "./pages/ClassifierArcade";
import Home from "./pages/Home";
import TrainingLab from "./pages/TrainingLab";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/training-lab", label: "Training Lab" },
  { to: "/classifier-arcade", label: "Classifier Arcade" }
];

const App = () => {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="logo">
          <span role="img" aria-label="popcorn">
            🍿
          </span>
          <h1>Movie Review Mood Arcade</h1>
        </div>
        <nav className="main-nav">
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
              end={link.to === "/"}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/training-lab" element={<TrainingLab />} />
          <Route path="/classifier-arcade" element={<ClassifierArcade />} />
        </Routes>
      </main>
      <footer className="app-footer">
        <p>
          Crafted with ✨ whimsy ✨ using FastAPI + React. Drop your hottest takes and
          let the classifier vibe-check them!
        </p>
      </footer>
    </div>
  );
};

export default App;
