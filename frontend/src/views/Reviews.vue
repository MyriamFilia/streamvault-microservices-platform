<template>
  <div class="sv-reviews-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <!-- Header -->
      <div class="sv-page-header">
        <div>
          <h1 class="sv-page-title"> My Reviews</h1>
          <p class="sv-page-subtitle">{{ reviews.length }} review{{ reviews.length !== 1 ? "s" : "" }} written</p>
        </div>
      </div>

      <!-- Toast -->
      <transition name="sv-toast-anim">
        <div v-if="toast.show" class="sv-toast" :class="toast.type">
          {{ toast.message }}
        </div>
      </transition>

      <!-- Loading -->
      <div v-if="loading" class="sv-loading">
        <div class="sv-spinner-lg"></div>
        <p>Loading your reviews...</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="reviews.length === 0" class="sv-empty">
        <div class="sv-empty-icon">⭐</div>
        <h3 class="sv-empty-title">No reviews yet</h3>
        <p class="sv-empty-text">
          Watch series and share your opinion — your reviews will appear here.
        </p>
        <router-link to="/" class="sv-btn-browse">Browse Series</router-link>
      </div>

      <!-- Reviews list -->
      <div v-else class="sv-reviews-list">
        <div
          v-for="review in reviews"
          :key="review.id"
          class="sv-review-card">

          <!-- Poster + Series info -->
          <router-link :to="`/detail/${review.series_id}`" class="sv-review-poster-link">
            <div class="sv-review-poster-wrap">
              <img
                :src="review._series?.image?.medium || review._series?.image?.original || fallbackImage"
                :alt="review._series?.name || `Series #${review.series_id}`"
                class="sv-review-poster"
                loading="lazy" />
            </div>
          </router-link>

          <!-- Content -->
          <div class="sv-review-content">
            <div class="sv-review-top">
              <div>
                <router-link :to="`/detail/${review.series_id}`" class="sv-review-series-name">
                  {{ review._series?.name || `Series #${review.series_id}` }}
                </router-link>
                <div class="sv-review-meta">
                  <span class="sv-review-date">{{ formatDate(review.created_at) }}</span>
                  <span v-if="review._series?.status" class="sv-meta-dot"
                    :class="review._series.status === 'Running' ? 'dot-green' : 'dot-gray'"></span>
                  <span v-if="review._series?.status" class="sv-review-status">
                    {{ review._series.status }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="sv-review-actions">
                <button class="sv-btn-edit" @click="openEdit(review)" title="Edit review">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  Edit
                </button>
                <button class="sv-btn-delete" @click="handleDelete(review.id)" title="Delete review">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                    <path d="M10 11v6M14 11v6"/>
                    <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                  </svg>
                  Delete
                </button>
              </div>
            </div>

            <!-- Stars -->
            <div class="sv-stars">
              <span
                v-for="i in 5"
                :key="i"
                class="sv-star"
                :class="i <= review.rating ? 'sv-star-filled' : 'sv-star-empty'">
                ★
              </span>
              <span class="sv-rating-value">{{ review.rating }}/5</span>
            </div>

            <!-- Comment -->
            <p v-if="review.comment" class="sv-review-comment">{{ review.comment }}</p>
            <p v-else class="sv-review-no-comment">No comment written.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <transition name="sv-modal-anim">
      <div v-if="editModal.show" class="sv-modal-backdrop" @click.self="closeEdit">
        <div class="sv-modal">
          <div class="sv-modal-header">
            <h3 class="sv-modal-title">Edit Review</h3>
            <button class="sv-modal-close" @click="closeEdit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <p class="sv-modal-series-name">{{ editModal.seriesName }}</p>

          <!-- Star picker -->
          <div class="sv-modal-field">
            <label class="sv-label">Rating</label>
            <div class="sv-star-picker">
              <button
                v-for="i in 5"
                :key="i"
                type="button"
                class="sv-star-btn"
                :class="i <= editModal.rating ? 'sv-star-active' : ''"
                @click="editModal.rating = i">
                ★
              </button>
              <span class="sv-rating-value">{{ editModal.rating }}/5</span>
            </div>
          </div>

          <!-- Comment -->
          <div class="sv-modal-field">
            <label class="sv-label">Comment <span class="sv-label-optional">(optional)</span></label>
            <textarea
              v-model="editModal.comment"
              class="sv-textarea"
              placeholder="Share your thoughts about this series..."
              rows="4">
            </textarea>
          </div>

          <div class="sv-modal-footer">
            <button class="sv-btn-cancel" @click="closeEdit">Cancel</button>
            <button class="sv-btn-save" @click="handleUpdate" :disabled="savingEdit">
              <span v-if="savingEdit" class="sv-spinner"></span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import { getMyReviews, updateReview, deleteReview } from "../services/reviews";
import { getSeriesDetail } from "../services/series";

const reviews = ref([]);
const loading = ref(false);
const savingEdit = ref(false);
const fallbackImage = "https://picsum.photos/seed/series/200/300";

const toast = ref({ show: false, message: "", type: "" });
const showToast = (message, type = "sv-toast-success") => {
  toast.value = { show: true, message, type };
  setTimeout(() => { toast.value.show = false; }, 3000);
};

const editModal = ref({
  show: false,
  reviewId: null,
  seriesName: "",
  rating: 5,
  comment: "",
});

// ── Load reviews ────────────────────────────────────────────────
const loadReviews = async () => {
  loading.value = true;
  try {
    const res = await getMyReviews();
    const data = res.data || [];

    const enriched = await Promise.all(
      data.map(async (review) => {
        try {
          const seriesRes = await getSeriesDetail(review.series_id);
          const seriesInfo = seriesRes.data.show || seriesRes.data.data || seriesRes.data;
          return { ...review, _series: seriesInfo };
        } catch {
          return { ...review, _series: null };
        }
      })
    );
    reviews.value = enriched.reverse();
  } catch (error) {
    showToast("Failed to load reviews.", "sv-toast-danger");
  } finally {
    loading.value = false;
  }
};

// ── Delete ──────────────────────────────────────────────────────
const handleDelete = async (reviewId) => {
  if (!confirm("Delete this review? This action cannot be undone.")) return;
  try {
    await deleteReview(reviewId);
    reviews.value = reviews.value.filter(r => r.id !== reviewId);
    showToast("Review deleted.", "sv-toast-danger");
  } catch (error) {
    showToast(error.response?.data?.detail || "Failed to delete review.", "sv-toast-danger");
  }
};

// ── Edit modal ──────────────────────────────────────────────────
const openEdit = (review) => {
  editModal.value = {
    show: true,
    reviewId: review.id,
    seriesName: review._series?.name || `Series #${review.series_id}`,
    rating: review.rating,
    comment: review.comment || "",
  };
};

const closeEdit = () => {
  editModal.value.show = false;
};

const handleUpdate = async () => {
  savingEdit.value = true;
  try {
    const res = await updateReview(editModal.value.reviewId, {
      rating: editModal.value.rating,
      comment: editModal.value.comment,
    });
    const updated = res.data;
    reviews.value = reviews.value.map(r =>
      r.id === updated.id ? { ...r, ...updated } : r
    );
    closeEdit();
    showToast("Review updated successfully ✅");
  } catch (error) {
    showToast(error.response?.data?.detail || "Failed to update review.", "sv-toast-danger");
  } finally {
    savingEdit.value = false;
  }
};

// ── Helpers ─────────────────────────────────────────────────────
const formatDate = (dateStr) => {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric", month: "short", year: "numeric",
  });
};

