import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import precision_score


# ==========================================
# 1. Load models
# ==========================================

svd_model = joblib.load(
    "models/svd_model.pkl"
)

content_data = joblib.load(
    "models/content_model.pkl"
)

tfidf = content_data["tfidf"]
genre_matrix = content_data["genre_matrix"]
movies = content_data["movies"]
movie_id_to_index = content_data["movie_id_to_index"]


# ==========================================
# 2. Load ratings
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


# ==========================================
# 3. Content recommendation function
# ==========================================

def get_content_scores(user_id):

    user_ratings = ratings[
        ratings["user_id"] == user_id
    ]

    liked_movies = user_ratings[
        user_ratings["rating"] >= 4
    ]

    scores = {}

    if liked_movies.empty:
        return scores

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
        return scores

    similarity_scores = (
        profile @ genre_matrix.T
    ).toarray().flatten()

    watched_movies = set(
        user_ratings["movie_id"]
    )

    for index, score in enumerate(
        similarity_scores
    ):

        movie_id = int(
            movies.iloc[index]["movie_id"]
        )

        if movie_id in watched_movies:
            continue

        scores[movie_id] = float(score)

    return scores


# ==========================================
# 4. Hybrid recommendations
# ==========================================

def hybrid_recommendations(
    user_id,
    n=10,
    cf_weight=0.7,
    content_weight=0.3
):

    user_ratings = ratings[
        ratings["user_id"] == user_id
    ]

    watched_movies = set(
        user_ratings["movie_id"]
    )

    content_scores = get_content_scores(
        user_id
    )

    candidates = []

    # Generate candidates from all movies
    for movie_id in movies["movie_id"]:

        movie_id = int(movie_id)

        if movie_id in watched_movies:
            continue

        # SVD prediction
        svd_prediction = svd_model.predict(
            user_id,
            movie_id
        ).est

        # Content score
        content_score = content_scores.get(
            movie_id,
            0
        )

        candidates.append(
            {
                "movie_id": movie_id,
                "svd_score": svd_prediction,
                "content_score": content_score
            }
        )

    result = pd.DataFrame(candidates)


    # ======================================
    # Normalize SVD score
    # ======================================

    svd_min = result["svd_score"].min()
    svd_max = result["svd_score"].max()

    result["svd_normalized"] = (
        result["svd_score"] - svd_min
    ) / (
        svd_max - svd_min + 1e-8
    )


    # ======================================
    # Normalize content score
    # ======================================

    content_min = result["content_score"].min()
    content_max = result["content_score"].max()

    result["content_normalized"] = (
        result["content_score"] - content_min
    ) / (
        content_max - content_min + 1e-8
    )


    # ======================================
    # Hybrid score
    # ======================================

    result["hybrid_score"] = (
        cf_weight
        * result["svd_normalized"]
        +
        content_weight
        * result["content_normalized"]
    )


    # ======================================
    # Sort
    # ======================================

    result = result.sort_values(
        "hybrid_score",
        ascending=False
    )


    # ======================================
    # Add movie titles
    # ======================================

    result = result.merge(
        movies[
            [
                "movie_id",
                "title"
            ]
        ],
        on="movie_id",
        how="left"
    )


    # ======================================
    # Return top N
    # ======================================

    return result[
        [
            "movie_id",
            "title",
            "svd_score",
            "content_score",
            "hybrid_score"
        ]
    ].head(n)


# ==========================================
# 5. Test hybrid system
# ==========================================

user_id = 1

print(
    "\n========== HYBRID RECOMMENDATIONS =========="
)

recommendations = hybrid_recommendations(
    user_id=user_id,
    n=10,
    cf_weight=0.7,
    content_weight=0.3
)

print(recommendations)


# ==========================================
# 6. Save recommendations
# ==========================================

recommendations.to_csv(
    "outputs/evaluation/"
    "hybrid_recommendations.csv",
    index=False
)

print(
    "\nHybrid recommendations saved to:"
    " outputs/evaluation/"
    "hybrid_recommendations.csv"
)