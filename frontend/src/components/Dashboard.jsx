import { useState } from "react";

function Dashboard({ onRecommend }) {
  const [userId, setUserId] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();

    const id = Number(userId);

    if (id >= 1) {
      onRecommend(id);
    }
  };

  return (
    <section className="dashboard">
      <div className="welcome-section">
        <div>
          <p className="section-label">RECOMMENDATION ENGINE</p>

          <h2>Discover movies you'll love.</h2>

          <p>
            Enter a user ID and let the SVD recommendation model
            find personalized movies from the catalog.
          </p>
        </div>
      </div>

      <div className="quick-recommend">
        <div>
          <p className="section-label">QUICK RECOMMEND</p>

          <h3>Get personalized recommendations</h3>

          <p>
            Recommendations are generated using your trained
            machine-learning model.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="recommend-form">
          <label htmlFor="userId">User ID</label>

          <div className="input-row">
            <input
              id="userId"
              type="number"
              min="1"
              max="943"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />

            <button type="submit">
              Recommend →
            </button>
          </div>

          <small>
            Valid users: 1–943
          </small>
        </form>
      </div>

      <div className="dashboard-grid">
        <div className="info-card">
          <span>🤖</span>
          <div>
            <strong>SVD Model</strong>
            <p>Personalized rating prediction</p>
          </div>
        </div>

        <div className="info-card">
          <span>🎯</span>
          <div>
            <strong>Content-Based</strong>
            <p>Find similar movies</p>
          </div>
        </div>

        <div className="info-card">
          <span>⚡</span>
          <div>
            <strong>Hybrid System</strong>
            <p>Combines recommendation signals</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Dashboard;