import { useState } from "react";
import { api } from "../api";
import MovieCard from "./MovieCard";

function Similar() {
  const [movieId, setMovieId] = useState(1);
  const [count, setCount] = useState(10);
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadSimilarMovies = async () => {
    if (movieId < 1 || movieId > 1682) {
      setError("Movie ID must be between 1 and 1682.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await api.similar(movieId, count);
      setMovies(data.similar_movies || []);
    } catch (err) {
      console.error(err);
      setError(err.message);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Similar Movies</h1>

      <div className="controls">
        <div>
          <label>Movie ID</label>
          <input
            type="number"
            min="1"
            max="1682"
            value={movieId}
            onChange={(e) => setMovieId(Number(e.target.value))}
          />
        </div>

        <div>
          <label>Number of Movies</label>
          <input
            type="number"
            min="1"
            max="50"
            value={count}
            onChange={(e) => setCount(Number(e.target.value))}
          />
        </div>

        <button onClick={loadSimilarMovies} disabled={loading}>
          {loading ? "Loading..." : "Find Similar Movies"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="movie-grid">
        {movies.map((movie) => (
          <MovieCard
            key={movie.movie_id}
            movie={movie}
          />
        ))}
      </div>

      {!loading && movies.length === 0 && !error && (
        <p>Enter a Movie ID and find similar movies.</p>
      )}
    </div>
  );
}

export default Similar;