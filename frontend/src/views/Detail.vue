<template>
  <div class="sv-detail-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div v-if="series" class="container py-5">
      <!-- Hero Section -->
      <div class="sv-hero">
        <img
          :src="series.image?.original || fallbackImage"
          class="sv-poster"
          :alt="series.name" />

        <div class="sv-hero-info">
          <h1 class="sv-title">{{ series.name }}</h1>

          <div class="sv-badges">
            <span class="sv-badge sv-badge-yellow">
              <template v-if="localAverageRating">
                ⭐ {{ localAverageRating }}/5 (StreamVault)
              </template>
              <template v-else-if="series.rating?.average">
                ⭐ {{ series.rating.average }}/10 (TVMaze)
              </template>
              <template v-else> ⭐ No rating </template>
            </span>
            <span class="sv-badge sv-badge-blue">{{
              series.language || "Unknown"
            }}</span>
            <span
              class="sv-badge"
              :class="
                series.status === 'Running' ? 'sv-badge-green' : 'sv-badge-gray'
              ">
              {{ series.status || "Unknown" }}
            </span>
          </div>

          <p class="sv-summary">{{ cleanSummary(series.summary) }}</p>

          <button
            v-if="token"
            class="sv-btn-fav"
            :class="{ 'sv-btn-fav--active': isFavorite }"
            @click="toggleFavorite"
            :disabled="favLoading">
            <span v-if="favLoading">...</span>
            <span v-else-if="isFavorite">💔 Remove from Favorites</span>
            <span v-else>❤️ Add to Favorites</span>
          </button>
          <p v-else class="sv-login-hint">
            Sign in to add this series to your favorites
          </p>

          <transition name="sv-toast-anim">
            <div v-if="toast.show" class="sv-toast" :class="toast.type">
              {{ toast.message }}
            </div>
          </transition>
        </div>
      </div>

      <hr class="sv-divider" />

      <!-- Reviews Section -->
      <div class="sv-reviews-section">
        <h2 class="sv-section-title">Reviews</h2>

        <!-- Formulaire -->
        <div v-if="token" class="sv-review-form">
          <h3 class="sv-form-title">
            {{ editMode ? "Edit your review" : "Write a review" }}
          </h3>

          <div class="sv-field">
            <label class="sv-label">Rating (1–5)</label>
            <div class="sv-input-wrap">
              <svg
                class="sv-input-icon"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2">
                <polygon
                  points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              <input
                v-model="reviewRating"
                type="number"
                min="1"
                max="5"
                class="sv-input"
                placeholder="Score out of 5" />
            </div>
          </div>

          <div class="sv-field">
            <label class="sv-label">Comment</label>
            <div class="sv-textarea-wrap">
              <textarea
                v-model="reviewComment"
                class="sv-textarea"
                rows="4"
                placeholder="Share your thoughts about this series..."></textarea>
            </div>
          </div>

          <div v-if="formError" class="sv-form-error">⚠️ {{ formError }}</div>

          <div class="sv-form-actions">
            <button
              class="sv-btn-submit"
              @click="submitReview"
              :disabled="isSubmitting">
              <span v-if="isSubmitting">Submitting...</span>
              <span v-else>{{
                editMode ? "Update Review" : "Publish Review"
              }}</span>
            </button>
            <button v-if="editMode" class="sv-btn-cancel" @click="cancelEdit">
              Cancel
            </button>
          </div>
        </div>

        <div v-else class="sv-login-prompt">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2">
            <circle cx="12" cy="8" r="4" />
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
          </svg>
          <span>Sign in or register to leave a review</span>
        </div>

        <!-- Empty state -->
        <div v-if="reviews.length === 0" class="sv-no-reviews">
          No reviews yet. Be the first to share your opinion!
        </div>

        <!-- Liste reviews -->
        <div v-for="review in reviews" :key="review.id" class="sv-review-card">
          <div v-if="editingId === review.id" class="sv-inline-edit">
            <div class="sv-field">
              <label class="sv-label">Rating (1–5)</label>
              <div class="sv-star-picker-inline">
                <button
                  v-for="i in 5"
                  :key="i"
                  @click="reviewRating = i"
                  class="sv-star-btn"
                  :class="i <= reviewRating ? 'sv-star-active' : ''">
                  ★
                </button>
                <span class="ms-2 text-muted">{{ reviewRating }}/5</span>
              </div>
            </div>
            <div class="sv-field">
              <textarea
                v-model="reviewComment"
                class="sv-textarea"
                rows="3"></textarea>
            </div>
            <div class="sv-form-actions">
              <button
                class="sv-btn-submit"
                @click="submitReview"
                :disabled="isSubmitting">
                {{ isSubmitting ? "Saving..." : "Save Changes" }}
              </button>
              <button class="sv-btn-cancel" @click="cancelEdit">Cancel</button>
            </div>
          </div>

          <template v-else>
            <div class="sv-review-header">
              <div class="sv-review-user">
                <div class="sv-avatar">
                  {{
                    review.display_name
                      ? review.display_name.charAt(0).toUpperCase()
                      : "U"
                  }}
                </div>
                <span class="sv-username">{{ review.display_name }}</span>
              </div>
              <span class="sv-badge sv-badge-yellow"
                >⭐ {{ review.rating }}/5</span
              >
            </div>

            <p class="sv-review-comment">{{ review.comment }}</p>

            <div
              v-if="Number(review.user_id) === Number(currentUserId)"
              class="sv-review-actions">
              <button class="sv-btn-edit" @click="editReview(review)">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <path
                    d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                  <path
                    d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                </svg>
                Edit
              </button>
              <button class="sv-btn-delete" @click="deleteReview(review.id)">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <polyline points="3 6 5 6 21 6" />
                  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                  <path d="M10 11v6M14 11v6" />
                  <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
                </svg>
                Delete
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import { getSeriesDetail } from "../services/series";
import {
  getReviewsForSeries,
  createReview,
  updateReview,
  deleteReview as deleteReviewApi,
} from "../services/reviews";
import {
  addFavorite,
  getMyFavorites,
  deleteFavorite,
} from "../services/favorites";

