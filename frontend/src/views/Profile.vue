<template>
  <div class="sv-profile-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <div class="sv-profile-layout">
        <!-- Sidebar -->
        <aside class="sv-sidebar">
          <div class="sv-avatar-block">
            <div class="sv-avatar-lg">{{ avatarLetter }}</div>
            <h2 class="sv-sidebar-name">{{ username }}</h2>
            <p class="sv-sidebar-email">{{ currentEmail || "No email set" }}</p>
          </div>

          <div class="sv-sidebar-stats">
            <router-link to="/myfavorites" class="sv-stat sv-stat-link">
              <span class="sv-stat-value">{{ favoritesCount }}</span>
              <span class="sv-stat-label">Favorites</span>
            </router-link>

            <div class="sv-stat-divider"></div>

            <router-link to="/myreviews" class="sv-stat sv-stat-link">
              <span class="sv-stat-value">{{ reviewsCount }}</span>
              <span class="sv-stat-label">Reviews</span>
            </router-link>
          </div>

          <button class="sv-btn-logout" @click="logout">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Sign Out
          </button>
        </aside>

        <!-- Main -->
        <main class="sv-main">
          <!-- Toast -->
          <transition name="sv-toast-anim">
            <div v-if="toast.show" class="sv-toast" :class="toast.type">
              {{ toast.message }}
            </div>
          </transition>

          <!-- ── Section 1 : Account Info ── -->
          <section class="sv-card">
            <h3 class="sv-card-title">
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
              Account Information
            </h3>

            <!-- Username readonly -->
            <div class="sv-field">
              <label class="sv-label">Username</label>
              <div class="sv-input-wrap sv-input-disabled">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <circle cx="12" cy="8" r="4" />
                  <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
                </svg>
                <input
                  type="text"
                  class="sv-input"
                  :value="username"
                  disabled />
                <span class="sv-input-badge">Fixed</span>
              </div>
              <p class="sv-field-hint">Your username cannot be changed.</p>
            </div>

            <!-- Current email readonly -->
            <div class="sv-field">
              <label class="sv-label">Current Email</label>
              <div class="sv-input-wrap sv-input-disabled">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <rect x="2" y="4" width="20" height="16" rx="2" />
                  <path d="M2 7l10 7 10-7" />
                </svg>
                <input
                  type="email"
                  class="sv-input"
                  :value="currentEmail || 'Not set'"
                  disabled />
                <span class="sv-input-badge">Current</span>
              </div>
            </div>

            <!-- New email -->
            <div class="sv-field">
              <label class="sv-label">New Email</label>
              <div
                class="sv-input-wrap"
                :class="{ 'sv-input-error': errors.email }">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <rect x="2" y="4" width="20" height="16" rx="2" />
                  <path d="M2 7l10 7 10-7" />
                </svg>
                <input
                  v-model="newEmail"
                  type="email"
                  class="sv-input"
                  placeholder="Enter new email address"
                  @input="errors.email = ''" />
              </div>
              <p v-if="errors.email" class="sv-field-error">
                ⚠️ {{ errors.email }}
              </p>
              <p
                v-else-if="newEmail && newEmail === currentEmail"
                class="sv-field-warning">
                ⚠️ This is already your current email.
              </p>
              <p
                v-else-if="newEmail && isValidEmail(newEmail)"
                class="sv-field-success">
                ✓ Valid email address
              </p>
            </div>

            <button
              class="sv-btn-save"
              @click="updateEmail"
              :disabled="
                savingEmail ||
                !newEmail ||
                newEmail === currentEmail ||
                !isValidEmail(newEmail)
              ">
              <span v-if="savingEmail" class="sv-spinner"></span>
              <span v-else>Update Email</span>
            </button>
          </section>

          <!-- ── Section 2 : Change Password ── -->
          <section class="sv-card">
            <h3 class="sv-card-title">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              Change Password
            </h3>

            <!-- Current password -->
            <div class="sv-field">
              <label class="sv-label">Current Password</label>
              <div
                class="sv-input-wrap"
                :class="{ 'sv-input-error': errors.currentPassword }">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  v-model="currentPassword"
                  :type="showCurrentPwd ? 'text' : 'password'"
                  class="sv-input"
                  placeholder="Your current password"
                  @input="errors.currentPassword = ''" />
                <button
                  type="button"
                  class="sv-eye"
                  @click="showCurrentPwd = !showCurrentPwd">
                  <svg
                    v-if="!showCurrentPwd"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  <svg
                    v-else
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
              </div>
              <p v-if="errors.currentPassword" class="sv-field-error">
                ⚠️ {{ errors.currentPassword }}
              </p>
            </div>

            <!-- New password -->
            <div class="sv-field">
              <label class="sv-label">New Password</label>
              <div
                class="sv-input-wrap"
                :class="{ 'sv-input-error': errors.password }">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  v-model="newPassword"
                  :type="showNewPwd ? 'text' : 'password'"
                  class="sv-input"
                  placeholder="At least 6 characters"
                  @input="errors.password = ''" />
                <button
                  type="button"
                  class="sv-eye"
                  @click="showNewPwd = !showNewPwd">
                  <svg
                    v-if="!showNewPwd"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  <svg
                    v-else
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
              </div>
              <!-- Barre de force du mot de passe -->
              <div v-if="newPassword" class="sv-strength-bar">
                <div class="sv-strength-track">
                  <div
                    class="sv-strength-fill"
                    :class="strengthClass"
                    :style="{ width: strengthWidth }"></div>
                </div>
                <span class="sv-strength-label" :class="strengthClass">{{
                  strengthLabel
                }}</span>
              </div>
              <p v-if="errors.password" class="sv-field-error">
                ⚠️ {{ errors.password }}
              </p>
            </div>

            <!-- Confirm new password -->
            <div class="sv-field">
              <label class="sv-label">Confirm New Password</label>
              <div
                class="sv-input-wrap"
                :class="{ 'sv-input-error': errors.confirm }">
                <svg
                  class="sv-input-icon"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  v-model="confirmPassword"
                  :type="showConfirmPwd ? 'text' : 'password'"
                  class="sv-input"
                  placeholder="Repeat new password"
                  @input="errors.confirm = ''" />
                <button
                  type="button"
                  class="sv-eye"
                  @click="showConfirmPwd = !showConfirmPwd">
                  <svg
                    v-if="!showConfirmPwd"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  <svg
                    v-else
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
              </div>
              <p v-if="errors.confirm" class="sv-field-error">
                ⚠️ {{ errors.confirm }}
              </p>
              <p
                v-else-if="confirmPassword && confirmPassword === newPassword"
                class="sv-field-success">
                ✓ Passwords match
              </p>
            </div>

            <button
              class="sv-btn-save"
              @click="updatePassword"
              :disabled="
                savingPassword ||
                !currentPassword ||
                !newPassword ||
                !confirmPassword
              ">
              <span v-if="savingPassword" class="sv-spinner"></span>
              <span v-else>Update Password</span>
            </button>
          </section>

          <!-- ── Danger Zone ── -->
          <section class="sv-card sv-card-danger">
            <h3 class="sv-card-title sv-danger-title">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2">
                <path
                  d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
              Danger Zone
            </h3>
            <p class="sv-danger-text">
              Deleting your account is permanent and cannot be undone. All your
              reviews and favorites will be lost.
            </p>
            <button class="sv-btn-danger" @click="deleteAccount">
              Delete My Account
            </button>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";
