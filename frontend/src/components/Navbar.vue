<template>
  <nav class="sv-navbar">
    <!-- LEFT -->
    <div class="sv-left">
      <!-- Logo -->
      <router-link to="/" class="sv-brand">
        <svg
          width="28"
          height="28"
          viewBox="0 0 32 32"
          fill="none"
          aria-label="StreamVault logo">
          <!-- Écran TV arrondi -->
          <rect
            x="2"
            y="4"
            width="28"
            height="18"
            rx="3"
            fill="#6c8fff"
            opacity="0.15" />
          <rect
            x="2"
            y="4"
            width="28"
            height="18"
            rx="3"
            stroke="#6c8fff"
            stroke-width="2" />
          <!-- Bouton play centré -->
          <polygon points="13,10 13,16 20,13" fill="#6c8fff" />
          <!-- Pied -->
          <path
            d="M11 22v3M21 22v3"
            stroke="#6c8fff"
            stroke-width="2"
            stroke-linecap="round" />
          <path
            d="M8 25h16"
            stroke="#6c8fff"
            stroke-width="2"
            stroke-linecap="round" />
          <!-- Petit point lumineux (indicateur on) -->
          <circle cx="26" cy="7" r="1.5" fill="#20c997" />
        </svg>

        <span class="sv-brand-text">StreamVault</span>
      </router-link>
      <span></span>
      <span></span>
      <span></span>

      <!-- Welcome -->
      <span v-if="username" class="sv-welcome">
        WELCOME BACK, {{ username }}
      </span>
    </div>

    <!-- SEARCH -->
    <form class="sv-search" @submit.prevent="handleSearch">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search for series..."
        aria-label="Search for series" />

      <button type="submit" aria-label="Search">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
      </button>
    </form>

    <!-- DESKTOP ACTIONS -->
    <div class="sv-actions">
      <template v-if="username">
        <div
          class="sv-profile-dropdown"
          @mouseenter="dropdownOpen = true"
          @mouseleave="dropdownOpen = false">
          <!-- Profile icon -->
          <button class="sv-profile-btn">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2">
              <circle cx="12" cy="8" r="4" />
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
            </svg>
          </button>

          <!-- Dropdown -->
          <div class="sv-dropdown-menu" :class="{ open: dropdownOpen }">
            <router-link to="/profile" class="sv-dropdown-item">
              👤 My Profile
            </router-link>

            <router-link to="/myfavorites" class="sv-dropdown-item">
              ❤️ My Favorites
            </router-link>

            <router-link to="/myreviews" class="sv-dropdown-item">
              ⭐ My Reviews
            </router-link>

            <router-link to="/settings" class="sv-dropdown-item">
              ⚙️ Settings
            </router-link>

            <button class="sv-dropdown-item danger" @click="logout">
              Logout
            </button>
          </div>
        </div>
      </template>

      <template v-else>
        <button
          class="sv-btn sv-btn-ghost"
          data-bs-toggle="modal"
          data-bs-target="#loginModal">
          Login
        </button>

        <button
          class="sv-btn sv-btn-primary"
          data-bs-toggle="modal"
          data-bs-target="#registerModal">
          Register
        </button>
      </template>
    </div>

    <!-- BURGER -->
    <button
      class="sv-burger"
      @click="menuOpen = !menuOpen"
      :aria-expanded="menuOpen"
      aria-label="Menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- MOBILE MENU -->
    <div class="sv-mobile-menu" :class="{ open: menuOpen }">
      <template v-if="username">
        <span class="sv-welcome-mobile"> WELCOME BACK, {{ username }} </span>

        <router-link
          to="/profile"
          class="sv-mobile-link"
          @click="menuOpen = false">
          👤 My Profile
        </router-link>

        <router-link
          to="/myfavorites"
          class="sv-mobile-link"
          @click="menuOpen = false">
          ❤️ My Favorites
        </router-link>

        <router-link
          to="/myreviews"
          class="sv-mobile-link"
          @click="menuOpen = false">
          ⭐ My Reviews
        </router-link>

        <router-link
          to="/settings"
          class="sv-mobile-link"
          @click="menuOpen = false">
          ⚙️ Settings
        </router-link>

        <button class="sv-btn sv-btn-danger w-100" @click="logout">
          Logout
        </button>
      </template>

      <template v-else>
        <button
          class="sv-btn sv-btn-ghost w-100"
          data-bs-toggle="modal"
          data-bs-target="#loginModal"
          @click="menuOpen = false">
          Login
        </button>

        <button
          class="sv-btn sv-btn-primary w-100"
          data-bs-toggle="modal"
          data-bs-target="#registerModal"
          @click="menuOpen = false">
          Register
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { logoutUser } from "../services/auth";

const router = useRouter();

const username = ref("");
const searchQuery = ref("");
const menuOpen = ref(false);
const dropdownOpen = ref(false);

