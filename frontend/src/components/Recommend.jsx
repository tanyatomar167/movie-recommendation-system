import React, { useState } from "react";

const API_URL = "https://movie-recommendation-system-4p8t.onrender.com";

export default function Recommend() {
  const [userId, setUserId] = useState("");
  const [n, setN] = useState(10);
  const [useHybrid, setUseHybrid] = useState(false);

  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadRecommendations() {
    const uid = parseInt(userId, 10);

    if (!uid || uid < 1 || uid > 943) {
      setError("Please enter a valid User ID between 1 and 943.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations(null);

    try {
      const endpoint = useHybrid
        ? `/hybrid/${uid}?n=${n}`
        : `/recommend/${uid}?n=${n}`;

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
      console.error("Recommendation error:", err);
      setError(err.message || "Failed to load recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="recommend-page">

      {/* ================= HEADER ================= */}

      <div className="recommend-header">

        <div>
          <div className="recommend-eyebrow">
            PERSONALIZED MOVIE DISCOVERY
          </div>

          <h1>
            ✦ Recommendations
          </h1>

          <p>
            Discover movies selected for you using machine learning
            and movie genre preferences.
          </p>
        </div>

        <div className="recommend-header-badge">
          🎬 AI Powered
        </div>

      </div>


      {/* ================= CONTROL PANEL ================= */}

      <div className="recommend-controls">

        <div className="control-group">

          <label>
            User ID
          </label>

          <input
            type="number"
            placeholder="1 – 943"
            min="1"
            max="943"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                loadRecommendations();
              }
            }}
          />

        </div>


        <div className="control-group">

          <label>
            Results
          </label>

          <select
            value={n}
            onChange={(e) => setN(Number(e.target.value))}
          >
            <option value={5}>5 movies</option>
            <option value={10}>10 movies</option>
            <option value={15}>15 movies</option>
            <option value={20}>20 movies</option>
          </select>

        </div>


        <label className="hybrid-option">

          <input
            type="checkbox"
            checked={useHybrid}
            onChange={(e) => setUseHybrid(e.target.checked)}
          />

          <span>
            Use hybrid model
          </span>

        </label>


        <button
          className="recommend-button"
          onClick={loadRecommendations}
          disabled={!userId || loading}
        >
          {loading
            ? "⏳ Finding movies..."
            : "▶ Recommend Movies"}
        </button>

      </div>


      {/* ================= ERROR ================= */}

      {error && (
        <div className="recommend-error">
          ⚠ {error}
        </div>
      )}


      {/* ================= LOADING ================= */}

      {loading && (
        <div className="recommend-loading">

          <div className="loading-icon">
            🎬
          </div>

          <h3>
            Finding movies for you...
          </h3>

          <p>
            Our recommendation model is analyzing your preferences.
          </p>

        </div>
      )}


      {/* ================= RESULTS ================= */}

      {!loading &&
        recommendations &&
        recommendations.length > 0 && (

          <div className="results-section">

            <div className="results-header">

              <div>

                <h2>
                  Recommended for You
                </h2>

                <p>
                  Top {recommendations.length} picks for User {userId}
                </p>

              </div>

              <div className="result-count">
                {recommendations.length} Movies
              </div>

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

                const yearMatch =
                  movie.title?.match(/\((\d{4})\)/);

                const year =
                  yearMatch ? yearMatch[1] : "";

                const cleanTitle =
                  movie.title?.replace(/\s*\(\d{4}\)\s*$/, "");

                return (

                  <div
                    className="real-movie-card"
                    key={movie.movie_id ?? index}
                  >

                    {/* ================= POSTER ================= */}

                    <div className="movie-poster">

                      <div className="poster-rank">
                        #{index + 1}
                      </div>

                      <div className="poster-icon">
                        🎬
                      </div>

                      <div className="poster-title">
                        {cleanTitle}
                        {year && ` (${year})`}
                      </div>

                    </div>


                    {/* ================= DETAILS ================= */}

                    <div className="movie-details">

                      <h3>
                        {cleanTitle}
                      </h3>

                      {year && (
                        <div className="movie-year">
                          {year}
                        </div>
                      )}


                      {/* GENRES */}

                      {genres.length > 0 && (

                        <div className="movie-genres">

                          {genres
                            .filter(Boolean)
                            .slice(0, 3)
                            .map((genre, i) => (

                              <span
                                className="genre-pill"
                                key={`${genre}-${i}`}
                              >
                                {genre}
                              </span>

                            ))}

                        </div>

                      )}


                      {/* RATING */}

                      {rating !== null && (

                        <>

                          <div className="rating-row">

                            <span className="rating-label">
                              ⭐ Predicted Rating
                            </span>

                            <strong>
                              {rating.toFixed(2)}
                            </strong>

                          </div>


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

                        </>

                      )}


                      {/* HYBRID */}

                      {hybrid !== null && (

                        <div className="hybrid-score">

                          <span>
                            AI Match Score
                          </span>

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


      {/* ================= NO RESULTS ================= */}

      {!loading &&
        !error &&
        recommendations &&
        recommendations.length === 0 && (

          <div className="recommend-empty">

            <div className="empty-movie-icon">
              🎬
            </div>

            <h2>
              No Recommendations Found
            </h2>

            <p>
              Try another User ID or increase the number of results.
            </p>

          </div>

        )}


      {/* ================= INITIAL STATE ================= */}

      {!loading &&
        !error &&
        !recommendations && (

          <div className="recommend-empty">

            <div className="empty-movie-icon">
              ✦
            </div>

            <h2>
              Discover Your Next Favorite Movie
            </h2>

            <p>
              Enter a User ID above and let the recommendation
              system find movies you may enjoy.
            </p>

          </div>

        )}

    </div>
  );
}