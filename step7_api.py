from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from functools import lru_cache


# ==========================================================
# GENRES
# ==========================================================

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
    "Western"
]


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI(
    title="Movie Recommendation API",
    description="Movie Recommendation System using SVD and Content-Based Filtering",
    version="1.0.0"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://movie-recommendation-system-1-igis.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# LOAD MODELS
# ==========================================================

svd_model = joblib.load(
    "models/svd_model.pkl"
)

content_data = joblib.load(
    "models/content_model.pkl"
)


# ==========================================================
# LOAD MOVIE DATA
# ==========================================================

movies = content_data["movies"].copy()

movie_id_to_index = content_data[
    "movie_id_to_index"
]

genre_matrix = content_data[
    "genre_matrix"
]


# ==========================================================
# IMPORTANT:
# LOAD ACTUAL GENRE DATA FROM u.item
# ==========================================================

movie_columns = [
    "movie_id",
    "title",
    "release_date",
    "video_release_date",
    "imdb_url"
] + GENRES


movie_data = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    header=None,
    names=movie_columns
)


# Only keep required columns
movie_data = movie_data[
    ["movie_id", "title"] + GENRES
].copy()


# ==========================================================
# FAST MOVIE LOOKUP
# ==========================================================

movie_lookup = (
    movie_data
    .set_index("movie_id")
    .to_dict("index")
)


# ==========================================================
# LOAD RATINGS
# ==========================================================

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


# ==========================================================
# FAST USER → WATCHED MOVIES LOOKUP
# ==========================================================

user_watched = (
    ratings
    .groupby("user_id")["movie_id"]
    .apply(set)
    .to_dict()
)


# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "Movie Recommendation API is running!",
        "docs": "/docs"
    }


# ==========================================================
# STATS
# ==========================================================

@app.get("/stats")
def stats():

    return {
        "users": int(
            ratings["user_id"].nunique()
        ),

        "movies": int(
            movie_data["movie_id"].nunique()
        ),

        "ratings": int(
            len(ratings)
        )
    }


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

@lru_cache(maxsize=100)
def generate_recommendations(
    user_id: int,
    n: int
):

    watched_movies = user_watched.get(
        user_id,
        set()
    )

    predictions = []

    # Only MovieLens movie IDs
    movie_ids = movie_data[
        "movie_id"
    ].tolist()

    for movie_id in movie_ids:

        movie_id = int(movie_id)

        if movie_id in watched_movies:
            continue

        try:

            prediction = svd_model.predict(
                user_id,
                movie_id
            )

            predictions.append({
                "movie_id": movie_id,
                "predicted_rating": float(
                    prediction.est
                )
            })

        except Exception:
            continue

    predictions.sort(
        key=lambda x: x["predicted_rating"],
        reverse=True
    )

    results = []

    for item in predictions[:n]:

        movie = movie_lookup.get(
            item["movie_id"]
        )

        if movie is None:
            continue

        results.append({
            "movie_id": item["movie_id"],
            "title": movie["title"],
            "predicted_rating": round(
                item["predicted_rating"],
                3
            )
        })

    return results


@app.get("/recommend/{user_id}")
def recommend(
    user_id: int,
    n: int = 10
):

    if user_id not in user_watched:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "recommendations":
            generate_recommendations(
                user_id,
                n
            )
    }


# ==========================================================
# MOVIE CATALOG
# ==========================================================

@app.get("/movies")
def get_movies(
    n: int = 1682,
    genre: str = "All"
):

    # ------------------------------------------------------
    # ALL MOVIES
    # ------------------------------------------------------

    if genre.lower() == "all":

        filtered_movies = movie_data.head(n)

    else:

        requested_genre = genre.strip().lower()

        # Find correct MovieLens genre name
        selected_genre = None

        for g in GENRES:

            if g.lower() == requested_genre:

                selected_genre = g
                break

        # Invalid genre
        if selected_genre is None:

            return {
                "movies": [],
                "count": 0
            }

        # --------------------------------------------------
        # FILTER USING ACTUAL u.item GENRE COLUMN
        # --------------------------------------------------

        filtered_movies = movie_data[
            movie_data[selected_genre] == 1
        ].head(n)

    # ------------------------------------------------------
    # BUILD RESPONSE
    # ------------------------------------------------------

    results = []

    for _, row in filtered_movies.iterrows():

        movie_genres = []

        for g in GENRES:

            # Don't show "unknown" in frontend
            if g == "unknown":
                continue

            if row[g] == 1:

                movie_genres.append(g)

        results.append({
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "genres": movie_genres
        })

    return {
        "movies": results,
        "count": len(results)
    }