const logout = async () => {
  try {
    await logoutUser(); // blacklist le token côté backend
  } catch {
    // token déjà expiré — on nettoie quand même
  } finally {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("email");
    menuOpen.value = false;
    dropdownOpen.value = false;
    router.push("/");
    window.location.reload();
  }
};

const handleSearch = () => {
  if (!searchQuery.value.trim()) return;

  router.push({
    path: "/search",
    query: {
      q: searchQuery.value,
    },
  });

  searchQuery.value = "";
};

onMounted(() => {
  username.value = localStorage.getItem("username") || "";
});
</script>

<style scoped>
/* NAVBAR */
.sv-navbar {
  position: sticky;
  top: 0;
  z-index: 1000;

  display: flex;
  align-items: center;
  gap: 1rem;

  padding: 0.9rem 1.5rem;

  background: rgba(10, 10, 15, 0.92);
  backdrop-filter: blur(12px);

  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

/* LEFT */
.sv-left {
  display: flex;
  align-items: center;
  gap: 1.8rem; /* plus éloigné */
}

/* BRAND */
.sv-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
}

.sv-brand svg {
  color: #6c8fff;
}

.sv-brand:hover {
  color: #6c8fff;
}

.sv-brand-text {
  white-space: nowrap;
}

/* WELCOME */
.sv-welcome {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.65);
  white-space: nowrap;
}

/* SEARCH */
.sv-search {
  display: flex;
  align-items: center;

  width: 280px;
  margin-left: auto;

  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;

  overflow: hidden;
  transition: 0.3s;
}

.sv-search:focus-within {
  width: 340px;
  border-color: #6c8fff;
}

.sv-search input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.55rem 1rem;
  color: white;
  font-size: 0.9rem;
}

.sv-search input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

.sv-search button {
  background: transparent;
  border: none;
  padding: 0 1rem;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.sv-search button:hover {
  color: #6c8fff;
}

/* ACTIONS */
.sv-actions {
  display: flex;
  align-items: center;
}

/* PROFILE */
.sv-profile-dropdown {
  position: relative;
}

.sv-profile-btn {
  width: 42px;
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.14);

  background: rgba(255, 255, 255, 0.05);
  color: white;

  cursor: pointer;
  transition: 0.2s;
}

.sv-profile-btn:hover {
  border-color: #6c8fff;
  color: #6c8fff;
}

/* DROPDOWN */
.sv-dropdown-menu {
  position: absolute;
  top: 55px;
  right: 0;

  min-width: 230px;

  background: #11131d;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;

  padding: 0.5rem;

  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);

  transition: 0.2s ease;

  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
}

.sv-dropdown-menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.sv-dropdown-item {
  display: block;
  width: 100%;

  padding: 0.85rem 1rem;
  border-radius: 10px;

  text-decoration: none;
  color: white;
  background: transparent;
  border: none;

  text-align: left;
  font-size: 0.92rem;
  cursor: pointer;

  transition: 0.2s;
}

.sv-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.sv-dropdown-item.danger {
  color: #ff6b7a;
}

/* BUTTONS */
.sv-btn {
  padding: 0.5rem 1rem;
  border-radius: 999px;
  border: none;
  cursor: pointer;
}

.sv-btn-primary {
  background: #6c8fff;
  color: white;
}

.sv-btn-ghost {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.sv-btn-danger {
  background: rgba(220, 53, 69, 0.15);
  color: #ff6b7a;
  border: 1px solid rgba(220, 53, 69, 0.25);
}

/* BURGER */
.sv-burger {
  display: none;
}

/* MOBILE */
.sv-mobile-menu {
  display: none;
}

.sv-mobile-menu.open {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;

  position: absolute;
  top: 100%;
  left: 0;
  right: 0;

  background: #0d0f1a;
  padding: 1rem 1.2rem;

  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sv-welcome-mobile {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.65);
}

.sv-mobile-link {
  color: white;
  text-decoration: none; /* pas souligné */
  padding: 0.25rem 0;
  font-weight: 500;
}

.sv-mobile-link:hover {
  color: #6c8fff;
}

.w-100 {
  width: 100%;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .sv-actions {
    display: none;
  }

  .sv-burger {
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: transparent;
    border: none;
    margin-left: 0.5rem;
    cursor: pointer;
  }

  .sv-burger span {
    width: 22px;
    height: 2px;
    background: white;
    border-radius: 2px;
  }

  .sv-welcome {
    display: none;
  }

  .sv-search {
    width: 150px;
  }

  .sv-search:focus-within {
    width: 200px;
  }
}

@media (max-width: 420px) {
  .sv-brand-text {
    display: none;
  }

  .sv-search {
    width: 120px;
  }

  .sv-search:focus-within {
    width: 150px;
  }
}
</style>
