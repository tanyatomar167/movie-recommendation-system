import React, { useState } from "react";
import { api } from "../api";

function Recommend({ userId = 1 }) {
  const [uid, setUid] = useState(userId);
  const [n, setN] = useState(10);
  const [useHybrid, setUseHybrid] = useState(true);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    if (uid < 1 || uid > 943) {
      setError("User ID must be between 1 and 943.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      let data;

      if (useHybrid) {
        data = await api.hybrid(uid, n);
      } else {
        data = await api.recommend(uid, n);
      }

      setRecommendations(data.recommendations || []);
    } catch (err) {
      console.error("Recommendation error:", err);

      // Fallback to normal SVD recommendations
      if (useHybrid) {
        try {
          const data = await api.recommend(uid, n);
          setRecommendations(data.recommendations || []);
          setError("Hybrid recommendation failed. Showing normal recommendations.");
        } catch (fallbackError) {
          setError(fallbackError.message);
        }
      } else {
        setError(err.message);
      }
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

        <button onClick={load} disabled={loading}>
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </div>

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      <div className="recommendation-list">
        {recommendations.map((movie) => {
          const genres = Array.isArray(movie.genres)
            ? movie.genres
            : typeof movie.genres === "string"
              ? movie.genres.split("|")
              : [];

          return (
            <div className="movie-card" key={movie.movie_id}>
              <h3>{movie.title}</h3>

              <div className="genres">
                {genres.map((genre) => (
                  <span key={genre} className="genre">
                    {genre}
                  </span>
                ))}
              </div>

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

      {!loading && recommendations.length === 0 && !error && (
        <p>No recommendations yet. Enter a User ID and click the button.</p>
      )}
    </div>
  );
}

export default Recommend;