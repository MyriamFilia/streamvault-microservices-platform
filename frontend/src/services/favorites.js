import { favoriteApi } from "./api";

// POST /favorites/
export const addFavorite = (seriesId) =>
  favoriteApi.post("/", { series_id: seriesId });

// GET /favorites/
export const getMyFavorites = () =>
  favoriteApi.get("/");

// DELETE /favorites/{id}
export const deleteFavorite = (favoriteId) =>
  favoriteApi.delete(`/${favoriteId}`);