import { useEffect, useState } from "react";

function Recommend({ userId }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRecommendations() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `/api/hybrid/${userId}?n=10`
        );

        if (!response.ok) {
          throw new Error("Failed to load recommendations");
        }

        const data = await response.json();

        setRecommendations(data.recommendations || []);
      } catch (err) {
        console.error(err);
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

      {!loading && !error && (
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