onMounted(() => loadReviews());
</script>

<style scoped>
.sv-reviews-page {
  min-height: 100vh;
}

/* ── Header ── */
.sv-page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.sv-page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0;
}
.sv-page-subtitle {
  color: #868e96;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

/* ── Toast ── */
.sv-toast {
  display: inline-flex;
  margin-bottom: 1.5rem;
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
.sv-toast-danger {
  background: rgba(220, 53, 69, 0.08);
  border: 1px solid rgba(220, 53, 69, 0.25);
  color: #dc3545;
}
.sv-toast-anim-enter-active,
.sv-toast-anim-leave-active { transition: opacity 0.3s, transform 0.3s; }
.sv-toast-anim-enter-from,
.sv-toast-anim-leave-to { opacity: 0; transform: translateY(-6px); }

/* ── Loading ── */
.sv-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5rem 1rem;
  gap: 1rem;
  color: #868e96;
  font-size: 0.9rem;
}
.sv-spinner-lg {
  width: 32px;
  height: 32px;
  border: 3px solid #e9ecef;
  border-top-color: #6c8fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* ── Empty ── */
.sv-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 5rem 1rem;
}
.sv-empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1.25rem;
  opacity: 0.4;
}
.sv-empty-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #343a40;
  margin-bottom: 0.5rem;
}
.sv-empty-text {
  color: #868e96;
  font-size: 0.9rem;
  max-width: 38ch;
  margin-bottom: 1.5rem;
}
.sv-btn-browse {
  padding: 0.65rem 1.5rem;
  background: #6c8fff;
  color: #fff;
  border-radius: 9999px;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.2s;
}
.sv-btn-browse:hover { background: #5a7aff; }

/* ── Reviews list ── */
.sv-reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* ── Review Card ── */
.sv-review-card {
  display: flex;
  gap: 1.25rem;
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  padding: 1.25rem;
  transition: box-shadow 0.2s, transform 0.2s;
}
.sv-review-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

/* Poster */
.sv-review-poster-link { flex-shrink: 0; display: block; }
.sv-review-poster-wrap {
  width: 64px;
  aspect-ratio: 2/3;
  border-radius: 10px;
  overflow: hidden;
  background: #f1f3f5;
}
.sv-review-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}
.sv-review-poster-link:hover .sv-review-poster { transform: scale(1.06); }

