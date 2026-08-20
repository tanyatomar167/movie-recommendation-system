import pandas as pd
import joblib
from sklearn.model_selection import train_test_split


# ==========================================
# 1. File path
# ==========================================

RATINGS_PATH = "data/u.data"


# ==========================================
# 2. Load ratings
# ==========================================

ratings = pd.read_csv(
    RATINGS_PATH,
    sep="\t",
    names=[
        "user_id",
        "movie_id",
        "rating",
        "timestamp"
    ]
)

print("\n========== ORIGINAL DATA ==========")
print(ratings.head())

print("\nTotal ratings:", len(ratings))


# ==========================================
# 3. Create user-item matrix
# ==========================================

user_item_matrix = ratings.pivot_table(
    index="user_id",
    columns="movie_id",
    values="rating"
)

print("\n========== USER-ITEM MATRIX ==========")

print(user_item_matrix.head())

print("\nMatrix shape:")
print(user_item_matrix.shape)


# ==========================================
# 4. Calculate sparsity
# ==========================================

total_possible = (
    user_item_matrix.shape[0]
    * user_item_matrix.shape[1]
)

actual_ratings = user_item_matrix.count().sum()

sparsity = 1 - (
    actual_ratings / total_possible
)

print("\n========== SPARSITY ==========")

print(
    f"Matrix sparsity: {sparsity * 100:.2f}%"
)


# ==========================================
# 5. Train/Test split
# ==========================================

train_data, test_data = train_test_split(
    ratings,
    test_size=0.20,
    random_state=42
)

print("\n========== TRAIN / TEST ==========")

print(
    "Training ratings:",
    len(train_data)
)

print(
    "Testing ratings:",
    len(test_data)
)


# ==========================================
# 6. Save preprocessing results
# ==========================================

joblib.dump(
    {
        "ratings": ratings,
        "user_item_matrix": user_item_matrix,
        "train_data": train_data,
        "test_data": test_data
    },
    "models/preprocessing.pkl"
)

print("\nPreprocessing completed successfully!")

print(
    "Saved to: models/preprocessing.pkl"
)