import {
  getProfile,
  updateProfile,
  logoutUser,
  deleteUser,
} from "../services/auth";
import { getMyReviews } from "../services/reviews";
import { getMyFavorites } from "../services/favorites";

const router = useRouter();

// ── State ──────────────────────────────────────────
const username = ref("");
const currentEmail = ref("");
const newEmail = ref("");

const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

const showCurrentPwd = ref(false);
const showNewPwd = ref(false);
const showConfirmPwd = ref(false);

const savingEmail = ref(false);
const savingPassword = ref(false);

const errors = ref({
  email: "",
  currentPassword: "",
  password: "",
  confirm: "",
});

const toast = ref({ show: false, message: "", type: "" });

// ── Toast ──────────────────────────────────────────
const showToast = (message, type = "sv-toast-success") => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3500);
};

// ── Computed ───────────────────────────────────────
const avatarLetter = computed(() =>
  username.value ? username.value.charAt(0).toUpperCase() : "?",
);

const favoritesCount = ref(0);
const reviewsCount = ref(0);

const loadCounts = async () => {
  try {
    const [favsRes, reviewsRes] = await Promise.all([
      getMyFavorites(),
      getMyReviews(),
    ]);
    favoritesCount.value = favsRes.data?.length || 0;
    reviewsCount.value = reviewsRes.data?.length || 0;
  } catch {
    // silencieux — les compteurs restent à 0
  }
};

