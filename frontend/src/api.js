const API_URL = "https://movie-recommendation-system-4p8t.onrender.com";

export async function getStats() {
  const response = await fetch(`${API_URL}/stats`);

  if (!response.ok) {
    throw new Error("Failed to fetch stats");
  }

  return response.json();
}

export async function getRecommendations(userId, n = 10) {
  const response = await fetch(
    `${API_URL}/recommend/${userId}?n=${n}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return response.json();
}

export async function getSimilarMovies(movieId, n = 10) {
  const response = await fetch(
    `${API_URL}/similar/${movieId}?n=${n}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch similar movies");
  }

  return response.json();
}

export async function getMovies(n = 1682, genre = "All") {
  const response = await fetch(
    `${API_URL}/movies?n=${n}&genre=${encodeURIComponent(genre)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch movies");
  }

  return response.json();
}

export async function getHybridRecommendations(userId, n = 10) {
  const response = await fetch(
    `${API_URL}/hybrid/${userId}?n=${n}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch hybrid recommendations");
  }

  return response.json();
}