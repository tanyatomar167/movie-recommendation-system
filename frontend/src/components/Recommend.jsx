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

      const response = await fetch(API_URL + endpoint);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      if (!Array.isArray(data.recommendations)) {
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
    <div className="recommend-page">

      {/* Header */}
      <div className="recommend-header">
        <div>
          <h1>🎬 Movie Recommendations</h1>
          <p>
            Personalized movie suggestions based on your preferences
          </p>
        </div>
      </div>

      {/* Controls */}
      <div className="recommend-controls">

        <div className="control-group">
          <label>User ID</label>

          <input
            type="number"
            min="1"
            max="943"
            value={uid}
            onChange={(e) => setUid(Number(e.target.value))}
          />
        </div>

        <div className="control-group">
          <label>Number of Movies</label>

          <select
            value={n}
            onChange={(e) => setN(Number(e.target.value))}
          >
            <option value={5}>5 Movies</option>
            <option value={10}>10 Movies</option>
            <option value={15}>15 Movies</option>
            <option value={20}>20 Movies</option>
          </select>
        </div>

        <label className="hybrid-option">
          <input
            type="checkbox"
            checked={useHybrid}
            onChange={(e) => setUseHybrid(e.target.checked)}
          />

          <span>Use Hybrid Recommendation</span>
        </label>

        <button
          className="recommend-button"
          type="button"
          onClick={loadRecommendations}
          disabled={loading}
        >
          {loading ? "⏳ Loading..." : "▶ Get Recommendations"}
        </button>

      </div>

      {/* Error */}
      {error && (
        <div className="recommend-error">
          ⚠ {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="recommend-loading">
          <div className="loading-icon">🎬</div>
          <p>Finding movies you may like...</p>
        </div>
      )}

      {/* Results */}
      {!loading && recommendations.length > 0 && (
        <div className="results-section">

          <div className="results-header">
            <div>
              <h2>Recommended for You</h2>
              <p>
                Top {recommendations.length} movie picks for User {uid}
              </p>
            </div>

            <span className="result-count">
              {recommendations.length} Movies
            </span>
          </div>

          <div className="movie-grid">

            {recommendations.map((movie, index) => {

              const genres = Array.isArray(movie.genres)
                ? movie.genres
                : typeof movie.genres === "string"
                  ? movie.genres.split("|")
                  : [];

              const rating =
                movie.predicted_rating !== undefined
                  ? Number(movie.predicted_rating)
                  : null;

              const hybrid =
                movie.hybrid_score !== undefined
                  ? Number(movie.hybrid_score)
                  : null;

              return (
                <div
                  className="real-movie-card"
                  key={movie.movie_id ?? index}
                >

                  {/* Poster */}
                  <div className="movie-poster">

                    <div className="poster-rank">
                      #{index + 1}
                    </div>

                    <div className="poster-icon">
                      🎬
                    </div>

                    <div className="poster-title">
                      {movie.title}
                    </div>

                  </div>

                  {/* Movie Details */}
                  <div className="movie-details">

                    <h3>
                      {movie.title}
                    </h3>

                    {/* Genres */}
                    {genres.length > 0 && (
                      <div className="movie-genres">

                        {genres.slice(0, 3).map((genre, i) => (
                          <span
                            key={`${genre}-${i}`}
                            className="genre-pill"
                          >
                            {genre}
                          </span>
                        ))}

                      </div>
                    )}

                    {/* Rating */}
                    {rating !== null && (
                      <div className="rating-row">

                        <span className="rating-label">
                          ⭐ Predicted Rating
                        </span>

                        <strong>
                          {rating.toFixed(2)}
                        </strong>

                      </div>
                    )}

                    {/* Rating Bar */}
                    {rating !== null && (
                      <div className="rating-bar">

                        <div
                          className="rating-fill"
                          style={{
                            width: `${Math.min(
                              100,
                              (rating / 5) * 100
                            )}%`
                          }}
                        />

                      </div>
                    )}

                    {/* Hybrid */}
                    {hybrid !== null && (
                      <div className="hybrid-score">
                        <span>Hybrid Score</span>

                        <strong>
                          {hybrid.toFixed(3)}
                        </strong>
                      </div>
                    )}

                  </div>

                </div>
              );
            })}

          </div>
        </div>
      )}

      {/* Empty */}
      {!loading &&
        !error &&
        recommendations.length === 0 && (

          <div className="recommend-empty">

            <div className="empty-movie-icon">
              🎬
            </div>

            <h2>Discover Your Next Movie</h2>

            <p>
              Enter a User ID and click
              <strong> Get Recommendations </strong>
              to discover movies you may enjoy.
            </p>

          </div>
        )}

    </div>
  );
}

export default Recommend;