const route = useRoute();
const router = useRouter();
const series = ref(null);
const fallbackImage = "https://picsum.photos/400/600";
const token = ref(localStorage.getItem("token"));
const currentUser = ref(localStorage.getItem("username") || "");

//💡 Fonction pour extraire l'ID utilisateur du JWT
const getUserIdFromToken = () => {
  if (!token.value) return null;
  try {
    const payload = JSON.parse(atob(token.value.split(".")[1]));
    return parseInt(payload.sub);
  } catch (e) {
    return null;
  }
};
const currentUserId = ref(getUserIdFromToken());
const generateUsername = (userId) => {
  if (userId === currentUserId.value) return currentUser.value;
  const adjectives = [
    "Cool",
    "Smart",
    "Cinephile",
    "Binger",
    "Fan",
    "Watcher",
    "Critic",
  ];
  const adj = adjectives[userId % adjectives.length];
  return `${adj}_${userId}`;
};

// Reviews state

const reviews = ref([]);

const localAverageRating = computed(() => {
  if (!reviews.value || reviews.value.length === 0) return null;
  const sum = reviews.value.reduce((acc, review) => acc + review.rating, 0);
  return (sum / reviews.value.length).toFixed(1);
});

const reviewRating = ref("");
const reviewComment = ref("");
const editMode = ref(false);
const editingId = ref(null);
const formError = ref("");
const isSubmitting = ref(false);

// Favorites state
const isFavorite = ref(false);
const favoriteId = ref(null); // l'id BDD du favori (pour pouvoir le supprimer)
const favLoading = ref(false);

// Toast state
const toast = ref({ show: false, message: "", type: "" });
const showToast = (message, type = "sv-toast-success") => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3000);
};

//Helper pour nettoyer les balises HTML du résumé
const cleanSummary = (html) => {
  if (!html) return "No summary available.";
  return html.replace(/<[^>]+>/g, "");
};

// Chargement des détails de la série
const loadSeriesDetail = async () => {
  try {
    const response = await getSeriesDetail(route.params.id);
    series.value = response.data.show || response.data.data || response.data;
  } catch (error) {
    console.error("Series load error:", error);
  }
};

//Chargement des reviews
const loadReviews = async () => {
  try {
    const response = await getReviewsForSeries(route.params.id);
    const reviewsWithNames = Array.isArray(response.data)
      ? response.data.map((review) => ({
          ...review,
          display_name: generateUsername(review.user_id),
        }))
      : [];
    reviews.value = Array.isArray(response.data)
      ? [...reviewsWithNames].reverse()
      : [];
  } catch (error) {
    console.error("Reviews load error:", error);
    reviews.value = [];
  }
};

// ── Vérifier si déjà en favori ────────────────────────────────
const checkFavoriteStatus = async () => {
  if (!token.value || !series.value) return;
  try {
    const response = await getMyFavorites();
    const fav = response.data.find((f) => f.series_id === series.value.id);
    if (fav) {
      isFavorite.value = true;
      favoriteId.value = fav.id;
    }
  } catch (error) {
    console.error("Error checking favorite status:", error);
  }
};

