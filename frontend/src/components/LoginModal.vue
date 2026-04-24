<template>
  <div class="modal fade" id="loginModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered sv-modal-dialog">
      <div class="modal-content sv-modal">
        <div class="sv-modal-header">
          <div class="sv-modal-logo">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" />
              <path d="M8 21h8M12 17v4" />
              <polygon
                points="10,8 16,11 10,14"
                fill="currentColor"
                stroke="none" />
            </svg>
          </div>
          <h4 class="sv-modal-title">Welcome Back</h4>
          <p class="sv-modal-subtitle">Sign in to your StreamVault account</p>
          <button
            type="button"
            class="sv-modal-close"
            data-bs-dismiss="modal"
            aria-label="Close">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="sv-modal-body">
          <form @submit.prevent="handleLogin">
            <div v-if="errorMsg" class="sv-alert">
              {{ errorMsg }}
            </div>
            <div v-if="successMsg" class="sv-success">
              {{ successMsg }}
            </div>
            <div class="sv-field">
              <label class="sv-label"> Username </label>
              <div class="sv-input-wrap">
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
                  v-model="username"
                  type="text"
                  class="sv-input"
                  placeholder="Enter your username"
                  autocomplete="username"
                  required />
              </div>
            </div>
            <div class="sv-field">
              <label class="sv-label"> Password </label>
              <div class="sv-input-wrap">
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
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  class="sv-input"
                  placeholder="Enter your password"
                  autocomplete="current-password"
                  required />
                <button
                  type="button"
                  class="sv-eye"
                  @click="showPassword = !showPassword">
                  <svg
                    v-if="!showPassword"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8s-4 8-11 8s-11-8-11-8z" />
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
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20
                      c-7 0-11-8-11-8
                      a18.45 18.45 0 0 1 5.06-5.94" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
              </div>
            </div>
            <button type="submit" class="sv-submit" :disabled="loading">
              <span v-if="loading" class="sv-spinner"></span>
              <span v-else> Sign In </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { loginUser, getProfile } from "../services/auth";

const username = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMsg = ref("");
const successMsg = ref("");

const handleLogin = async () => {
  errorMsg.value = "";
  successMsg.value = "";
  loading.value = true;

  try {
    const response = await loginUser({
      username: username.value,
      password: password.value,
    });

    const token = response.data.access_token;
    localStorage.setItem("token", token);
    localStorage.setItem("username", username.value);

    try {
      const profile = await getProfile();
      localStorage.setItem("email", profile.data.email || "");
      localStorage.setItem("user_id", profile.data.id);
    } catch (e) {
      console.error("Profile fetch failed", e);
    }

    successMsg.value = "Login successful!";

    // Redirection propre sans utiliser le script Bootstrap
    setTimeout(() => {
      // Note : J'ai mis les bons chemins avec les tirets (my-reviews, etc.)
      const protectedPaths = ["/my-favorites", "/profile", "/my-reviews", "/settings"];
      const needsRedirect = protectedPaths.some(p => 
        window.location.pathname.startsWith(p)
      );
      
      if (needsRedirect) {
        window.location.href = "/";
      } else {
        window.location.reload();
      }
    }, 1200);

  } catch (error) {
    loading.value = false;
    errorMsg.value = error.response?.data?.detail || "Invalid username or password.";
  }
};
</script>

<style scoped>
.sv-modal-dialog {
  width: 100%;
  max-width: 460px; /* Parfait pour mobile */
}

@media (min-width: 768px) {
  .sv-modal-dialog {
    max-width: 550px;
  }
}
@media (min-width: 1200px) {
  .sv-modal-dialog {
    max-width: 650px;
  }
}

/* Modal */
.sv-modal {
  background: rgba(13, 15, 26, 0.97);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;
  overflow: hidden;
  color: white;
  backdrop-filter: blur(14px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

/* Header */
.sv-modal-header {
  position: relative;
  text-align: center;
  padding: 2.2rem 2rem 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.sv-modal-logo {
  width: 54px;
  height: 54px;
  margin: 0 auto 1rem;
  border-radius: 14px;
  background: rgba(108, 143, 255, 0.14);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c8fff;
}
.sv-modal-title {
  font-size: 1.45rem;
  font-weight: 700;
  margin: 0;
}
.sv-modal-subtitle {
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.92rem;
}
.sv-modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.06);
  border: none;
  border-radius: 10px;
  padding: 8px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}
.sv-modal-close:hover {
  background: rgba(255, 255, 255, 0.12);
  color: white;
}

/* Body */
.sv-modal-body {
  padding: 2rem;
}

/* Alerts */
.sv-alert,
.sv-success {
  border-radius: 12px;
  padding: 0.9rem 1rem;
  font-size: 0.9rem;
  margin-bottom: 1.2rem;
}
.sv-alert {
  background: rgba(220, 53, 69, 0.12);
  border: 1px solid rgba(220, 53, 69, 0.28);
  color: #ff6b7a;
}
.sv-success {
  background: rgba(25, 135, 84, 0.12);
  border: 1px solid rgba(25, 135, 84, 0.28);
  color: #7dffb2;
}

/* Fields */
.sv-field {
  margin-bottom: 1.2rem;
}
.sv-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.65);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.sv-input-wrap {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  transition: 0.2s;
}
.sv-input-wrap:focus-within {
  border-color: #6c8fff;
  background: rgba(108, 143, 255, 0.06);
}
.sv-input-icon {
  margin-left: 1rem;
  color: rgba(255, 255, 255, 0.35);
}
.sv-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: white;
  padding: 0.9rem;
  font-size: 0.95rem;
}
.sv-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.sv-eye {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  padding: 0 1rem;
  cursor: pointer;
}
.sv-eye:hover {
  color: white;
}

/* Submit */
.sv-submit {
  width: 100%;
  margin-top: 0.8rem;
  padding: 0.95rem;
  border: none;
  border-radius: 14px;
  background: #6c8fff;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: 0.2s;
}
.sv-submit:hover:not(:disabled) {
  background: #5a7aff;
}
.sv-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Spinner */
.sv-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
