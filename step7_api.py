from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib


# --------------------------------------------------
# GENRES
# --------------------------------------------------

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


# --------------------------------------------------
# CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Movie Recommendation API",
    description="Movie Recommendation System using SVD and Content-Based Filtering",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LOAD TRAINED MODELS
# --------------------------------------------------

# Load SVD model
svd_model = joblib.load("models/svd_model.pkl")

# Load content-based model
content_data = joblib.load("models/content_model.pkl")

movies = content_data["movies"]
movie_id_to_index = content_data["movie_id_to_index"]
genre_matrix = content_data["genre_matrix"]


# --------------------------------------------------
# LOAD MOVIELENS RATINGS
# --------------------------------------------------

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


# --------------------------------------------------
# HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running!",
        "docs": "/docs"
    }


# --------------------------------------------------
# STATISTICS ENDPOINT
# --------------------------------------------------

@app.get("/stats")
def stats():

    return {
        "users": int(ratings["user_id"].nunique()),
        "movies": int(ratings["movie_id"].nunique()),
        "ratings": int(len(ratings))
    }


# --------------------------------------------------
# PERSONALIZED RECOMMENDATIONS
# --------------------------------------------------

@app.get("/recommend/{user_id}")
def recommend(user_id: int, n: int = 10):

    # Check whether user exists
    if user_id not in ratings["user_id"].values:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Movies already watched/rated by the user
    watched_movies = set(
        ratings[
            ratings["user_id"] == user_id
        ]["movie_id"]
    )

    recommendations = []

    # Predict rating for every movie
    for movie_id in movies["movie_id"]:

        movie_id = int(movie_id)

        # Don't recommend movies already watched
        if movie_id in watched_movies:
            continue

        prediction = svd_model.predict(
            user_id,
            movie_id
        )

        movie_title = movies[
            movies["movie_id"] == movie_id
        ]["title"].iloc[0]

        recommendations.append({
            "movie_id": movie_id,
            "title": movie_title,
            "predicted_rating": round(
                prediction.est,
                3
            )
        })

    # Sort by predicted rating
    recommendations.sort(
        key=lambda x: x["predicted_rating"],
        reverse=True
    )

    # Return top N recommendations
    return {
        "user_id": user_id,
        "recommendations": recommendations[:n]
    }


# --------------------------------------------------
# SIMILAR MOVIES
# --------------------------------------------------

@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, n: int = 10):

    # Check whether movie exists
    if movie_id not in movie_id_to_index:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Get index of selected movie
    index = movie_id_to_index[movie_id]

    # Calculate similarity
    similarity_scores = (
        genre_matrix @ genre_matrix[index].T
    ).toarray().flatten()

    # Sort movies by similarity
    similar_indices = similarity_scores.argsort()[::-1]

    results = []

    for idx in similar_indices:

        current_movie_id = int(
            movies.iloc[idx]["movie_id"]
        )

        # Don't return the same movie
        if current_movie_id == movie_id:
            continue

        results.append({
            "movie_id": current_movie_id,
            "title": movies.iloc[idx]["title"],
            "similarity": round(
                float(similarity_scores[idx]),
                4
            )
        })

        if len(results) >= n:
            break

    return {
        "movie_id": movie_id,
        "similar_movies": results
    }


# --------------------------------------------------
# MOVIE CATALOG
# --------------------------------------------------

@app.get("/movies")
def get_movies(
    n: int = 1682,
    genre: str = "All"
):

    movie_list = movies.head(n)

    results = []

    for idx, row in movie_list.iterrows():

        movie_genres = []

        if idx < genre_matrix.shape[0]:

            genre_values = (
                genre_matrix[idx]
                .toarray()
                .flatten()
            )

            for i, value in enumerate(genre_values):

                if value > 0 and i < len(GENRES):
                    movie_genres.append(
                        GENRES[i]
                    )

        if genre != "All" and genre not in movie_genres:
            continue

        results.append({
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "genres": movie_genres
        })

    return {
        "movies": results
    }


# --------------------------------------------------
# HYBRID RECOMMENDATIONS
# --------------------------------------------------

@app.get("/hybrid/{user_id}")
def hybrid_recommend(
    user_id: int,
    n: int = 10
):

    if user_id not in ratings["user_id"].values:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    watched_movies = set(
        ratings[
            ratings["user_id"] == user_id
        ]["movie_id"]
    )

    results = []

    # Get SVD predictions
    for movie_id in movies["movie_id"]:

        movie_id = int(movie_id)

        if movie_id in watched_movies:
            continue

        prediction = svd_model.predict(
            user_id,
            movie_id
        )

        results.append({
            "movie_id": movie_id,
            "title": movies[
                movies["movie_id"] == movie_id
            ]["title"].iloc[0],
            "svd_score": float(
                prediction.est
            )
        })

    if not results:
        return {
            "user_id": user_id,
            "recommendations": []
        }

    # Normalize SVD scores
    max_score = max(
        x["svd_score"]
        for x in results
    )

    min_score = min(
        x["svd_score"]
        for x in results
    )

    for item in results:

        if max_score == min_score:

            item["svd_normalized"] = 1.0

        else:

            item["svd_normalized"] = (
                (item["svd_score"] - min_score)
                / (max_score - min_score)
            )

        # Content score based on genre matrix
        movie_id = item["movie_id"]

        if movie_id in movie_id_to_index:

            index = movie_id_to_index[movie_id]

            content_score = float(
                genre_matrix[index].sum()
            )

            item["content_score"] = content_score

        else:

            item["content_score"] = 0.0

    max_content = max(
        x["content_score"]
        for x in results
    )

    min_content = min(
        x["content_score"]
        for x in results
    )

    for item in results:

        if max_content == min_content:

            content_normalized = 1.0

        else:

            content_normalized = (
                (item["content_score"] - min_content)
                / (max_content - min_content)
            )

        item["hybrid_score"] = round(
            0.7 * item["svd_normalized"]
            + 0.3 * content_normalized,
            4
        )

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    recommendations = []

    for item in results[:n]:

        recommendations.append({
            "movie_id": item["movie_id"],
            "title": item["title"],
            "predicted_rating": round(
                item["svd_score"],
                3
            ),
            "hybrid_score": item["hybrid_score"]
        })

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }