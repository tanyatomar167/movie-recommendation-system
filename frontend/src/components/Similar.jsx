import { useState } from "react";
import { getSimilarMovies } from "../api";
import MovieCard from "./MovieCard";

function Similar() {
  const [movieId, setMovieId] = useState("1");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const findSimilarMovies = async () => {
    const id = Number(movieId);

    if (!id || id < 1) {
      setError("Please enter a valid Movie ID.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await getSimilarMovies(id, 10);

      setMovies(data.similar_movies || []);
    } catch (err) {
      setError("Unable to load similar movies.");
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="similar-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">CONTENT-BASED DISCOVERY</p>

          <h1>Similar Movies</h1>

          <p className="page-description">
            Find movies similar to a movie from the catalog.
          </p>
        </div>
      </div>

      <div className="search-panel">
        <label htmlFor="movieId">Movie ID</label>

        <div className="input-row">
          <input
            id="movieId"
            type="number"
            min="1"
            value={movieId}
            onChange={(e) => setMovieId(e.target.value)}
            placeholder="Enter Movie ID"
          />

          <button
            className="primary-button"
            onClick={findSimilarMovies}
          >
            {loading ? "Searching..." : "Find Similar Movies"}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!loading && movies.length === 0 && !error && (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>

          <h2>Find similar movies</h2>

          <p>
            Enter a Movie ID and we'll find movies with similar
            content.
          </p>
        </div>
      )}

      {movies.length > 0 && (
        <>
          <div className="section-heading">
            <h2>Similar Movies</h2>
            <span>{movies.length} results</span>
          </div>

          <div className="movie-grid">
            {movies.map((movie) => (
              <MovieCard
                key={movie.movie_id}
                movie={movie}
                type="similar"
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Similar;