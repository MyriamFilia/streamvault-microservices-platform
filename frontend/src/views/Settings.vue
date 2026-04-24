<template>
  <div class="sv-settings-page">
    <Navbar />
    <LoginModal />
    <RegisterModal />

    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
          
          <div class="sv-page-header">
            <h1 class="sv-page-title">⚙️ Settings</h1>
            <p class="sv-page-subtitle">Customize your StreamVault experience</p>
          </div>

          <transition name="sv-toast-anim">
            <div v-if="toast.show" class="sv-toast" :class="toast.type">
              {{ toast.message }}
            </div>
          </transition>

          <div class="sv-settings-content">
            
            <section class="sv-card">
              <h3 class="sv-card-title">App Preferences</h3>
              
              <div class="sv-setting-row">
                <div class="sv-setting-info">
                  <label class="sv-label">Language</label>
                  <p class="sv-setting-desc">Select your preferred interface language.</p>
                </div>
                <div class="sv-input-wrap sv-select-wrap">
                  <select v-model="settings.language" class="sv-input sv-select">
                    <option value="en">English</option>
                    <option value="fr">Français</option>
                    <option value="es">Español</option>
                  </select>
                </div>
              </div>

              <hr class="sv-divider" />

              <div class="sv-setting-row">
                <div class="sv-setting-info">
                  <label class="sv-label">Autoplay Trailers</label>
                  <p class="sv-setting-desc">Automatically play video trailers on the detail page.</p>
                </div>
                <label class="sv-toggle">
                  <input type="checkbox" v-model="settings.autoplay"/>
                  <span class="sv-toggle-slider"></span>
                </label>
              </div>
            </section>

            <section class="sv-card">
              <h3 class="sv-card-title">Notifications</h3>
              
              <div class="sv-setting-row">
                <div class="sv-setting-info">
                  <label class="sv-label">Email Newsletter</label>
                  <p class="sv-setting-desc">Receive weekly recommendations and platform updates.</p>
                </div>
                <label class="sv-toggle">
                  <input type="checkbox" v-model="settings.newsletter"/>
                  <span class="sv-toggle-slider"></span>
                </label>
              </div>

              <hr class="sv-divider" />

              <div class="sv-setting-row">
                <div class="sv-setting-info">
                  <label class="sv-label">New Episode Alerts</label>
                  <p class="sv-setting-desc">Get notified when a new episode of your favorite series airs.</p>
                </div>
                <label class="sv-toggle">
                  <input type="checkbox" v-model="settings.episodeAlerts"/>
                  <span class="sv-toggle-slider"></span>
                </label>
              </div>
            </section>

            <section class="sv-card">
              <h3 class="sv-card-title">Data & Privacy</h3>
              
              <div class="sv-setting-row">
                <div class="sv-setting-info">
                  <label class="sv-label">Clear Local Cache</label>
                  <p class="sv-setting-desc">Free up space by clearing locally saved search history and temporary images.</p>
                </div>
                <button class="sv-btn-ghost" @click="clearCache">Clear Cache</button>
              </div>
            </section>

            <div class="sv-save-container">
              <button class="sv-btn-save" @click="saveSettings" :disabled="isSaving">
                <span v-if="isSaving" class="sv-spinner"></span>
                <span v-else>💾 Save Preferences</span>
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginModal from "../components/LoginModal.vue";
import RegisterModal from "../components/RegisterModal.vue";

const router = useRouter();

// Toast Logic
const toast = ref({ show: false, message: "", type: "" });
const showToast = (message, type = "sv-toast-success") => {
  toast.value = { show: true, message, type };
  setTimeout(() => { toast.value.show = false; }, 3000);
};

// Settings State
const isSaving = ref(false);
const settings = ref({
  language: "en",
  autoplay: true,
  newsletter: false,
  episodeAlerts: true
});

// Load settings from LocalStorage
const loadSettings = () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/?login=required");
    return;
  }

  const savedSettings = localStorage.getItem("user_settings");
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings);
  }
};