/* Content */
.sv-review-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.sv-review-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.sv-review-series-name {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  text-decoration: none;
  line-height: 1.3;
}
.sv-review-series-name:hover { color: #6c8fff; }

.sv-review-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.2rem;
}
.sv-review-date {
  font-size: 0.78rem;
  color: #adb5bd;
}
.sv-meta-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-green { background: #20c997; }
.dot-gray { background: #adb5bd; }
.sv-review-status {
  font-size: 0.75rem;
  color: #868e96;
}

/* Actions */
.sv-review-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}
.sv-btn-edit,
.sv-btn-delete {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid;
}
.sv-btn-edit {
  background: rgba(108, 143, 255, 0.07);
  color: #6c8fff;
  border-color: rgba(108, 143, 255, 0.25);
}
.sv-btn-edit:hover {
  background: rgba(108, 143, 255, 0.15);
}
.sv-btn-delete {
  background: rgba(220, 53, 69, 0.06);
  color: #dc3545;
  border-color: rgba(220, 53, 69, 0.18);
}
.sv-btn-delete:hover {
  background: rgba(220, 53, 69, 0.14);
}

/* Stars */
.sv-stars {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}
.sv-star {
  font-size: 1rem;
  line-height: 1;
}
.sv-star-filled { color: #f59e0b; }
.sv-star-empty { color: #dee2e6; }
.sv-rating-value {
  font-size: 0.8rem;
  font-weight: 600;
  color: #495057;
  margin-left: 0.4rem;
}

/* Comment */
.sv-review-comment {
  font-size: 0.875rem;
  color: #495057;
  line-height: 1.6;
  margin: 0;
}
.sv-review-no-comment {
  font-size: 0.82rem;
  color: #adb5bd;
  font-style: italic;
  margin: 0;
}

/* ── Modal ── */
.sv-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.sv-modal {
  background: #fff;
  border-radius: 20px;
  padding: 1.75rem;
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}
.sv-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sv-modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}
.sv-modal-close {
  background: transparent;
  border: none;
  color: #adb5bd;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.2s;
  display: flex;
}
.sv-modal-close:hover { color: #495057; }

.sv-modal-series-name {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
  margin: 0;
}

.sv-modal-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.sv-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.sv-label-optional {
  font-weight: 400;
  text-transform: none;
  letter-spacing: 0;
  color: #adb5bd;
}

/* Star picker */
.sv-star-picker {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.sv-star-btn {
  font-size: 1.6rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #dee2e6;
  transition: color 0.15s, transform 0.15s;
  padding: 0;
  line-height: 1;
}
.sv-star-btn:hover,
.sv-star-active { color: #f59e0b; }
.sv-star-btn:hover { transform: scale(1.15); }

/* Textarea */
.sv-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  font-size: 0.9rem;
  color: #1a1a1a;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
}
.sv-textarea:focus {
  border-color: #6c8fff;
  background: #fff;
}
.sv-textarea::placeholder { color: #adb5bd; }

.sv-modal-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 0.25rem;
}
.sv-btn-cancel {
  padding: 0.6rem 1.25rem;
  background: transparent;
  color: #6c757d;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-cancel:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}
.sv-btn-save {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.5rem;
  background: #6c8fff;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  min-width: 130px;
}
.sv-btn-save:hover:not(:disabled) { background: #5a7aff; }
.sv-btn-save:disabled { opacity: 0.5; cursor: not-allowed; }

/* Spinner */
.sv-spinner {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Modal animation */
.sv-modal-anim-enter-active,
.sv-modal-anim-leave-active { transition: opacity 0.25s, transform 0.25s; }
.sv-modal-anim-enter-from,
.sv-modal-anim-leave-to { opacity: 0; transform: scale(0.95); }

/* Responsive */
@media (max-width: 576px) {
  .sv-review-card { flex-direction: column; }
  .sv-review-poster-wrap { width: 100%; aspect-ratio: 16/9; }
  .sv-review-poster { object-position: top; }
  .sv-review-actions { align-self: flex-end; }
}
</style>