// ── Toggle favori ──────────────────────────────────────────────
const toggleFavorite = async () => {
  if (!token.value) {
    router.push({ path: "/", query: { login: "required" } });
    return;
  }
  favLoading.value = true;
  try {
    if (isFavorite.value) {
      await deleteFavorite(favoriteId.value);
      isFavorite.value = false;
      favoriteId.value = null;
      showToast("Removed from favorites", "sv-toast-danger");
    } else {
      const response = await addFavorite(series.value.id);
      isFavorite.value = true;
      favoriteId.value = response.data.id;
      showToast("Added to favorites ❤️", "sv-toast-success");
    }
  } catch (error) {
    const msg = error.response?.data?.detail || "Error updating favorites";
    showToast(msg, "sv-toast-danger");
  } finally {
    favLoading.value = false;
  }
};

// ── Éditer review (Sur place) ──────────────────────────────────
const editReview = (review) => {
  editMode.value = true;
  editingId.value = review.id; // Active le v-if dans la carte
  reviewRating.value = Number(review.rating);
  reviewComment.value = review.comment;
  // Plus de scroll ! On édite là où on est.
};

const cancelEdit = () => {
  reviewRating.value = 1; // Défaut
  reviewComment.value = "";
  editMode.value = false;
  editingId.value = null;
  formError.value = "";
};

// ── Soumission (Note bridée à 5) ────────────────────────────────
const submitReview = async () => {
  formError.value = "";
  if (!reviewRating.value || !reviewComment.value.trim()) {
    formError.value = "Please fill in all fields.";
    return;
  }

  isSubmitting.value = true;
  try {
    if (editMode.value) {
      await updateReview(editingId.value, {
        rating: Math.min(Number(reviewRating.value), 5), // Sécurité : max 5
        comment: reviewComment.value,
      });
      showToast("Review updated! ✨");
    } else {
      await createReview({
        series_id: series.value.id,
        rating: Math.min(Number(reviewRating.value), 5),
        comment: reviewComment.value,
      });
      showToast("Review published! 🚀");
    }
    cancelEdit();
    await loadReviews();
  } catch (error) {
    formError.value = error.response?.data?.detail || "Error.";
  } finally {
    isSubmitting.value = false;
  }
};

// ── Supprimer review ───────────────────────────────────────────
const deleteReview = async (id) => {
  try {
    await deleteReviewApi(id);
    showToast("Review deleted", "sv-toast-danger");
    await loadReviews();
  } catch (error) {
    showToast(
      error.response?.data?.detail || "Failed to delete review.",
      "sv-toast-danger",
    );
  }
};

// ── Mounted ────────────────────────────────────────────────────
onMounted(async () => {
  await loadSeriesDetail();
  if (series.value) {
    await checkFavoriteStatus();
    await loadReviews();
  }
});
</script>

<style scoped>
/* Pas de background — hérite du blanc global via App.vue */
.sv-detail-page {
  min-height: 100vh;
}

/* Hero */
.sv-hero {
  display: flex;
  gap: 2.5rem;
  align-items: flex-start;
  margin-bottom: 2rem;
}
.sv-poster {
  width: 260px;
  flex-shrink: 0;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}
.sv-hero-info {
  flex: 1;
}

.sv-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 1rem;
  line-height: 1.2;
}

/* Badges */
.sv-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}
.sv-badge {
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
}
.sv-badge-yellow {
  background: rgba(255, 193, 7, 0.15);
  color: #b8860b;
  border: 1px solid rgba(255, 193, 7, 0.4);
}
.sv-badge-blue {
  background: rgba(108, 143, 255, 0.12);
  color: #4a6fd8;
  border: 1px solid rgba(108, 143, 255, 0.3);
}
.sv-badge-green {
  background: rgba(25, 135, 84, 0.12);
  color: #146c43;
  border: 1px solid rgba(25, 135, 84, 0.3);
}
.sv-badge-gray {
  background: #f1f3f5;
  color: #868e96;
  border: 1px solid #dee2e6;
}

.sv-summary {
  color: #495057;
  line-height: 1.75;
  margin-bottom: 1.5rem;
  max-width: 70ch;
}

/* Favoris */
.sv-btn-fav {
  padding: 0.65rem 1.5rem;
  background: rgba(220, 53, 69, 0.08);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.25);
  border-radius: 9999px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-fav:hover {
  background: rgba(220, 53, 69, 0.16);
  transform: translateY(-1px);
}
.sv-login-hint {
  font-size: 0.9rem;
  color: #868e96;
}

