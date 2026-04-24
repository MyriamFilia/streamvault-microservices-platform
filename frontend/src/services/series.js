import { seriesApi } from "./api";

// GET /api/popular
export const getPopularSeries = () =>
  seriesApi.get("/popular");

// GET /api/search?q=...
export const searchSeries = (query) =>
  seriesApi.get("/search", { params: { q: query } });

// GET /api/{id}
export const getSeriesDetail = (id) =>
  seriesApi.get(`/${id}`);