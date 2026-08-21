import { useEffect, useState } from "react";
import { getHybridRecommendations } from "../api";

function Recommend({ userId }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRecommendations() {
      try {
        setLoading(true);
        setError("");

        const data = await getHybridRecommendations(userId, 10);

        setRecommendations(data.recommendations || []);
      } catch (err) {
        console.error("Recommendation error:", err);
        setError("Unable to load recommendations.");
      } finally {
        setLoading(false);
      }
    }

    loadRecommendations();
  }, [userId]);

  return (
    <section>
      <div className="page-heading">
        <p className="section-label">
          PERSONALIZED DISCOVERY
        </p>

        <h2>Recommended Movies</h2>

        <p>
          Hybrid recommendations for User #{userId}
        </p>
      </div>

      {loading && (
        <div className="loading-message">
          Finding movies for you...
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!loading && !error && recommendations.length === 0 && (
        <div className="empty-state">
          No recommendations found.
        </div>
      )}

      {!loading && !error && recommendations.length > 0 && (
        <div className="recommendation-grid">
          {recommendations.map((movie, index) => (
            <div
              className="recommendation-card"
              key={movie.movie_id}
            >
              <div className="recommendation-number">
                #{index + 1}
              </div>

              <div className="movie-poster">
                🎬
              </div>

              <h3>{movie.title}</h3>

              <p>
                Predicted rating:{" "}
                <strong>
                  ⭐ {movie.predicted_rating}
                </strong>
              </p>

              <span className="hybrid-score">
                Hybrid score: {movie.hybrid_score}
              </span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default Recommend;