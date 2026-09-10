# 🎬 CineRec — Movie Recommendation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**A full-stack hybrid movie recommendation engine trained on MovieLens 100K.**  
Combines SVD matrix factorisation, collaborative filtering, and TF-IDF content-based filtering — served through a FastAPI backend and a React dashboard.

[**Live Demo →**](https://cinerec-frontend.onrender.com) &nbsp;·&nbsp;
[**API Docs →**](https://cinrec-api.onrender.com/docs) &nbsp;·&nbsp;
[**Report a Bug**](https://github.com/YOUR_USERNAME/movie-recommendation-system/issues)

</div>

---

## 📸 Screenshots

| Dashboard | Recommendations | Similar Movies |
|-----------|----------------|----------------|
| ![dash](docs/dashboard.png) | ![recs](docs/recs.png) | ![sim](docs/similar.png) |

> _Replace the placeholder images above with screenshots of your running app._

---

## ✨ Features

- **Hybrid recommendations** — blends SVD (collaborative) + TF-IDF (content-based) with an adjustable weight slider
- **Interactive dashboard** — live charts for rating distribution, model comparison, genre coverage, and matrix sparsity
- **User history** — see exactly what each user has rated alongside their personalised picks
- **Similar movies** — content-based similarity search by movie ID
- **Genre catalog** — browse and filter all 1,682 movies by genre
- **REST API** — full FastAPI backend with auto-generated Swagger docs at `/docs`

---

## 🧠 How It Works

```
MovieLens 100K Data
        │
        ▼
┌───────────────────┐
│  Preprocessing    │  pivot table → user-item matrix (96% sparse)
│  (step2)          │  mean-centering, train/test 80/20 split
└────────┬──────────┘
         │
    ┌────┴──────────────────────────────┐
    │                                   │
    ▼                                   ▼
┌──────────────┐               ┌──────────────────┐
│ Collaborative│               │  Content-Based   │
│  Filtering   │               │   Filtering      │
│  (step3)     │               │   (step5)        │
│              │               │                  │
│ • User-based │               │ • TF-IDF on      │
│   cosine sim │               │   genre strings  │
│ • Item-based │               │ • Cosine sim     │
│   cosine sim │               │   on genre vecs  │
└──────┬───────┘               └────────┬─────────┘
       │                                │
       ▼                                │
┌──────────────┐                        │
│     SVD      │                        │
│ (step4)      │                        │
│              │                        │
│ n_factors=50 │                        │
│ RMSE = 0.79  │                        │
└──────┬───────┘                        │
       │                                │
       └──────────────┬─────────────────┘
                      ▼
              ┌───────────────┐
              │  Hybrid Model │  70% SVD + 30% Content
              │  (step6)      │  Best RMSE + Recall
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │  FastAPI REST │  /recommend, /similar,
              │  (step7)      │  /user/history, /movies
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ React Frontend│  Dashboard, Charts,
              │  (frontend/)  │  Interactive UI
              └───────────────┘
```

### Algorithm details

| Algorithm | Approach | RMSE | MAE |
|-----------|----------|------|-----|
| User-based CF | Cosine similarity on user rating vectors | 0.98 | 0.77 |
| Item-based CF | Cosine similarity on item rating vectors | 1.02 | 0.81 |
| **SVD** | Matrix factorisation, 50 latent factors | **0.79** | **0.61** |
| **Hybrid** | 70% SVD + 30% TF-IDF content | **0.76** | **0.58** |

---

## 🗂️ Project Structure

```
movie-recommendation-system/
│
├── data/                        # MovieLens 100K dataset
│   ├── u.data                   # 100,000 ratings (user, movie, rating, timestamp)
│   └── u.item                   # 1,682 movies with genre flags
│
├── models/                      # Serialised trained models (gitignored)
│   ├── preprocessing.pkl        # user-item matrix, train/test splits
│   ├── collaborative.pkl        # user & item similarity matrices
│   ├── svd_model.pkl            # trained SVD model
│   └── content_model.pkl        # TF-IDF vectoriser + genre matrix
│
├── outputs/                     # Generated charts and CSVs (gitignored)
│   ├── eda/
│   └── evaluation/
│
├── step1_eda.py                 # Exploratory data analysis + charts
├── step2_preprocessing.py       # Build user-item matrix, train/test split
├── step3_collaborative.py       # User-based & item-based CF + evaluation
├── step4_svd.py                 # SVD matrix factorisation + GridSearch tuning
├── step5_content.py             # TF-IDF content-based filtering
├── step6_hybrid_eval.py         # Hybrid model + full Precision@K / Recall@K eval
├── step7_api.py                 # FastAPI REST API (5 endpoints)
│
├── frontend/                    # React 18 dashboard
│   ├── public/index.html
│   ├── src/
│   │   ├── api.js               # All fetch calls in one place
│   │   ├── App.jsx              # Shell + routing
│   │   ├── App.css              # Full design system (dark theme)
│   │   └── components/
│   │       ├── Sidebar.jsx      # Navigation + live API stats
│   │       ├── Dashboard.jsx    # Charts, stats, quick-recommend
│   │       ├── Recommend.jsx    # Full hybrid recs + history tabs
│   │       ├── Similar.jsx      # Content-based similar movies
│   │       ├── Browse.jsx       # Genre-filtered catalog
│   │       └── MovieCard.jsx    # Reusable movie row component
│   └── package.json
│
├── requirements.txt             # Python dependencies for Render
├── render.yaml                  # Render Blueprint (deploy both services)
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.9+ and `pip`
- Node.js 18+ and `npm`
- MovieLens 100K dataset → [download here](https://grouplens.org/datasets/movielens/100k/)

### 1. Clone & set up Python

```bash
git clone https://github.com/YOUR_USERNAME/movie-recommendation-system.git
cd movie-recommendation-system

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Prepare the dataset

```bash
mkdir -p data outputs/eda outputs/evaluation models
# Place u.data and u.item inside data/
```

### 3. Train the models (run in order)

```bash
python step1_eda.py            # EDA charts → outputs/eda/
python step2_preprocessing.py  # Builds user-item matrix → models/preprocessing.pkl
python step3_collaborative.py  # CF models  → models/collaborative.pkl
python step4_svd.py            # SVD model  → models/svd_model.pkl
python step5_content.py        # TF-IDF     → models/content_model.pkl
python step6_hybrid_eval.py    # Evaluation → outputs/evaluation/
```

### 4. Start the API

```bash
uvicorn step7_api:app --reload --port 8000
# API live at http://127.0.0.1:8000
# Swagger docs at http://127.0.0.1:8000/docs
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm start
# App live at http://localhost:5174  (or :3000 with CRA)
```

---

## 🌐 API Reference

Base URL (local): `http://127.0.0.1:8000`  
Base URL (production): `https://cinrec-api.onrender.com`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info and available endpoints |
| `GET` | `/stats` | Dataset stats + model metrics |
| `GET` | `/recommend/{user_id}` | Top-N hybrid recommendations |
| `GET` | `/similar/{movie_id}` | Content-similar movies |
| `GET` | `/user/{user_id}/history` | User's rating history |
| `GET` | `/movies` | Browse catalog with genre filter |

### Example requests

```bash
# Get top 10 recommendations for user 42
curl "http://127.0.0.1:8000/recommend/42?n=10&cf_weight=0.7"

# Find movies similar to movie 1
curl "http://127.0.0.1:8000/similar/1?n=5"

# Browse Action movies
curl "http://127.0.0.1:8000/movies?genre=Action&limit=20"

# User 1's rating history
curl "http://127.0.0.1:8000/user/1/history?limit=20"
```

### Example response — `/recommend/42`

```json
{
  "user_id": 42,
  "n_recommendations": 10,
  "cf_weight": 0.7,
  "recommendations": [
    {
      "item_id": 318,
      "title": "Schindler's List (1993)",
      "genres": "Drama|War",
      "score": 0.9571,
      "svd_score": 1.0,
      "cb_score": 0.8574
    }
  ]
}
```

---

## ☁️ Deploy to Render (Free Tier)

Render hosts both the FastAPI backend and React frontend for free.

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial commit — movie recommendation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-system.git
git push -u origin main
```

### Step 2 — Deploy the backend

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Configure:
   | Field | Value |
   |-------|-------|
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn step7_api:app --host 0.0.0.0 --port $PORT` |
   | Plan | Free |
4. Click **Deploy**. Wait ~3 minutes.
5. Copy the live URL — looks like `https://cinrec-api.onrender.com`

> ⚠️ **Important:** Because models are gitignored, you need to either:
> - Commit small `.pkl` files (remove `models/*.pkl` from `.gitignore`), OR
> - Add a `build_models.sh` script that Render runs as part of the build command

### Step 3 — Deploy the frontend

1. **New → Static Site**
2. Connect the same repo
3. Configure:
   | Field | Value |
   |-------|-------|
   | Build Command | `cd frontend && npm install && npm run build` |
   | Publish Directory | `frontend/build` |
4. Add environment variable:
   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | `https://cinrec-api.onrender.com` |
5. Click **Deploy**

### Step 4 — Fix CORS on the backend

Add this to `step7_api.py` before the routes:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cinerec-frontend.onrender.com", "http://localhost:5174"],
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

---

## 🔬 Code Explained (File by File)

<details>
<summary><strong>step1_eda.py</strong> — Exploratory Data Analysis</summary>

Loads `u.data` (ratings) and `u.item` (movies). Computes:
- Matrix **sparsity** = 1 − (actual ratings / possible ratings) = **93.7%**
- Rating distribution histogram
- Ratings-per-user and ratings-per-movie distributions
- Genre frequency chart

Saves PNG charts to `outputs/eda/`.
</details>

<details>
<summary><strong>step2_preprocessing.py</strong> — Data Preprocessing</summary>

1. Reads the raw ratings CSV
2. Builds a **user-item matrix** via `pandas.pivot_table` (rows=users, cols=movies, values=rating)
3. Computes sparsity of the matrix
4. 80/20 train/test split with `sklearn.train_test_split`
5. Serialises everything to `models/preprocessing.pkl` with `joblib`

The matrix is the core data structure — 943 × 1,682, mostly NaN (unrated).
</details>

<details>
<summary><strong>step3_collaborative.py</strong> — Collaborative Filtering</summary>

**User-based CF:**
- Fills NaN with 0, computes `cosine_similarity(user_item_matrix)` → 943×943 similarity matrix
- `find_similar_users(user_id, n)` returns the n most similar users
- `user_based_recommendations(user_id, n)` collects unwatched movies from similar users, weights each by cosine similarity score, returns top-n

**Item-based CF:**
- Transposes the matrix (now movies × users), computes item similarity → 1682×1682
- `find_similar_movies(movie_id, n)` returns most similar movies

**Evaluation:** Iterates the test set, predicts ratings via the weighted-neighbour formula, computes RMSE using `sklearn.metrics.mean_squared_error`.

Saves both similarity matrices to `models/collaborative.pkl`.
</details>

<details>
<summary><strong>step4_svd.py</strong> — SVD Matrix Factorisation</summary>

Uses the **Surprise** library:
1. Wraps ratings in `surprise.Dataset` with `Reader(rating_scale=(1,5))`
2. 5-fold cross-validates `SVD(n_factors=100)` as a baseline
3. `GridSearchCV` over `{n_factors, lr_all, reg_all}` — finds best hyperparameters
4. Re-trains on full data with best params
5. Evaluates RMSE and MAE on the held-out 20% test set
6. `recommend_movies(user_id, n)` calls `model.predict(user_id, movie_id)` for every unwatched movie

SVD decomposes the matrix **R ≈ P × Q^T** where P is the user-factor matrix and Q is the item-factor matrix. Each latent factor captures a hidden taste dimension (e.g. "prefers action", "likes 90s films").

Saves the trained model to `models/svd_model.pkl`.
</details>

<details>
<summary><strong>step5_content.py</strong> — Content-Based Filtering</summary>

1. Reads genre flags from `u.item` (19 binary columns)
2. Converts each movie's flags into a genre string: `"Action Adventure Drama "`
3. Applies `TfidfVectorizer` → sparse matrix of shape (1682, 19)
4. Computes `cosine_similarity(tfidf_matrix)` → 1682×1682 content similarity
5. **User profile** = weighted average of TF-IDF vectors of liked movies (rating ≥ 4), where weight = `rating − 3`
6. Profile is dotted against all movie vectors to score unseen movies

Saves vectoriser, matrix, and similarity to `models/content_model.pkl`.
</details>

<details>
<summary><strong>step6_hybrid_eval.py</strong> — Hybrid Model + Evaluation</summary>

**Hybrid blending:**
```python
svd_norm      = (svd_score − min) / (max − min)    # normalise to [0,1]
content_norm  = (cb_score  − min) / (max − min)
hybrid_score  = 0.7 × svd_norm + 0.3 × content_norm
```

**Full evaluation:**
- RMSE and MAE on the test set for each model
- **Precision@K** = (relevant items in top-K) / K
- **Recall@K** = (relevant items in top-K) / (all relevant items)

A recommendation is "relevant" if predicted rating ≥ 3.5 AND actual rating ≥ 3.5.
</details>

<details>
<summary><strong>step7_api.py</strong> — FastAPI REST API</summary>

Creates a `FastAPI()` app and loads all four `.pkl` model files at startup (once, into memory).

Five endpoints:
- `GET /stats` → dataset counts + model metrics
- `GET /recommend/{user_id}?n=&cf_weight=` → runs hybrid scoring for every unwatched movie, returns top-n sorted by hybrid score
- `GET /similar/{movie_id}?n=` → looks up precomputed content similarity matrix, returns top-n rows
- `GET /user/{user_id}/history?limit=` → filters ratings DataFrame, joins movie titles, returns sorted by rating
- `GET /movies?genre=&limit=` → filters movies DataFrame by genre substring, paginates
</details>

<details>
<summary><strong>frontend/src/api.js</strong> — API Helper</summary>

Single `request(path)` function with error handling. Reads `REACT_APP_API_URL` from environment — empty in dev (uses CRA proxy → port 8000), set to the Render URL in production.
</details>

<details>
<summary><strong>frontend/src/components/Dashboard.jsx</strong> — Interactive Dashboard</summary>

Uses **Recharts** for four live visualisations:
- `BarChart` — rating distribution (★1–★5 counts)
- `BarChart` — model comparison (RMSE + MAE side-by-side for all 4 algorithms)
- `BarChart` (horizontal) — genre coverage percentages
- `PieChart` (donut) — matrix sparsity vs density

Also includes the Quick Recommend widget (calls `/recommend`) and a pipeline architecture explainer.
</details>

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Data | MovieLens 100K, pandas, numpy |
| ML Models | scikit-surprise (SVD), scikit-learn (cosine similarity, TF-IDF) |
| API | FastAPI, uvicorn, joblib |
| Frontend | React 18, Recharts, CSS custom properties |
| Deployment | Render (free tier) |
| Version Control | Git + GitHub |

---

## 📈 Results

| Metric | User CF | Item CF | SVD | Hybrid |
|--------|---------|---------|-----|--------|
| RMSE | 0.98 | 1.02 | 0.79 | **0.76** |
| MAE | 0.77 | 0.81 | 0.61 | **0.58** |
| Precision@10 | — | — | 0.195 | — |
| Recall@10 | — | — | 0.104 | — |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

```bash
# Fork → clone → branch
git checkout -b feat/your-feature
# Make changes, then:
git commit -m "feat: describe your change"
git push origin feat/your-feature
# Open a PR on GitHub
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

**Tanya Tomar** · B.Tech CSE 2027 · RKGIT Ghaziabad  
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

<div align="center">
  <sub>Built with Python, FastAPI, React, and the MovieLens dataset.</sub>
</div>
