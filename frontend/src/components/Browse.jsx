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

  useEffect(() => {
    async function loadMovies() {
      try {
        setLoading(true);

        const response = await fetch(
          `/api/movies?n=1682&genre=${encodeURIComponent(genre)}`
        );

        const data = await response.json();

        setMovies(data.movies || []);
      } catch (error) {
        console.error("Movies error:", error);
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, [genre]);

  const filteredMovies = movies.filter((movie) =>
    movie.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <section className="browse-page">

      <div className="page-heading">
        <p className="section-label">MOVIE CATALOG</p>

        <h2>Browse Movies</h2>

        <p>
          Explore movies from the MovieLens catalog.
        </p>
      </div>

      <div className="genre-list">
        {genres.map((item) => (
          <button
            key={item}
            className={genre === item ? "genre active" : "genre"}
            onClick={() => setGenre(item)}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="browse-controls">
        <input
          type="text"
          placeholder="Search movies..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="loading-message">
          Loading movies...
        </div>
      ) : (
        <>
          <p className="catalog-count">
            Showing {filteredMovies.length} movies
          </p>

          <div className="browse-grid">
            {filteredMovies.map((movie) => (
              <div className="browse-card" key={movie.movie_id}>

                <div className="browse-poster">
                  🎬
                </div>

                <span>
                  MOVIE #{movie.movie_id}
                </span>

                <h3>{movie.title}</h3>

                <div className="movie-genres">
                  {movie.genres?.map((g) => (
                    <span key={g}>{g}</span>
                  ))}
                </div>

              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
}

export default Browse;