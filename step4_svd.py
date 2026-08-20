import pandas as pd
import joblib

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy


# ==========================================
# 1. Load ratings
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

print("\n========== SVD MATRIX FACTORIZATION ==========")

print("Total ratings:", len(ratings))


# ==========================================
# 2. Prepare data for Surprise
# ==========================================

reader = Reader(
    rating_scale=(1, 5)
)

dataset = Dataset.load_from_df(
    ratings[
        [
            "user_id",
            "movie_id",
            "rating"
        ]
    ],
    reader
)


# ==========================================
# 3. Train/Test split
# ==========================================

trainset, testset = train_test_split(
    dataset,
    test_size=0.20,
    random_state=42
)

print("Training ratings:", trainset.n_ratings)
print("Testing ratings:", len(testset))


# ==========================================
# 4. Train SVD model
# ==========================================

model = SVD(
    n_factors=100,
    n_epochs=20,
    lr_all=0.005,
    reg_all=0.02,
    random_state=42
)

print("\nTraining SVD model...")

model.fit(trainset)

print("SVD training completed!")


# ==========================================
# 5. Evaluate
# ==========================================

predictions = model.test(testset)

rmse = accuracy.rmse(
    predictions,
    verbose=True
)

mae = accuracy.mae(
    predictions,
    verbose=True
)


# ==========================================
# 6. Save model
# ==========================================

joblib.dump(
    model,
    "models/svd_model.pkl"
)

print(
    "\nSVD model saved to: models/svd_model.pkl"
)


# ==========================================
# 7. Generate recommendations
# ==========================================

movies = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    header=None,
    usecols=[0, 1],
    names=[
        "movie_id",
        "title"
    ]
)


def recommend_movies(
    user_id,
    n=10
):

    watched_movies = set(
        ratings[
            ratings["user_id"] == user_id
        ]["movie_id"]
    )

    all_movies = movies["movie_id"]

    predictions = []

    for movie_id in all_movies:

        if movie_id in watched_movies:
            continue

        prediction = model.predict(
            user_id,
            movie_id
        )

        predictions.append(
            (
                movie_id,
                prediction.est
            )
        )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_movies = predictions[:n]

    result = []

    for movie_id, predicted_rating in top_movies:

        title = movies[
            movies["movie_id"] == movie_id
        ]["title"].iloc[0]

        result.append(
            {
                "movie_id": movie_id,
                "title": title,
                "predicted_rating":
                    round(
                        predicted_rating,
                        3
                    )
            }
        )

    return pd.DataFrame(result)


# ==========================================
# 8. Test recommendation
# ==========================================

user_id = 1

recommendations = recommend_movies(
    user_id,
    n=10
)

print(
    f"\n========== RECOMMENDATIONS FOR USER {user_id} =========="
)

print(recommendations)


# ==========================================
# 9. Save recommendations
# ==========================================

recommendations.to_csv(
    "outputs/evaluation/svd_recommendations.csv",
    index=False
)

print(
    "\nRecommendations saved to:"
    " outputs/evaluation/svd_recommendations.csv"
)