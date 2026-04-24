<template>
  <div class="sv-home">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <!-- Header -->
      <div class="sv-home-header">
        <h1 class="sv-home-title">Popular Series</h1>
        <p class="sv-home-subtitle">
          Discover the most watched series right now
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="sv-loading">
        <div class="sv-spinner"></div>
        <span>Loading series...</span>
      </div>

      <!-- Erreur -->
      <div v-if="errorMsg && !loading" class="sv-error">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        {{ errorMsg }}
        <button class="sv-retry" @click="loadPopularSeries">Retry</button>
      </div>

      <!-- Grille -->
      <div v-else class="row">
        <SeriesCard
          v-for="series in paginatedSeries"
          :key="series.id"
          :series="series" />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="sv-pagination">
        <button
          class="sv-page-btn"
          @click="prevPage"
          :disabled="currentPage === 1">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5">
            <path d="M15 18l-6-6 6-6" />
          </svg>
          Previous
        </button>

        <div class="sv-page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            class="sv-page-num"
            :class="{ active: page === currentPage, dots: page === '...' }"
            @click="page !== '...' && goToPage(page)">
            {{ page }}
          </button>
        </div>

        <button
          class="sv-page-btn"
          @click="nextPage"
          :disabled="currentPage === totalPages">
          Next
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import SeriesCard from "../components/SeriesCard.vue";
import { getPopularSeries } from "../services/series";

const route = useRoute();
const router = useRouter();
const seriesList = ref([]);
const currentPage = ref(1);
const itemsPerPage = 12;
const loading = ref(true);
const errorMsg = ref("");

const paginatedSeries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return seriesList.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() =>
  Math.ceil(seriesList.value.length / itemsPerPage),
);

const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);

  const pages = [];
  if (current <= 4) {
    pages.push(1, 2, 3, 4, 5, "...", total);
  } else if (current >= total - 3) {
    pages.push(1, "...", total - 4, total - 3, total - 2, total - 1, total);
  } else {
    pages.push(1, "...", current - 1, current, current + 1, "...", total);
  }
  return pages;
});

const goToPage = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: "smooth" });
};
const nextPage = () => {
  if (currentPage.value < totalPages.value) goToPage(currentPage.value + 1);
};
const prevPage = () => {
  if (currentPage.value > 1) goToPage(currentPage.value - 1);
};

const loadPopularSeries = async () => {
  errorMsg.value = "";
  loading.value = true;
  try {
    const response = await getPopularSeries();
    seriesList.value = Array.isArray(response.data)
      ? response.data
      : response.data.results || response.data.data || [];
  } catch (error) {
    console.error(error);
    errorMsg.value = "Failed to load popular series.";
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPopularSeries();
  if (route.query.login === "required") {
    await router.replace({ query: {} });
    const loginModalElement = document.getElementById("loginModal");
    if (loginModalElement && window.bootstrap) {
      new window.bootstrap.Modal(loginModalElement).show();
    }
  }
});
</script>

<style scoped>
.sv-home {
  min-height: 100vh;
}

/* Header */
.sv-home-header {
  margin-bottom: 2.5rem;
}
.sv-home-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.375rem;
  color: #1a1a1a;
}
.sv-home-subtitle {
  color: #666;
  font-size: 0.95rem;
}

/* Loading */
.sv-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 5rem 0;
  color: #666;
}
.sv-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e0e0e0;
  border-top-color: #6c8fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Pagination */
.sv-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.sv-page-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1.1rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  color: #495057;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-page-btn:hover:not(:disabled) {
  background: #e9ecef;
  border-color: #6c8fff;
  color: #6c8fff;
}
.sv-page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sv-page-numbers {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.sv-page-num {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 1px solid #dee2e6;
  background: #fff;
  color: #6c757d;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-page-num:hover:not(.dots):not(.active) {
  background: #f8f9fa;
  color: #495057;
}
.sv-page-num.active {
  background: #6c8fff;
  border-color: #6c8fff;
  color: #fff;
  font-weight: 700;
}
.sv-page-num.dots {
  cursor: default;
  color: #adb5bd;
  background: transparent;
}

@media (max-width: 576px) {
  .sv-page-numbers {
    display: none;
  }
  .sv-home-title {
    font-size: 1.5rem;
  }
}

/* Error state */
.sv-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 4rem 1rem;
  color: #868e96;
  text-align: center;
  font-size: 0.95rem;
}
.sv-retry {
  padding: 0.5rem 1.25rem;
  background: #6c8fff;
  color: white;
  border: none;
  border-radius: 9999px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.2s;
}
.sv-retry:hover { background: #5a7aff; }
</style>
