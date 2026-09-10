const API_URL = "https://movie-recommendation-system-4p8t.onrender.com";

async function request(path) {
  const response = await fetch(API_URL + path);

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: response.statusText,
    }));

    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  stats: () => request("/stats"),

  recommend: (userId, n = 10) =>
    request(`/recommend/${userId}?n=${n}`),

  hybrid: (userId, n = 10) =>
    request(`/hybrid/${userId}?n=${n}`),

  similar: (movieId, n = 10) =>
    request(`/similar/${movieId}?n=${n}`),

  movies: (genre = "All", n = 20) =>
    request(
      `/movies?genre=${encodeURIComponent(genre || "All")}&n=${n}`
    ),
};