import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. Load movies
# ==========================================

movies = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    header=None
)

# MovieLens genre columns start at column 5
genre_columns = list(range(5, 24))

movies.columns = [
    "movie_id",
    "title",
    "release_date",
    "video_release_date",
    "IMDb_URL"
] + [
    f"genre_{i}"
    for i in range(19)
]


# ==========================================
# 2. Create genre text
# ==========================================

genre_names = [
    "unknown",
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"
]

movies["genres"] = ""

for i, genre in enumerate(genre_names):
    column = f"genre_{i}"

    movies.loc[
        movies[column] == 1,
        "genres"
    ] += genre + " "


# ==========================================
# 3. TF-IDF
# ==========================================

tfidf = TfidfVectorizer(
    lowercase=True
)

genre_matrix = tfidf.fit_transform(
    movies["genres"]
)

print("\n========== CONTENT-BASED FILTERING ==========")

print(
    "TF-IDF matrix shape:",
    genre_matrix.shape
)


# ==========================================
# 4. Movie similarity
# ==========================================

movie_similarity = cosine_similarity(
    genre_matrix
)

print(
    "Movie similarity matrix shape:",
    movie_similarity.shape
)


# ==========================================
# 5. Movie ID → matrix index
# ==========================================

movie_id_to_index = pd.Series(
    movies.index,
    index=movies["movie_id"]
)


# ==========================================
# 6. Similar movies function
# ==========================================

def similar_movies(movie_id, n=10):

    if movie_id not in movie_id_to_index:
        return pd.DataFrame()

    index = movie_id_to_index[movie_id]

    similarity_scores = list(
        enumerate(
            movie_similarity[index]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[
        1:n + 1
    ]

    result = []

    for index, score in similarity_scores:

        result.append(
            {
                "movie_id":
                    movies.iloc[index]["movie_id"],

                "title":
                    movies.iloc[index]["title"],

                "similarity":
                    round(score, 4)
            }
        )

    return pd.DataFrame(result)


# ==========================================
# 7. Test movie similarity
# ==========================================

movie_id = 1

print(
    f"\nMovies similar to Movie {movie_id}:"
)

print(
    similar_movies(
        movie_id,
        n=10
    )
)


# ==========================================
# 8. User profile
# ==========================================

ratings = pd.read_csv(
    "data/u.data",
    sep="\t",
    names=[
        "user_id",
        "movie_id",
        "rating",
        "timestamp"
    ]
)


def content_recommendations(
    user_id,
    n=10
):

    user_ratings = ratings[
        ratings["user_id"] == user_id
    ]

    liked_movies = user_ratings[
        user_ratings["rating"] >= 4
    ]

    if liked_movies.empty:
        return pd.DataFrame()

    profile = None

    for movie_id, rating in zip(
        liked_movies["movie_id"],
        liked_movies["rating"]
    ):

        if movie_id not in movie_id_to_index:
            continue

        index = movie_id_to_index[movie_id]

        vector = genre_matrix[index]

        weight = rating - 3

        if profile is None:
            profile = vector * weight
        else:
            profile = profile + vector * weight

    if profile is None:
        return pd.DataFrame()

    scores = cosine_similarity(
        profile,
        genre_matrix
    ).flatten()

    watched_movies = set(
        user_ratings["movie_id"]
    )

    recommendations = []

    for index, score in enumerate(scores):

        movie_id = movies.iloc[index]["movie_id"]

        if movie_id in watched_movies:
            continue

        recommendations.append(
            (
                movie_id,
                movies.iloc[index]["title"],
                score
            )
        )

    recommendations.sort(
        key=lambda x: x[2],
        reverse=True
    )

    return pd.DataFrame(
        recommendations[:n],
        columns=[
            "movie_id",
            "title",
            "score"
        ]
    )


# ==========================================
# 9. Test user recommendations
# ==========================================

user_id = 1

recommendations = content_recommendations(
    user_id,
    n=10
)

print(
    f"\n========== CONTENT RECOMMENDATIONS "
    f"FOR USER {user_id} =========="
)

print(recommendations)


# ==========================================
# 10. Save model
# ==========================================

joblib.dump(
    {
        "tfidf": tfidf,
        "genre_matrix": genre_matrix,
        "movie_similarity": movie_similarity,
        "movies": movies,
        "movie_id_to_index":
            movie_id_to_index
    },
    "models/content_model.pkl"
)

print(
    "\nContent-based model saved to:"
    " models/content_model.pkl"
)