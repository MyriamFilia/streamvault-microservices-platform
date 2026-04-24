import { reviewApi } from "./api";

// POST /reviews/
export const createReview = (data) =>
  reviewApi.post("/", data);
// data = { series_id, rating, comment }

// PUT /reviews/{id}
export const updateReview = (reviewId, data) =>
  reviewApi.put(`/${reviewId}`, data);
// data = { rating, comment }

// DELETE /reviews/{id}
export const deleteReview = (reviewId) =>
  reviewApi.delete(`/${reviewId}`);

// GET /reviews/series/{series_id}
export const getReviewsForSeries = (seriesId) =>
  reviewApi.get(`/series/${seriesId}`);

// GET /reviews/me
export const getMyReviews = () =>
  reviewApi.get("/me");