// Save settings to LocalStorage
const saveSettings = () => {
  isSaving.value = true;
  
  // Simulation d'un appel réseau (UX)
  setTimeout(() => {
    localStorage.setItem("user_settings", JSON.stringify(settings.value));
    showToast("Settings saved successfully! ⚙️", "sv-toast-success");
    isSaving.value = false;
  }, 600);
};

// Clear Cache
const clearCache = () => {
  // On ne supprime que les préférences, pas le token ou les favoris
  localStorage.removeItem("user_settings");
  // Réinitialiser par défaut
  settings.value = {
    language: "en",
    autoplay: true,
    newsletter: false,
    episodeAlerts: true
  };
  showToast("Local cache cleared.", "sv-toast-info");
};

onMounted(() => {
  loadSettings();
});
</script>

<style scoped>
.sv-settings-page { min-height: 100vh; }

/* Header */
.sv-page-header { margin-bottom: 2.5rem; }
.sv-page-title { font-size: 2rem; font-weight: 800; color: #1a1a1a; margin: 0 0 0.5rem 0; }
.sv-page-subtitle { color: #868e96; font-size: 0.95rem; margin: 0; }

/* Content */
.sv-settings-content { display: flex; flex-direction: column; gap: 1.5rem; }

/* Cards */
.sv-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.sv-card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f3f5;
}

/* Rows */
.sv-setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}
.sv-setting-info { flex: 1; }
.sv-label {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 0.25rem;
}
.sv-setting-desc {
  font-size: 0.85rem;
  color: #868e96;
  margin: 0;
  line-height: 1.4;
}
.sv-divider { border-color: #f1f3f5; margin: 1.25rem 0; }

/* Select Input */
.sv-input-wrap {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  transition: 0.2s;
  min-width: 140px;
}
.sv-input-wrap:focus-within { border-color: #6c8fff; background: white; }
.sv-select {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #1a1a1a;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
}

/* Custom Toggle Switch */
.sv-toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
  flex-shrink: 0;
}
.sv-toggle input { opacity: 0; width: 0; height: 0; }
.sv-toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #dee2e6;
  transition: .3s;
  border-radius: 34px;
}
.sv-toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px; width: 18px;
  left: 4px; bottom: 4px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
input:checked + .sv-toggle-slider { background-color: #20c997; }
input:checked + .sv-toggle-slider:before { transform: translateX(22px); }

/* Buttons */
.sv-btn-ghost {
  padding: 0.5rem 1.2rem;
  background: transparent;
  color: #495057;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  transition: 0.2s;
  white-space: nowrap;
}
.sv-btn-ghost:hover { color: #1a1a1a; border-color: #adb5bd; background: #f8f9fa; }

.sv-save-container { display: flex; justify-content: flex-end; margin-top: 0.5rem; }
.sv-btn-save {
  padding: 0.75rem 2rem;
  background: #6c8fff;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 180px;
}
.sv-btn-save:hover:not(:disabled) { background: #5a7aff; }
.sv-btn-save:disabled { opacity: 0.7; cursor: not-allowed; }

/* Spinner */
.sv-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Toast */
.sv-toast {
  display: inline-flex;
  padding: 0.65rem 1.1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1050;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.sv-toast-success {
  background: rgba(25, 135, 84, 0.1);
  border: 1px solid rgba(25, 135, 84, 0.3);
  color: #146c43;
}
.sv-toast-info {
  background: rgba(108, 143, 255, 0.1);
  border: 1px solid rgba(108, 143, 255, 0.3);
  color: #5a7aff;
}
.sv-toast-anim-enter-active,
.sv-toast-anim-leave-active { transition: opacity 0.3s, transform 0.3s; }
.sv-toast-anim-enter-from,
.sv-toast-anim-leave-to { opacity: 0; transform: translateY(6px); }

/* Responsive */
@media (max-width: 576px) {
  .sv-setting-row { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
  .sv-input-wrap { width: 100%; }
  .sv-save-container { justify-content: stretch; }
  .sv-btn-save { width: 100%; }
}
</style>