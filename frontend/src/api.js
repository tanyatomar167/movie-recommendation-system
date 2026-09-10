// api.js

const BASE = "https://movie-recommendation-system-4p8t.onrender.com";

async function request(path) {
  const res = await fetch(BASE + path);

  if (!res.ok) {
    const err = await res.json().catch(() => ({
      detail: res.statusText,
    }));

    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
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
    request(`/movies?genre=${encodeURIComponent(genre || "All")}&n=${n}`),
};