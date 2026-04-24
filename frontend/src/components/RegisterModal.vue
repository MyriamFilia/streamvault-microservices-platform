<template>
  <div class="modal fade" id="registerModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered sv-modal-dialog">
      <div class="modal-content sv-modal">
        <!-- Header -->
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
          <h4 class="sv-modal-title">Create Account</h4>
          <p class="sv-modal-subtitle">Join StreamVault today</p>
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

        <!-- Body -->
        <div class="sv-modal-body">
          <form @submit.prevent="handleRegister">
            <div v-if="errorMsg" class="sv-alert">{{ errorMsg }}</div>
            <div v-if="successMsg" class="sv-success">{{ successMsg }}</div>

            <!-- Username -->
            <div class="sv-field">
              <label class="sv-label">Username</label>
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
                  placeholder="Choose a username"
                  autocomplete="username"
                  required />
              </div>
            </div>

            <!-- Email -->
            <div class="sv-field">
              <label class="sv-label">Email</label>
              <div class="sv-input-wrap">
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
                  v-model="email"
                  type="email"
                  class="sv-input"
                  placeholder="Enter your email"
                  autocomplete="email"
                  required />
              </div>
            </div>

            <!-- Password -->
            <div class="sv-field">
              <label class="sv-label">Password</label>
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
                  placeholder="Create a password"
                  autocomplete="new-password"
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
            </div>

            <!-- Confirm Password -->
            <div class="sv-field">
              <label class="sv-label">Confirm Password</label>
              <div
                class="sv-input-wrap"
                :class="{ 'sv-input-error': passwordMismatch }">
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
                  :type="showConfirm ? 'text' : 'password'"
                  class="sv-input"
                  placeholder="Repeat your password"
                  autocomplete="new-password"
                  required />
                <button
                  type="button"
                  class="sv-eye"
                  @click="showConfirm = !showConfirm">
                  <svg
                    v-if="!showConfirm"
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
              <p v-if="passwordMismatch" class="sv-field-error">
                Passwords do not match
              </p>
            </div>

            <button
              type="submit"
              class="sv-submit"
              :disabled="loading || passwordMismatch">
              <span v-if="loading" class="sv-spinner"></span>
              <span v-else>Create Account</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { registerUser } from "../services/auth";

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirm = ref(false);
const loading = ref(false);
const errorMsg = ref("");
const successMsg = ref("");

// Vrai seulement si l'utilisateur a commencé à taper dans confirm
const passwordMismatch = computed(
  () =>
    confirmPassword.value.length > 0 &&
    password.value !== confirmPassword.value,
);

const resetForm = () => {
  username.value = "";
  email.value = "";
  password.value = "";
  confirmPassword.value = "";
};

const handleRegister = async () => {
  errorMsg.value = "";
  successMsg.value = "";

  // Validation simple
  if (!username.value.trim()) {
    errorMsg.value = "Username is required.";
    return;
  }

  if (!email.value.trim()) {
    errorMsg.value = "Email is required.";
    return;
  }

  if (!password.value.trim()) {
    errorMsg.value = "Password is required.";
    return;
  }

  if (password.value.length < 6) {
    errorMsg.value = "Password must be at least 6 characters.";
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMsg.value = "Passwords do not match.";
    return;
  }

  loading.value = true;

  try {
    await registerUser({
      username: username.value,
      email: email.value,
      password: password.value,
    });

    successMsg.value =
      "Account created successfully! Please login.";

    resetForm();
    setTimeout(() => window.location.reload(), 1200);
  } catch (error) {
    errorMsg.value =
      error.response?.data?.detail || "Registration failed. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.sv-modal-dialog {
  width: 100%;
  max-width: 460px;
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

.sv-modal {
  background: rgba(13, 15, 26, 0.97);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;
  overflow: hidden;
  color: white;
  backdrop-filter: blur(14px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

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
  display: flex;
  transition: all 0.2s;
}
.sv-modal-close:hover {
  background: rgba(255, 255, 255, 0.12);
  color: white;
}

.sv-modal-body {
  padding: 2rem;
}

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
  transition:
    border-color 0.2s,
    background 0.2s;
}
.sv-input-wrap:focus-within {
  border-color: #6c8fff;
  background: rgba(108, 143, 255, 0.06);
}
.sv-input-error {
  border-color: rgba(220, 53, 69, 0.6) !important;
  background: rgba(220, 53, 69, 0.04) !important;
}
.sv-input-icon {
  flex-shrink: 0;
  margin-left: 1rem;
  color: rgba(255, 255, 255, 0.35);
}
.sv-input {
  flex: 1;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
  caret-color: #6c8fff;
  padding: 0.9rem;
  font-size: 0.95rem;
}
.sv-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.sv-input:-webkit-autofill,
.sv-input:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0px 1000px rgba(13, 15, 26, 0.97) inset !important;
  -webkit-text-fill-color: #ffffff !important;
}

.sv-eye {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  padding: 0 1rem;
  cursor: pointer;
  display: flex;
  transition: color 0.2s;
}
.sv-eye:hover {
  color: #fff;
}

.sv-field-error {
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: #ff6b7a;
}

.sv-submit {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.95rem;
  border: none;
  border-radius: 14px;
  background: #6c8fff;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sv-submit:hover:not(:disabled) {
  background: #5a7aff;
}
.sv-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.sv-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
