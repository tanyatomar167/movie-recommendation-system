from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np

app = FastAPI(
    title="Movie Recommendation API",
    description="Movie Recommendation System API",
    version="1.0"
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
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

movies = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    header=None,
    usecols=[0, 1],
    names=["movie_id", "title"]
)


# --------------------------------------------------
# LOAD RATINGS
# --------------------------------------------------

ratings = pd.read_csv(
    "data/u.data",
    sep="\t",
    header=None,
    names=["user_id", "movie_id", "rating", "timestamp"]
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
        "users": int(ratings["user_id"].nunique()),
        "movies": int(movies["movie_id"].nunique()),
        "ratings": int(len(ratings))
    }


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

@app.get("/recommend/{user_id}")
def recommend_movies(user_id: int, n: int = 10):

    user_ratings = ratings[
        ratings["user_id"] == user_id
    ]

    rated_movies = set(
        user_ratings["movie_id"].tolist()
    )

    predictions = []

    for movie_id in movies["movie_id"]:

        if movie_id in rated_movies:
            continue

        try:
            prediction = svd_model.predict(
                user_id,
                movie_id
            )

            predicted_rating = prediction.est

            predictions.append({
                "movie_id": int(movie_id),
                "predicted_rating": round(
                    float(predicted_rating), 3
                )
            })

        except Exception:
            continue

    predictions = sorted(
        predictions,
        key=lambda x: x["predicted_rating"],
        reverse=True
    )[:n]

    result = []

    for item in predictions:

        movie = movies[
            movies["movie_id"] == item["movie_id"]
        ]

        if movie.empty:
            continue

        result.append({
            "movie_id": item["movie_id"],
            "title": movie.iloc[0]["title"],
            "predicted_rating": item["predicted_rating"]
        })

    return {
        "user_id": user_id,
        "recommendations": result
    }


# --------------------------------------------------
# SIMILAR MOVIES
# --------------------------------------------------
@app.get("/movies")
def get_movies(n: int = 100):
    movie_list = movies.head(n)

    return {
        "movies": [
            {
                "movie_id": int(row["movie_id"]),
                "title": row["title"]
            }
            for _, row in movie_list.iterrows()
        ]
    }
@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, n: int = 10):

    movie_ids = content_model["movie_ids"]
    similarity_matrix = content_model["similarity_matrix"]

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

        # Don't return the movie itself
        if similar_movie_id == movie_id:
            continue

        movie = movies[
            movies["movie_id"] == similar_movie_id
        ]

        if movie.empty:
            continue

        results.append({
            "movie_id": int(similar_movie_id),
            "title": movie.iloc[0]["title"],
            "similarity": round(
                float(similarities[idx]), 3
            )
        })

        if len(results) >= n:
            break

    return {
        "movie_id": movie_id,
        "similar_movies": results
    }