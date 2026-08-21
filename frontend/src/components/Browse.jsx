import { useEffect, useState } from "react";

const genres = [
  "All",
  "Action",
  "Adventure",
  "Animation",
  "Comedy",
  "Crime",
  "Drama",
  "Horror",
  "Romance",
  "Sci-Fi",
  "Thriller",
];

function Browse() {
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState("");
  const [genre, setGenre] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMovies() {
      try {
        setLoading(true);
        setError("");

        const url =
          genre === "All"
            ? "/api/movies?n=1682"
            : `/api/movies?n=1682&genre=${encodeURIComponent(
                genre
              )}`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(
            `Failed to fetch movies: ${response.status}`
          );
        }

        const data = await response.json();

        setMovies(data.movies || []);
      } catch (error) {
        console.error("Movies error:", error);
        setMovies([]);
        setError("Unable to load movies.");
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, [genre]);

  const filteredMovies = movies.filter((movie) =>
    movie.title
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <section className="browse-page">

      <div className="page-heading">
        <p className="section-label">
          MOVIE CATALOG
        </p>

        <h2>Browse Movies</h2>

        <p>
          Explore movies from the MovieLens catalog.
        </p>
      </div>

      {/* GENRES */}

      <div className="genre-list">
        {genres.map((item) => (
          <button
            key={item}
            className={
              genre === item
                ? "genre active"
                : "genre"
            }
            onClick={() => setGenre(item)}
          >
            {item}
          </button>
        ))}
      </div>

      {/* SEARCH */}

      <div className="browse-controls">
        <input
          type="text"
          placeholder="Search movies..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />
      </div>

      {/* CONTENT */}

      {loading ? (
        <div className="loading-message">
          Loading movies...
        </div>
      ) : error ? (
        <div className="error-message">
          {error}
        </div>
      ) : (
        <>
          <p className="catalog-count">
            Showing {filteredMovies.length} movies
          </p>

          <div className="browse-grid">

            {filteredMovies.length === 0 ? (
              <div className="empty-message">
                No movies found.
              </div>
            ) : (
              filteredMovies.map((movie) => (
                <div
                  className="browse-card"
                  key={movie.movie_id}
                >

                  <div className="browse-poster">
                    🎬
                  </div>

                  <span>
                    MOVIE #{movie.movie_id}
                  </span>

                  <h3>{movie.title}</h3>

                  <div className="movie-genres">
                    {movie.genres?.map((g) => (
                      <span key={g}>
                        {g}
                      </span>
                    ))}
                  </div>

                </div>
              ))
            )}

          </div>
        </>
      )}
    </section>
  );
}

export default Browse;