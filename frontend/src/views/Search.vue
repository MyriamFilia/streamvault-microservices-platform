<template>
  <div class="sv-search-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <div class="sv-search-header">
        <h1 class="sv-search-title">Search Results</h1>
        <p class="sv-search-subtitle">
          <template v-if="!loading && searchResults.length > 0">
            <strong>{{ searchResults.length }}</strong> results for
          </template>
          <template v-else>Results for</template>
          <span>"{{ route.query.q || "Series" }}"</span>
        </p>
      </div>

      <div v-if="loading" class="sv-loading">
        <div class="sv-spinner"></div>
        <span>Searching series...</span>
      </div>

      <div v-else-if="errorMsg" class="sv-error">
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
        <button class="sv-retry" @click="loadSearchResults">Retry</button>
      </div>

      <div v-else-if="searchResults.length === 0" class="sv-empty">
        <h3>No results found</h3>
        <p>Try another keyword or search for a different series.</p>
      </div>

      <div v-else class="row">
        <SeriesCard
          v-for="item in paginatedResults"
          :key="item.id"
          :series="item" />
      </div>

      <div v-if="totalPages > 1" class="sv-pagination">
        <button
          class="sv-page-btn"
          @click="prevPage"
          :disabled="currentPage === 1">
          ← Previous
        </button>

        <div class="sv-page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            class="sv-page-num"
            :class="{
              active: page === currentPage,
              dots: page === '...',
            }"
            @click="page !== '...' && goToPage(page)">
            {{ page }}
          </button>
        </div>

        <button
          class="sv-page-btn"
          @click="nextPage"
          :disabled="currentPage === totalPages">
          Next →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import SeriesCard from "../components/SeriesCard.vue";
import { searchSeries } from "../services/series";

const route = useRoute();

const searchResults = ref([]);
const loading = ref(true);
const errorMsg = ref(""); // ✅ AJOUT DE LA VARIABLE MANQUANTE
const currentPage = ref(1);
const itemsPerPage = 12;

/* Pagination */
const paginatedResults = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return searchResults.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() =>
  Math.ceil(searchResults.value.length / itemsPerPage),
);

const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }
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

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    goToPage(currentPage.value + 1);
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    goToPage(currentPage.value - 1);
  }
};

/* Load search */
const loadSearchResults = async () => {
  const query = route.query.q?.trim();
  if (!query) {
    searchResults.value = [];
    loading.value = false;
    return;
  }
  loading.value = true;
  errorMsg.value = "";
  currentPage.value = 1;

  try {
    const response = await searchSeries(query);
    const raw = Array.isArray(response.data)
      ? response.data
      : response.data.results || response.data.data || [];
    
    // Normalise : TVMaze search renvoie [{score, show}] ou directement [show]
    searchResults.value = raw.map((item) => item.show || item);
  } catch (error) {
    console.error(error);
    errorMsg.value = "Search failed. Please try again.";
    searchResults.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadSearchResults();
});

watch(
  () => route.query.q,
  () => {
    loadSearchResults();
  },
);
</script>

<style scoped>
/* Les styles sont parfaits, je n'ai rien touché */
.sv-search-page {
  min-height: 100vh;
}

.sv-search-header {
  margin-bottom: 2.5rem;
}

.sv-search-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 0.4rem;
}

.sv-search-subtitle {
  color: #666;
  font-size: 0.95rem;
}

.sv-search-subtitle span {
  color: #6c8fff;
  font-weight: 600;
}

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

.sv-empty {
  text-align: center;
  padding: 5rem 0;
}

.sv-empty h3 {
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.sv-empty p {
  color: #666;
}

.sv-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.sv-page-btn {
  padding: 0.6rem 1.1rem;
  border: 1px solid #dee2e6;
  background: #f8f9fa;
  border-radius: 10px;
  color: #495057;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s;
}

.sv-page-btn:hover:not(:disabled) {
  border-color: #6c8fff;
  color: #6c8fff;
}

.sv-page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sv-page-numbers {
  display: flex;
  gap: 0.4rem;
}

.sv-page-num {
  width: 38px;
  height: 38px;
  border: 1px solid #dee2e6;
  background: white;
  border-radius: 8px;
  color: #6c757d;
  cursor: pointer;
  transition: 0.2s;
  font-weight: 500;
}

.sv-page-num.active {
  background: #6c8fff;
  border-color: #6c8fff;
  color: white;
  font-weight: 700;
}

.sv-page-num.dots {
  cursor: default;
  background: transparent;
  border: none;
}

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

@media (max-width: 576px) {
  .sv-page-numbers {
    display: none;
  }

  .sv-search-title {
    font-size: 1.5rem;
  }
}
</style>