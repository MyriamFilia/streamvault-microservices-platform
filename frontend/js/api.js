const API_BASE_URL = "/api";

async function safeFetch(url) {
  const response = await fetch(`${API_BASE_URL}${url}`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  return response.json();
}