<template>
  <div class="sv-favorites-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <!-- Header -->
      <div class="sv-page-header">
        <div>
          <h1 class="sv-page-title">❤️ My Favorites</h1>
          <p class="sv-page-subtitle">
            {{ favorites.length }} series saved
          </p>
        </div>
        <button
          v-if="favorites.length > 0"
          class="sv-btn-clear"
          @click="clearAll">
          Clear all
        </button>
      </div>

      <!-- Toast -->
      <transition name="sv-toast-anim">
        <div v-if="toast.show" class="sv-toast" :class="toast.type">
          {{ toast.message }}
        </div>
      </transition>

      <!-- Empty state -->
      <div v-if="favorites.length === 0" class="sv-empty">
        <div class="sv-empty-icon">❤️</div>
        <h3 class="sv-empty-title">No favorites yet</h3>
        <p class="sv-empty-text">
          Browse series and add them to your favorites to find them here.
        </p>
        <router-link to="/" class="sv-btn-browse">Browse Series</router-link>
      </div>

      <!-- Mini cards grid -->
      <div v-else class="sv-grid">
        <div v-for="series in favorites" :key="series.id" class="sv-mini-card">
          <!-- Poster -->
          <router-link :to="`/detail/${series.id}`" class="sv-poster-link">
            <div class="sv-poster-wrap">
              <img
                :src="
                  series.image?.medium ||
                  series.image?.original ||
                  fallbackImage
                "
                :alt="series.name"
                class="sv-poster"
                loading="lazy" />
              <!-- Overlay au hover -->
              <div class="sv-poster-overlay">
                <span class="sv-overlay-btn">View Details</span>
              </div>
            </div>
          </router-link>

          <!-- Info -->
          <div class="sv-card-body">
            <div class="sv-card-top">
              <h4 class="sv-card-title">{{ series.name }}</h4>
              <div class="sv-card-meta">
                <span v-if="series.rating?.average" class="sv-meta-item">
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="#f59e0b"
                    stroke="none">
                    <polygon
                      points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                  {{ series.rating.average }}
                </span>
                <span
                  v-if="series.status"
                  class="sv-status-dot"
                  :class="
                    series.status === 'Running' ? 'dot-green' : 'dot-gray'
                  "></span>
                <span class="sv-meta-text">{{
                  series.status || "Unknown"
                }}</span>
              </div>
              <p v-if="series.genres?.length" class="sv-genres">
                {{ series.genres.slice(0, 2).join(" · ") }}
              </p>
            </div>

            <!-- Remove -->
            <button class="sv-btn-remove" @click="handleRemoveFavorite(series.id)">
              <svg
                width="13"
                height="13"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                <path d="M10 11v6M14 11v6" />
                <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
              </svg>
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import { getMyFavorites, deleteFavorite } from "../services/favorites";
import { getSeriesDetail } from "../services/series";

const token = ref(localStorage.getItem("token"));
const favorites = ref([]);
const loading = ref(false);
const fallbackImage = "https://picsum.photos/seed/series/200/300";

const toast = ref({ show: false, message: "", type: "" });
const showToast = (message, type = "sv-toast-success") => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3000);
};

// Charger les favoris depuis le Backend
const loadFavorites = async () => {
  if (!token.value) return;
  loading.value = true;
  try {
    const response = await getMyFavorites();
    const favoritesData = response.data || [];

    const seriesPromises = await Promise.all(
      favoritesData.map(async (fav) => {
        try {
          const seriesResponse = await getSeriesDetail(fav.series_id);
          const seriesInfo = seriesResponse.data.show || seriesResponse.data.data || seriesResponse.data;
          return {
            ...seriesInfo,
            _fav_id: fav.id,
          };
        } catch (error) {
            console.error("Error loading series:", error);
            return { id: fav.series_id, _fav_id: fav.id, name: `Series #${fav.series_id}` };
          }
      })
    );
    favorites.value = seriesPromises.filter(item => item !== null).reverse();
  } catch (error) {
    console.error("Error loading favorites:", error);
    showToast("Failed to load favorites.", "sv-toast-danger");
  } finally {
    loading.value = false;
  }
};

// Supprimer un favori
const handleRemoveFavorite = async (favoriteId) => {
  const fav = favorites.value.find(f => f.id === favoriteId);
  if (!fav) return;
  try {
    await deleteFavorite(fav._fav_id);
    favorites.value = favorites.value.filter(f => f.id !== favoriteId);
    showToast("Removed from favorites", "sv-toast-danger");
  } catch (error) {
    showToast(error.response?.data?.detail || "Failed to remove.", "sv-toast-danger");
  }
};


// ── Clear all ──────────────────────────────────────────────────
const clearAll = async () => {
  try {
    await Promise.all(favorites.value.map(f => deleteFavorite(f._fav_id)));
    favorites.value = [];
    showToast("All favorites cleared", "sv-toast-danger");
  } catch (error) {
    showToast("Failed to clear all favorites.", "sv-toast-danger");
  }
};

onMounted(() => loadFavorites());
</script>

<style scoped>
.sv-favorites-page {
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

.sv-btn-clear {
  padding: 0.5rem 1.1rem;
  background: rgba(220, 53, 69, 0.08);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.25);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.sv-btn-clear:hover {
  background: rgba(220, 53, 69, 0.16);
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
  max-width: 36ch;
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
.sv-btn-browse:hover {
  background: #5a7aff;
}

/* ── Grid ── */
.sv-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1.25rem;
}
@media (max-width: 576px) {
  .sv-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.875rem;
  }
}

/* ── Mini Card ── */
.sv-mini-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  overflow: hidden;
  transition:
    box-shadow 0.2s,
    transform 0.2s;
  display: flex;
  flex-direction: column;
}
.sv-mini-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

/* Poster */
.sv-poster-link {
  display: block;
  text-decoration: none;
}
.sv-poster-wrap {
  position: relative;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: #f1f3f5;
}
.sv-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}
.sv-mini-card:hover .sv-poster {
  transform: scale(1.04);
}

.sv-poster-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.25s;
}
.sv-mini-card:hover .sv-poster-overlay {
  opacity: 1;
}
.sv-overlay-btn {
  padding: 0.45rem 1rem;
  background: rgba(255, 255, 255, 0.95);
  color: #1a1a1a;
  border-radius: 9999px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

/* Card body */
.sv-card-body {
  padding: 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  flex: 1;
}
.sv-card-top {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  flex: 1;
}

.sv-card-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.3;
  /* Tronquer à 2 lignes */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sv-card-meta {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  flex-wrap: wrap;
}
.sv-meta-item {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #495057;
}
.sv-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-green {
  background: #20c997;
}
.dot-gray {
  background: #adb5bd;
}
.sv-meta-text {
  font-size: 0.75rem;
  color: #868e96;
}

.sv-genres {
  font-size: 0.73rem;
  color: #adb5bd;
  margin: 0;
  line-height: 1.3;
}

/* Remove button */
.sv-btn-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  width: 100%;
  padding: 0.45rem;
  background: rgba(220, 53, 69, 0.06);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.18);
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-remove:hover {
  background: rgba(220, 53, 69, 0.14);
}
</style>
