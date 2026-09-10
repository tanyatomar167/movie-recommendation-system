import { useEffect, useState } from "react";
import { api } from "./api";

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
        const data = await api.stats();
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