/* Toast */
.sv-toast {
  display: inline-flex;
  margin-top: 1rem;
  padding: 0.6rem 1.1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
}
.sv-toast-success {
  background: rgba(25, 135, 84, 0.1);
  border: 1px solid rgba(25, 135, 84, 0.3);
  color: #146c43;
}
.sv-toast-info {
  background: rgba(108, 143, 255, 0.1);
  border: 1px solid rgba(108, 143, 255, 0.3);
  color: #4a6fd8;
}
.sv-toast-danger {
  background: rgba(220, 53, 69, 0.08);
  border: 1px solid rgba(220, 53, 69, 0.25);
  color: #dc3545;
}
.sv-toast-anim-enter-active,
.sv-toast-anim-leave-active {
  transition:
    opacity 0.3s,
    transform 0.3s;
}
.sv-toast-anim-enter-from,
.sv-toast-anim-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.sv-divider {
  border-color: #dee2e6;
  margin: 2.5rem 0;
}

/* Reviews */
.sv-reviews-section {
  max-width: 800px;
}
.sv-section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1.5rem;
}

/* Formulaire */
.sv-review-form {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 18px;
  padding: 1.75rem;
  margin-bottom: 2rem;
}
.sv-form-title {
  font-size: 1rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 1.25rem;
}
.sv-field {
  margin-bottom: 1.1rem;
}
.sv-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.4rem;
}
.sv-input-wrap {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  transition: border-color 0.2s;
}
.sv-input-wrap:focus-within {
  border-color: #6c8fff;
}
.sv-input-icon {
  margin-left: 1rem;
  color: #adb5bd;
  flex-shrink: 0;
}
.sv-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #1a1a1a;
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
}
.sv-input::placeholder {
  color: #adb5bd;
}

.sv-textarea-wrap {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  transition: border-color 0.2s;
}
.sv-textarea-wrap:focus-within {
  border-color: #6c8fff;
}
.sv-textarea {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #1a1a1a;
  padding: 0.85rem 1rem;
  font-size: 0.9rem;
  resize: vertical;
}
.sv-textarea::placeholder {
  color: #adb5bd;
}

.sv-form-error {
  font-size: 0.85rem;
  color: #dc3545;
  margin-bottom: 0.75rem;
}
.sv-form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.sv-btn-submit {
  padding: 0.65rem 1.5rem;
  background: #6c8fff;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.sv-btn-submit:hover {
  background: #5a7aff;
}

.sv-btn-cancel {
  padding: 0.65rem 1.25rem;
  background: transparent;
  color: #6c757d;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-cancel:hover {
  color: #343a40;
  border-color: #adb5bd;
}

/* Login prompt */
.sv-login-prompt {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 1rem 1.25rem;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  color: #868e96;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

/* No reviews */
.sv-no-reviews {
  text-align: center;
  padding: 3rem 1rem;
  color: #adb5bd;
  font-size: 0.95rem;
}

/* Review cards */
.sv-review-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  transition: box-shadow 0.2s;
}
.sv-review-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.sv-review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.sv-review-user {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}
.sv-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(108, 143, 255, 0.12);
  color: #6c8fff;
  font-weight: 700;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sv-username {
  font-weight: 600;
  font-size: 0.9rem;
  color: #343a40;
}
.sv-review-comment {
  color: #495057;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 0.75rem;
}

.sv-review-actions {
  display: flex;
  gap: 0.5rem;
}
.sv-btn-edit,
.sv-btn-delete {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.875rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}
.sv-btn-edit {
  background: rgba(255, 193, 7, 0.1);
  color: #b8860b;
  border: 1px solid rgba(255, 193, 7, 0.3);
}
.sv-btn-edit:hover {
  background: rgba(255, 193, 7, 0.2);
}
.sv-btn-delete {
  background: rgba(220, 53, 69, 0.08);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.2);
}
.sv-btn-delete:hover {
  background: rgba(220, 53, 69, 0.15);
}
.sv-btn-fav--active {
  background: rgba(220, 53, 69, 0.18);
  border-color: rgba(220, 53, 69, 0.5);
}
.sv-badge-sub {
  font-weight: 400;
  font-size: 0.7rem;
  opacity: 0.75;
  margin-left: 0.2rem;
}
/* Style pour l'édition sur place */
.sv-star-picker-inline {
  display: flex;
  gap: 5px;
  align-items: center;
  margin-bottom: 10px;
}
.sv-star-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #ccc;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
}
.sv-star-btn.sv-star-active {
  color: #f59e0b; /* Jaune or */
}
.sv-inline-edit {
  width: 100%;
}
.sv-inline-edit .sv-textarea {
  border: 1px solid #6c8fff;
  background: #fff;
  border-radius: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .sv-hero {
    flex-direction: column;
  }
  .sv-poster {
    width: 100%;
    max-width: 280px;
    margin: 0 auto;
  }
  .sv-title {
    font-size: 1.6rem;
  }
}
</style>
