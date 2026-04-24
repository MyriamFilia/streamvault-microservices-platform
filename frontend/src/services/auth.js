import { userApi } from "./api";

// POST /users/register
export const registerUser = (userData) =>
  userApi.post("/register", userData);

// POST /users/login
export const loginUser = (credentials) =>
  userApi.post("/login", credentials);

// GET /users/me
export const getProfile = () =>
  userApi.get("/me");

// PUT /users/me — email et/ou password
export const updateProfile = (updates) =>
  userApi.put("/me", updates);

// POST /users/logout
export const logoutUser = () =>
  userApi.post("/logout");

// DELETE /users/me
export const deleteUser = () =>
  userApi.delete("/me");