# ==========================================================
# SIMILAR MOVIES
# ==========================================================

@app.get("/similar/{movie_id}")
def similar_movies(
    movie_id: int,
    n: int = 10
):

    if movie_id not in movie_id_to_index:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    index = movie_id_to_index[
        movie_id
    ]

    similarity_scores = (
        genre_matrix @
        genre_matrix[index].T
    ).toarray().flatten()

    similar_indices = (
        similarity_scores
        .argsort()[::-1]
    )

    results = []

    for idx in similar_indices:

        current_movie_id = int(
            movie_data.iloc[idx]["movie_id"]
        )

        if current_movie_id == movie_id:
            continue

        movie = movie_lookup.get(
            current_movie_id
        )

        if movie is None:
            continue

        results.append({
            "movie_id": current_movie_id,
            "title": movie["title"],
            "similarity": round(
                float(
                    similarity_scores[idx]
                ),
                4
            )
        })

        if len(results) >= n:
            break

    return {
        "movie_id": movie_id,
        "similar_movies": results
    }


# ==========================================================
# HYBRID RECOMMENDATIONS
# ==========================================================

@lru_cache(maxsize=100)
def generate_hybrid_recommendations(
    user_id: int,
    n: int
):

    watched_movies = user_watched.get(
        user_id,
        set()
    )

    results = []

    # ------------------------------------------------------
    # SVD PREDICTIONS
    # ------------------------------------------------------

    for movie_id in movie_data[
        "movie_id"
    ].tolist():

        movie_id = int(movie_id)

        if movie_id in watched_movies:
            continue

        try:

            prediction = svd_model.predict(
                user_id,
                movie_id
            )

            results.append({
                "movie_id": movie_id,
                "title": movie_lookup[
                    movie_id
                ]["title"],
                "svd_score": float(
                    prediction.est
                )
            })

        except Exception:
            continue

    if not results:
        return []

    # ------------------------------------------------------
    # NORMALIZE SVD
    # ------------------------------------------------------

    svd_scores = [
        item["svd_score"]
        for item in results
    ]

    max_svd = max(svd_scores)
    min_svd = min(svd_scores)

    for item in results:

        if max_svd == min_svd:

            item["svd_normalized"] = 1.0

        else:

            item["svd_normalized"] = (
                (
                    item["svd_score"]
                    - min_svd
                )
                /
                (
                    max_svd
                    - min_svd
                )
            )

    # ------------------------------------------------------
    # CONTENT SCORE
    # ------------------------------------------------------

    for item in results:

        movie_id = item["movie_id"]

        index = movie_id_to_index.get(
            movie_id
        )

        if index is not None:

            # Number of genres
            content_score = float(
                genre_matrix[index].sum()
            )

            item["content_score"] = (
                content_score
            )

        else:

            item["content_score"] = 0.0

    # ------------------------------------------------------
    # NORMALIZE CONTENT
    # ------------------------------------------------------

    content_scores = [
        item["content_score"]
        for item in results
    ]

    max_content = max(content_scores)
    min_content = min(content_scores)

    for item in results:

        if max_content == min_content:

            content_normalized = 1.0

        else:

            content_normalized = (
                (
                    item["content_score"]
                    - min_content
                )
                /
                (
                    max_content
                    - min_content
                )
            )

        # 70% collaborative
        # 30% content

        item["hybrid_score"] = round(
            (
                0.7 *
                item["svd_normalized"]
            )
            +
            (
                0.3 *
                content_normalized
            ),
            4
        )

    # ------------------------------------------------------
    # SORT
    # ------------------------------------------------------

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    # ------------------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------------------

    recommendations = []

    for item in results[:n]:

        recommendations.append({
            "movie_id": item["movie_id"],
            "title": item["title"],
            "predicted_rating": round(
                item["svd_score"],
                3
            ),
            "hybrid_score": item[
                "hybrid_score"
            ]
        })

    return recommendations


@app.get("/hybrid/{user_id}")
def hybrid_recommend(
    user_id: int,
    n: int = 10
):

    if user_id not in user_watched:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "recommendations":
            generate_hybrid_recommendations(
                user_id,
                n
            )
    }