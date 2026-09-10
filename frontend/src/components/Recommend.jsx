import { useState } from "react";

const API_URL = "https://movie-recommendation-system-4p8t.onrender.com";

function Recommend({ userId = 1 }) {
  const [uid, setUid] = useState(Number(userId));
  const [n, setN] = useState(10);
  const [useHybrid, setUseHybrid] = useState(false);

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadRecommendations = async () => {
    const user = Number(uid);
    const count = Number(n);

    if (!Number.isInteger(user) || user < 1 || user > 943) {
      setError("User ID must be between 1 and 943.");
      return;
    }

    if (!Number.isInteger(count) || count < 1 || count > 50) {
      setError("Number of movies must be between 1 and 50.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const endpoint = useHybrid
        ? `/hybrid/${user}?n=${count}`
        : `/recommend/${user}?n=${count}`;

      console.log("Calling:", API_URL + endpoint);

      const response = await fetch(API_URL + endpoint);

      console.log("Status:", response.status);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      console.log("API Response:", data);

      if (!data.recommendations) {
        throw new Error("No recommendations received.");
      }

      setRecommendations(data.recommendations);

    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to load recommendations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">

      <h1>Movie Recommendations</h1>

      <div className="controls">

        <div>
          <label>User ID</label>

          <input
            type="number"
            min="1"
            max="943"
            value={uid}
            onChange={(e) => setUid(Number(e.target.value))}
          />
        </div>

        <div>
          <label>Number of Movies</label>

          <input
            type="number"
            min="1"
            max="50"
            value={n}
            onChange={(e) => setN(Number(e.target.value))}
          />
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={useHybrid}
              onChange={(e) => setUseHybrid(e.target.checked)}
            />

            Use Hybrid Recommendation
          </label>
        </div>

        <button
          type="button"
          onClick={loadRecommendations}
          disabled={loading}
        >
          {loading ? "Loading..." : "Get Recommendations"}
        </button>

      </div>

      {loading && (
        <p>Loading recommendations...</p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {/* RESULTS */}
      {!loading && recommendations.length > 0 && (
        <div className="recommendation-list">

          <h2>
            Recommended Movies
          </h2>

          {recommendations.map((movie, index) => (

            <div
              className="movie-card"
              key={movie.movie_id ?? index}
            >

              <div>
                <strong>
                  #{index + 1}
                </strong>
              </div>

              <h3>
                {movie.title}
              </h3>

              {movie.predicted_rating !== undefined && (
                <p>
                  Predicted Rating:{" "}
                  <strong>
                    {Number(movie.predicted_rating).toFixed(2)}
                  </strong>
                </p>
              )}

              {movie.hybrid_score !== undefined && (
                <p>
                  Hybrid Score:{" "}
                  <strong>
                    {Number(movie.hybrid_score).toFixed(3)}
                  </strong>
                </p>
              )}

            </div>

          ))}

        </div>
      )}

      {!loading &&
        !error &&
        recommendations.length === 0 && (
          <p>
            Enter a User ID and click Get Recommendations.
          </p>
        )}

    </div>
  );
}

export default Recommend;