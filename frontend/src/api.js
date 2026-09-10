// api.js

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


// ================================
// Original API functions
// ================================

export const getStats = () => {
  return request("/stats");
};


export const getRecommendations = (userId, n = 10) => {
  return request(`/recommend/${userId}?n=${n}`);
};


export const getHybridRecommendations = (userId, n = 10) => {
  return request(`/hybrid/${userId}?n=${n}`);
};


export const getSimilarMovies = (movieId, n = 10) => {
  return request(`/similar/${movieId}?n=${n}`);
};


export const getMovies = (genre = "All", n = 20) => {
  return request(
    `/movies?genre=${encodeURIComponent(genre || "All")}&n=${n}`
  );
};


// ================================
// api object
// ================================

export const api = {
  stats: getStats,

  recommend: getRecommendations,

  hybrid: getHybridRecommendations,

  similar: getSimilarMovies,

  movies: getMovies,
};