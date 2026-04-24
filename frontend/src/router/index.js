import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import Search from "../views/Search.vue";
import Detail from "../views/Detail.vue";
import Favorites from "../views/Favorites.vue";
import Profile from "../views/Profile.vue";
import Reviews from "../views/Reviews.vue";
import Settings from "../views/Settings.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/search",
    name: "Search",
    component: Search
  },
  {
    path: "/detail/:id",
    name: "Detail",
    component: Detail
  },
  {
    path: "/myfavorites",
    name: "Favorites",
    component: Favorites,
    meta: { requiresAuth: true } // 🔒 
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { requiresAuth: true } // 🔒 
  },
  {
    path: "/myreviews",
    name: "Reviews",
    component: Reviews,
    meta: { requiresAuth: true } // 🔒 
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { requiresAuth: true } // 🔒
    }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token");
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/?login=required");
  } else {
    next();
  }
});

export default router;