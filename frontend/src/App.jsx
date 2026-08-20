import { useEffect, useState } from "react";
import { getStats } from "./api";

import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import Recommend from "./components/Recommend";
import Similar from "./components/Similar";
import Browse from "./components/Browse";

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [userId, setUserId] = useState(1);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    async function loadStats() {
      try {
        const data = await getStats();
        setStats(data);
      } catch (error) {
        console.error("Stats error:", error);
      }
    }

    loadStats();
  }, []);

  const handleRecommend = (id) => {
    setUserId(id);
    setActivePage("recommend");
  };

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        stats={stats}
      />

      <main className="main-content">

  <header className="top-header">
    <div>
      <p className="eyebrow">MOVIE DISCOVERY</p>

      <h1>Find your next favorite movie</h1>

      <p className="header-subtitle">
        Personalized recommendations powered by machine learning.
      </p>
    </div>

    <div className="header-badge">
      ● AI Recommendation Engine
    </div>
  </header>

  {activePage === "dashboard" && (
    <Dashboard onRecommend={handleRecommend} />
  )}

  {activePage === "recommend" && (
    <Recommend userId={userId} />
  )}

  {activePage === "similar" && <Similar />}

  {activePage === "browse" && <Browse />}

</main>
    </div>
  );
}

export default App;