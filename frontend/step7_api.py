from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
from functools import lru_cache


app = FastAPI(
    title="Movie Recommendation API",
    description="Movie Recommendation System API",
    version="1.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://movie-recommendation-system-4p8t.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

with open("models/svd_model.pkl", "rb") as f:
    svd_model = pickle.load(f)

with open("models/content_model.pkl", "rb") as f:
    content_model = pickle.load(f)


# --------------------------------------------------
# LOAD MOVIE DATA
# --------------------------------------------------

# MovieLens u.item:
#
# 0  movie_id
# 1  movie_title
# 2  release_date
# 3  video_release_date
# 4  IMDb URL
# 5  unknown
# 6  Action
# 7  Adventure
# 8  Animation
# 9  Children's
# 10 Comedy
# 11 Crime
# 12 Documentary
# 13 Drama
# 14 Fantasy
# 15 Film-Noir
# 16 Horror
# 17 Musical
# 18 Mystery
# 19 Romance
# 20 Sci-Fi
# 21 Thriller
# 22 War
# 23 Western

GENRES = [
    "unknown",
    "Action",
    "Adventure",
    "Animation",
    "Children's",
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
    "Western",
]


movie_columns = [
    "movie_id",
    "title",
    "release_date",
    "video_release_date",
    "imdb_url",
] + GENRES


movies_full = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    header=None,
    names=movie_columns
)


# Keep only useful movie information
movies = movies_full[
    ["movie_id", "title"] + GENRES
].copy()


# --------------------------------------------------
# FAST MOVIE LOOKUP
# --------------------------------------------------

# movie_id -> movie information
movie_lookup = movies.set_index("movie_id").to_dict("index")


# --------------------------------------------------
# LOAD RATINGS
# --------------------------------------------------

ratings = pd.read_csv(
    "data/u.data",
    sep="\t",
    header=None,
    names=[
        "user_id",
        "movie_id",
        "rating",
        "timestamp"
    ]
)


# --------------------------------------------------
# USER RATING LOOKUP
# --------------------------------------------------

user_rated_movies = (
    ratings.groupby("user_id")["movie_id"]
    .apply(set)
    .to_dict()
)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running"
    }


# --------------------------------------------------
# STATS
# --------------------------------------------------

@app.get("/stats")
def get_stats():

    return {
        "users": int(
            ratings["user_id"].nunique()
        ),
        "movies": int(
            movies["movie_id"].nunique()
        ),
        "ratings": int(
            len(ratings)
        )
    }


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

@lru_cache(maxsize=100)
def generate_recommendations(
    user_id: int,
    n: int
):

    rated_movies = user_rated_movies.get(
        user_id,
        set()
    )

    predictions = []

    # Use numpy array instead of repeatedly
    # iterating over pandas rows
    movie_ids = movies["movie_id"].to_numpy()

    for movie_id in movie_ids:

        movie_id = int(movie_id)

        if movie_id in rated_movies:
            continue

        try:

            prediction = svd_model.predict(
                user_id,
                movie_id
            )

            predictions.append(
                (
                    movie_id,
                    float(prediction.est)
                )
            )

        except Exception:
            continue

    # Sort by predicted rating
    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    predictions = predictions[:n]

    result = []

    for movie_id, predicted_rating in predictions:

        movie = movie_lookup.get(movie_id)

        if movie is None:
            continue

        result.append({
            "movie_id": movie_id,
            "title": movie["title"],
            "predicted_rating": round(
                predicted_rating,
                3
            )
        })

    return result


@app.get("/recommend/{user_id}")
def recommend_movies(
    user_id: int,
    n: int = 10
):

    result = generate_recommendations(
        user_id,
        n
    )

    return {
        "user_id": user_id,
        "recommendations": result
    }


# --------------------------------------------------
# BROWSE MOVIES
# --------------------------------------------------

@app.get("/movies")
def get_movies(
    n: int = 100,
    genre: str | None = None
):

    filtered_movies = movies

    # Genre filter
    if genre:

        # Normalize input
        requested_genre = genre.strip().lower()

        matching_genres = [
            g for g in GENRES
            if g.lower() == requested_genre
        ]

        if matching_genres:

            selected_genre = matching_genres[0]

            filtered_movies = filtered_movies[
                filtered_movies[selected_genre] == 1
            ]

        else:

            # Unknown genre
            filtered_movies = filtered_movies.iloc[0:0]

    filtered_movies = filtered_movies.head(n)

    result = []

    for _, row in filtered_movies.iterrows():

        movie_genres = [
            genre_name
            for genre_name in GENRES
            if row[genre_name] == 1
        ]

        result.append({
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "genres": movie_genres
        })

    return {
        "movies": result,
        "count": len(result)
    }


# --------------------------------------------------
# SIMILAR MOVIES
# --------------------------------------------------

@app.get("/similar/{movie_id}")
def similar_movies(
    movie_id: int,
    n: int = 10
):

    movie_ids = content_model["movie_ids"]

    similarity_matrix = content_model[
        "similarity_matrix"
    ]

    if movie_id not in movie_ids:

        return {
            "movie_id": movie_id,
            "similar_movies": []
        }

    index = movie_ids.index(movie_id)

    similarities = similarity_matrix[index]

    similar_indices = np.argsort(
        similarities
    )[::-1]

    results = []

    for idx in similar_indices:

        similar_movie_id = movie_ids[idx]

        # Don't return itself
        if similar_movie_id == movie_id:
            continue

        movie = movie_lookup.get(
            similar_movie_id
        )

        if movie is None:
            continue

        results.append({
            "movie_id": int(
                similar_movie_id
            ),
            "title": movie["title"],
            "similarity": round(
                float(similarities[idx]),
                3
            )
        })

        if len(results) >= n:
            break

    return {
        "movie_id": movie_id,
        "similar_movies": results
    }