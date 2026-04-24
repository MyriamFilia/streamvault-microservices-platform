import axios from "axios";

export const userApi = axios.create({
  baseURL: "/users",
  headers: { "Content-Type": "application/json" }
});

export const seriesApi = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" }
});

export const reviewApi = axios.create({
  baseURL: "/reviews",
  headers: { "Content-Type": "application/json" }
});

export const favoriteApi = axios.create({
  baseURL: "/favorites",
  headers: { "Content-Type": "application/json" }
});

// ── Intercepteur global (Requête) ──────────────────────────────
// Injecte le token JWT sur toutes les requêtes sortantes
const authInterceptor = (config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

userApi.interceptors.request.use(authInterceptor);
reviewApi.interceptors.request.use(authInterceptor);
favoriteApi.interceptors.request.use(authInterceptor);

// ── Intercepteur global (Réponse) ──────────────────────────────
// Déconnexion auto si le token est expiré ou invalide (Erreur 401)
// Déconnexion auto si le token est expiré (Sauf pour la page de Login !)
const expiredTokenInterceptor = (error) => {
  if (error.response?.status === 401 && !error.config.url.includes("login")) {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("email");
    window.location.href = "/?login=required"; 
  }
  return Promise.reject(error);
};

// On applique cette règle de réponse à toutes les API protégées
userApi.interceptors.response.use((response) => response, expiredTokenInterceptor);
reviewApi.interceptors.response.use((response) => response, expiredTokenInterceptor);
favoriteApi.interceptors.response.use((response) => response, expiredTokenInterceptor);