// Force du mot de passe
const passwordStrength = computed(() => {
  const p = newPassword.value;
  if (!p) return 0;
  let score = 0;
  if (p.length >= 6) score++;
  if (p.length >= 10) score++;
  if (/[A-Z]/.test(p)) score++;
  if (/[0-9]/.test(p)) score++;
  if (/[^A-Za-z0-9]/.test(p)) score++;
  return score;
});
const strengthWidth = computed(() => {
  return `${(passwordStrength.value / 5) * 100}%`;
});
const strengthLabel = computed(() => {
  const s = passwordStrength.value;
  if (s <= 1) return "Weak";
  if (s <= 2) return "Fair";
  if (s <= 3) return "Good";
  if (s <= 4) return "Strong";
  return "Very Strong";
});
const strengthClass = computed(() => {
  const s = passwordStrength.value;
  if (s <= 1) return "strength-weak";
  if (s <= 2) return "strength-fair";
  if (s <= 3) return "strength-good";
  if (s <= 4) return "strength-strong";
  return "strength-vstrong";
});

// ── Helpers ────────────────────────────────────────
const isValidEmail = (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);

// ── Load ───────────────────────────────────────────
const loadProfile = async () => {
  try {
    const res = await getProfile();
    const user = res.data;
    username.value = user.username || "";
    currentEmail.value = user.email || "";
    localStorage.setItem("username", user.username || "");
    localStorage.setItem("email", user.email || "");
  } catch (error) {
    console.error("Error loading profile:", error);
    // fallback localStorage si API indisponible
    username.value = localStorage.getItem("username") || "";
    currentEmail.value = localStorage.getItem("email") || "";
  }
};

// ── Update email ───────────────────────────────────
const updateEmail = async () => {
  errors.value.email = "";

  if (!newEmail.value) {
    errors.value.email = "Email is required.";
    return;
  }

  if (!isValidEmail(newEmail.value)) {
    errors.value.email = "Please enter a valid email address.";
    return;
  }

  if (newEmail.value === currentEmail.value) {
    errors.value.email = "This is already your current email.";
    return;
  }

  savingEmail.value = true;

  try {
    await updateProfile({
      email: newEmail.value,
    });

    currentEmail.value = newEmail.value;
    localStorage.setItem("email", currentEmail.value);
    newEmail.value = "";
    showToast("Email updated successfully ✅");
  } catch (error) {
    errors.value.email =
      error.response?.data?.detail || "Failed to update email.";
  } finally {
    savingEmail.value = false;
  }
};

// ── Update password ────────────────────────────────
const updatePassword = async () => {
  errors.value.currentPassword = "";
  errors.value.password = "";
  errors.value.confirm = "";

  if (!currentPassword.value) {
    errors.value.currentPassword = "Please enter your current password.";
    return;
  }

  if (!newPassword.value) {
    errors.value.password = "New password is required.";
    return;
  }

  if (newPassword.value.length < 6) {
    errors.value.password = "Password must be at least 6 characters.";
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    errors.value.confirm = "Passwords do not match.";
    return;
  }

  savingPassword.value = true;

  try {
    await updateProfile({
      password: newPassword.value,
    });

    currentPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";

    showToast("Password updated successfully 🔒");
  } catch (error) {
    errors.value.password =
      error.response?.data?.detail || "Failed to update password.";
  } finally {
    savingPassword.value = false;
  }
};

// ── Logout ─────────────────────────────────────────
const logout = async () => {
  try {
    await logoutUser();
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("email");

    router.push("/");
  }
};

// ── Delete account ─────────────────────────────────
const deleteAccount = async () => {
  if (!confirm("Are you sure? This action is permanent and cannot be undone."))
    return;
  try {
    await deleteUser();

    localStorage.clear();
    showToast("Account deleted", "sv-toast-danger");
    router.push("/");
  } catch (error) {
    showToast(
      error.response?.data?.detail || "Failed to delete account.",
      "sv-toast-danger",
    );
  }
};

onMounted(async () => {
  await loadProfile();
  await loadCounts();
});
</script>

<style scoped>
.sv-profile-page {
  min-height: 100vh;
}

/* Layout */
.sv-profile-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2rem;
  align-items: start;
}
@media (max-width: 768px) {
  .sv-profile-layout {
    grid-template-columns: 1fr;
  }
}

/* ── Sidebar ── */
.sv-sidebar {
  background: rgba(13, 15, 26, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.25rem;
  position: sticky;
  top: 1.5rem;
  backdrop-filter: blur(14px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}
.sv-avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.sv-avatar-lg {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(108, 143, 255, 0.14);
  color: #6c8fff;
  font-size: 2rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sv-sidebar-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
  margin: 0;
}
.sv-sidebar-email {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.55);
  margin: 0;
  word-break: break-all;
}

.sv-sidebar-stats {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  width: 100%;
  justify-content: center;
  padding: 1rem 0;
  border-top: 1px solid #f1f3f5;
  border-bottom: 1px solid #f1f3f5;
}
.sv-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}
.sv-stat-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1a1a1a;
}
.sv-stat-label {
  font-size: 0.75rem;
  color: #868e96;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.sv-stat-divider {
  width: 1px;
  height: 36px;
  background: #e9ecef;
}

