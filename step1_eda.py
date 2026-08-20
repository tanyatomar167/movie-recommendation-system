import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. File paths
# ==========================================

RATINGS_PATH = "data/u.data"
MOVIES_PATH = "data/u.item"


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


# ==========================================
# 3. Load movies
# ==========================================

movies = pd.read_csv(
    MOVIES_PATH,
    sep="|",
    encoding="latin-1",
    header=None,
    names=[
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "IMDb_URL",
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
)


# ==========================================
# 4. Display first rows
# ==========================================

print("\n========== RATINGS ==========")

print(ratings.head())


print("\n========== MOVIES ==========")

print(movies[["movie_id", "title"]].head())


# ==========================================
# 5. Dataset information
# ==========================================

print("\n========== DATASET INFORMATION ==========")

print("Number of users:", ratings["user_id"].nunique())

print(
    "Number of movies:",
    ratings["movie_id"].nunique()
)

print(
    "Number of ratings:",
    len(ratings)
)


# ==========================================
# 6. Rating statistics
# ==========================================

print("\n========== RATING STATISTICS ==========")

print(
    ratings["rating"].describe()
)


# ==========================================
# 7. Rating distribution
# ==========================================

print("\n========== RATING DISTRIBUTION ==========")

print(
    ratings["rating"]
    .value_counts()
    .sort_index()
)


# ==========================================
# 8. Calculate sparsity
# ==========================================

num_users = ratings["user_id"].nunique()
num_movies = ratings["movie_id"].nunique()

total_possible_ratings = num_users * num_movies

actual_ratings = len(ratings)

sparsity = (
    1
    - actual_ratings / total_possible_ratings
)

print("\n========== SPARSITY ==========")

print(
    f"Sparsity: {sparsity * 100:.2f}%"
)


# ==========================================
# 9. Create rating distribution chart
# ==========================================

plt.figure(figsize=(8, 5))

ratings["rating"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("MovieLens Rating Distribution")

plt.xlabel("Rating")

plt.ylabel("Number of Ratings")

plt.tight_layout()

plt.savefig(
    "outputs/eda/rating_distribution.png"
)

#plt.show()


print("\nEDA completed successfully!")

print(
    "Chart saved to: "
    "outputs/eda/rating_distribution.png"
)