import pandas as pd
import joblib

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
import numpy as np


# ==========================================
# 1. Load preprocessing data
# ==========================================

data = joblib.load("models/preprocessing.pkl")

ratings = data["ratings"]
user_item_matrix = data["user_item_matrix"]
train_data = data["train_data"]
test_data = data["test_data"]


# ==========================================
# 2. Fill missing values
# ==========================================

matrix_filled = user_item_matrix.fillna(0)


# ==========================================
# 3. USER-BASED COLLABORATIVE FILTERING
# ==========================================

print("\n========== USER-BASED COLLABORATIVE FILTERING ==========")

user_similarity = cosine_similarity(matrix_filled)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_item_matrix.index,
    columns=user_item_matrix.index
)

print("User similarity matrix shape:")
print(user_similarity_df.shape)


# ==========================================
# 4. Find similar users
# ==========================================

def find_similar_users(user_id, n=5):

    if user_id not in user_similarity_df.index:
        return []

    similarities = user_similarity_df[user_id].drop(
        user_id
    )

    similar_users = similarities.sort_values(
        ascending=False
    ).head(n)

    return similar_users


# ==========================================
# 5. USER-BASED RECOMMENDATIONS
# ==========================================

def user_based_recommendations(user_id, n=10):

    if user_id not in user_item_matrix.index:
        return pd.DataFrame()

    similar_users = find_similar_users(
        user_id,
        n=20
    )

    watched_movies = set(
        user_item_matrix.loc[user_id]
        .dropna()
        .index
    )

    recommendations = {}

    for similar_user, similarity in similar_users.items():

        user_ratings = user_item_matrix.loc[
            similar_user
        ].dropna()

        for movie_id, rating in user_ratings.items():

            if movie_id in watched_movies:
                continue

            if movie_id not in recommendations:
                recommendations[movie_id] = 0

            recommendations[movie_id] += (
                similarity * rating
            )

    recommended_movies = sorted(
        recommendations.items(),
        key=lambda x: x[1],
        reverse=True
    )[:n]

    return pd.DataFrame(
        recommended_movies,
        columns=["movie_id", "score"]
    )


# ==========================================
# 6. Test user-based recommendation
# ==========================================

user_id = 1

print(
    f"\nRecommendations for User {user_id}:"
)

user_recommendations = (
    user_based_recommendations(
        user_id,
        n=10
    )
)

print(user_recommendations)


# ==========================================
# 7. ITEM-BASED COLLABORATIVE FILTERING
# ==========================================

print(
    "\n========== ITEM-BASED COLLABORATIVE FILTERING =========="
)


# Transpose:
# users × movies
# becomes
# movies × users

item_matrix = matrix_filled.T

item_similarity = cosine_similarity(
    item_matrix
)

item_similarity_df = pd.DataFrame(
    item_similarity,
    index=item_matrix.index,
    columns=item_matrix.index
)

print("Item similarity matrix shape:")

print(item_similarity_df.shape)


# ==========================================
# 8. Find similar movies
# ==========================================

def find_similar_movies(movie_id, n=10):

    if movie_id not in item_similarity_df.index:
        return pd.DataFrame()

    similarities = item_similarity_df[
        movie_id
    ].drop(movie_id)

    similar_movies = similarities.sort_values(
        ascending=False
    ).head(n)

    return similar_movies.reset_index(
        name="similarity"
    ).rename(
        columns={
            "index": "movie_id"
        }
    )


# ==========================================
# 9. Test item similarity
# ==========================================

movie_id = 1

similar_movies = find_similar_movies(
    movie_id,
    n=10
)

print(
    f"\nMovies similar to Movie {movie_id}:"
)

print(similar_movies)


# ==========================================
# 10. Calculate RMSE
# ==========================================

print("\n========== SIMPLE EVALUATION ==========")

predictions = []

actuals = []

for _, row in test_data.iterrows():

    user_id = row["user_id"]
    movie_id = row["movie_id"]

    actual_rating = row["rating"]

    if user_id not in user_item_matrix.index:
        continue

    if movie_id not in user_item_matrix.columns:
        continue

    similar_users = find_similar_users(
        user_id,
        n=20
    )

    numerator = 0
    denominator = 0

    for similar_user, similarity in similar_users.items():

        rating = user_item_matrix.loc[
            similar_user,
            movie_id
        ]

        if pd.notna(rating):

            numerator += (
                similarity * rating
            )

            denominator += abs(
                similarity
            )

    if denominator == 0:
        continue

    predicted_rating = (
        numerator / denominator
    )

    predicted_rating = max(
        1,
        min(5, predicted_rating)
    )

    predictions.append(
        predicted_rating
    )

    actuals.append(
        actual_rating
    )


if len(predictions) > 0:

    rmse = np.sqrt(
        mean_squared_error(
            actuals,
            predictions
        )
    )

    print(
        f"User-based CF RMSE: {rmse:.4f}"
    )

else:

    print(
        "No predictions available."
    )


# ==========================================
# 11. Save collaborative filtering model
# ==========================================

joblib.dump(
    {
        "user_similarity": user_similarity_df,
        "item_similarity": item_similarity_df
    },
    "models/collaborative.pkl"
)

print(
    "\nCollaborative filtering completed!"
)

print(
    "Saved to: models/collaborative.pkl"
)