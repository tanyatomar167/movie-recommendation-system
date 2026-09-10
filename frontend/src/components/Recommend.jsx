import { useState } from "react";

const API_URL = "https://movie-recommendation-system-4p8t.onrender.com";

function Recommend({ userId = 1 }) {
  const [uid, setUid] = useState(userId);
  const [n, setN] = useState(10);
  const [useHybrid, setUseHybrid] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadRecommendations = async () => {
    if (uid < 1 || uid > 943) {
      setError("User ID must be between 1 and 943.");
      return;
    }

    if (n < 1 || n > 50) {
      setError("Number of movies must be between 1 and 50.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const endpoint = useHybrid
        ? `/hybrid/${uid}?n=${n}`
        : `/recommend/${uid}?n=${n}`;

      const response = await fetch(API_URL + endpoint);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      console.log("Recommendation API response:", data);

      if (!data.recommendations) {
        throw new Error("No recommendations received from API.");
      }

      setRecommendations(data.recommendations);
    } catch (err) {
      console.error("Recommendation error:", err);
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
        <p>
          Loading recommendations...
        </p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {!loading && recommendations.length > 0 && (
        <div className="recommendation-list">

          {recommendations.map((movie) => {

            const genres = Array.isArray(movie.genres)
              ? movie.genres
              : typeof movie.genres === "string"
                ? movie.genres.split("|")
                : [];

            return (
              <div
                className="movie-card"
                key={movie.movie_id}
              >

                <h3>{movie.title}</h3>

                {genres.length > 0 && (
                  <div className="genres">
                    {genres.map((genre) => (
                      <span
                        className="genre"
                        key={genre}
                      >
                        {genre}
                      </span>
                    ))}
                  </div>
                )}

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
            );
          })}

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