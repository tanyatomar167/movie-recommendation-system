function MovieCard({ movie, type }) {
  const score =
    type === "similar"
      ? movie.similarity
      : movie.predicted_rating;

  const label =
    type === "similar"
      ? "Similarity"
      : "Predicted Rating";

  return (
    <div className="movie-card">
      <div className="movie-poster">
        🎬
      </div>

      <div className="movie-info">
        <div className="movie-id">
          MOVIE #{movie.movie_id}
        </div>

        <h3>{movie.title}</h3>

        <div className="movie-rating">
          <span className="star">★</span>

          <strong>
            {Number(score).toFixed(3)}
          </strong>

          <span>{label}</span>
        </div>
      </div>
    </div>
  );
}

export default MovieCard;