.sv-stat-link {
  text-decoration: none;
  transition: all 0.2s ease;
  padding: 0.5rem 1rem;
  border-radius: 14px;
}

.sv-stat-link:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}

.sv-stat-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: white;
}

.sv-stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.55);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.sv-stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(255, 255, 255, 0.08);
}

.sv-btn-logout {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  justify-content: center;
  padding: 0.6rem 1rem;
  background: transparent;
  color: #868e96;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-logout:hover {
  color: #dc3545;
  border-color: rgba(220, 53, 69, 0.3);
  background: rgba(220, 53, 69, 0.05);
}

/* ── Main ── */
.sv-main {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Toast */
.sv-toast {
  display: inline-flex;
  padding: 0.65rem 1.1rem;
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

/* Cards */
.sv-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 18px;
  padding: 1.75rem;
}
.sv-card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1.5rem;
}

/* Fields */
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
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  transition:
    border-color 0.2s,
    background 0.2s;
}
.sv-input-wrap:focus-within {
  border-color: #6c8fff;
  background: #fff;
}
.sv-input-disabled {
  background: #f1f3f5 !important;
}
.sv-input-error {
  border-color: rgba(220, 53, 69, 0.5) !important;
  background: rgba(220, 53, 69, 0.02) !important;
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
.sv-input:disabled {
  color: #868e96;
  cursor: not-allowed;
}
.sv-input::placeholder {
  color: #adb5bd;
}
.sv-input-badge {
  margin-right: 0.875rem;
  font-size: 0.72rem;
  font-weight: 600;
  color: #868e96;
  background: #e9ecef;
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
  white-space: nowrap;
}
.sv-eye {
  background: transparent;
  border: none;
  color: #adb5bd;
  padding: 0 1rem;
  cursor: pointer;
  display: flex;
  transition: color 0.2s;
}
.sv-eye:hover {
  color: #495057;
}

/* Feedback sous champs */
.sv-field-hint {
  font-size: 0.78rem;
  color: #adb5bd;
  margin-top: 0.35rem;
}
.sv-field-error {
  font-size: 0.8rem;
  color: #dc3545;
  margin-top: 0.35rem;
}
.sv-field-warning {
  font-size: 0.8rem;
  color: #b8860b;
  margin-top: 0.35rem;
}
.sv-field-success {
  font-size: 0.8rem;
  color: #146c43;
  margin-top: 0.35rem;
}

/* Password strength bar */
.sv-strength-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.sv-strength-track {
  flex: 1;
  height: 5px;
  background: #e9ecef;
  border-radius: 9999px;
  overflow: hidden;
}
.sv-strength-fill {
  height: 100%;
  border-radius: 9999px;
  transition:
    width 0.3s,
    background 0.3s;
}
.sv-strength-label {
  font-size: 0.78rem;
  font-weight: 600;
  white-space: nowrap;
}

.strength-weak .sv-strength-fill,
.sv-strength-fill.strength-weak {
  background: #dc3545;
}
.strength-fair .sv-strength-fill,
.sv-strength-fill.strength-fair {
  background: #fd7e14;
}
.strength-good .sv-strength-fill,
.sv-strength-fill.strength-good {
  background: #ffc107;
}
.strength-strong .sv-strength-fill,
.sv-strength-fill.strength-strong {
  background: #20c997;
}
.strength-vstrong .sv-strength-fill,
.sv-strength-fill.strength-vstrong {
  background: #198754;
}

.strength-weak {
  color: #dc3545;
}
.strength-fair {
  color: #fd7e14;
}
.strength-good {
  color: #b8860b;
}
.strength-strong {
  color: #0d9488;
}
.strength-vstrong {
  color: #146c43;
}

/* Save button */
.sv-btn-save {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.65rem 1.5rem;
  background: #6c8fff;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
  min-width: 150px;
  margin-top: 0.25rem;
}
.sv-btn-save:hover:not(:disabled) {
  background: #5a7aff;
}
.sv-btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Spinner */
.sv-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Danger zone */
.sv-card-danger {
  border-color: rgba(220, 53, 69, 0.2);
  background: rgba(220, 53, 69, 0.02);
}
.sv-danger-title {
  color: #dc3545 !important;
}
.sv-danger-text {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 1.25rem;
  max-width: 60ch;
}
.sv-btn-danger {
  padding: 0.6rem 1.25rem;
  background: transparent;
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.4);
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.sv-btn-danger:hover {
  background: #dc3545;
  color: #fff;
}
</style>
