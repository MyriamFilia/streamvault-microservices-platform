const params = new URLSearchParams(window.location.search);
const id = params.get("id");

function cleanHtml(html) {
  if (!html || html === "null" || html === "undefined") {
    return "No summary available.";
  }

  return html.replace(/<[^>]+>/g, "").trim();
}

async function safeFetch(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}

async function loadDetail() {
  const container = document.getElementById("series-detail");

  container.innerHTML = `
    <div class="text-center text-secondary">
      Chargement des détails...
    </div>
  `;

  try {
    const show = await safeFetch(
      `http://localhost:8000/series/${id}`
    );

    const imageUrl =
      show.image?.original ||
      show.image?.medium ||
      "https://dummyimage.com/500x750/111/fff&text=No+Image";

    const name = show.name || "No title";

    const summary = cleanHtml(show.summary);

    const language = show.language || "No language";

    const premiered = show.premiered || "No date";

    const genres =
      show.genres && show.genres.length > 0
        ? show.genres.join(", ")
        : "No genre";

    const status = show.status || "Unknown";

    const rating =
      show.rating?.average || "No rating";

    container.innerHTML = `
      <div class="row g-4 align-items-start">

        <div class="col-md-4">
          <img
            src="${imageUrl}"
            alt="${name}"
            class="img-fluid rounded shadow detail-poster"
          >
        </div>

        <div class="col-md-8">
          <h1 class="mb-3">${name}</h1>

          <p class="text-light mb-4">
            ${summary}
          </p>

          <div class="row">
            <div class="col-md-6">
              <p><strong>Language:</strong> ${language}</p>
              <p><strong>Premiered:</strong> ${premiered}</p>
            </div>

            <div class="col-md-6">
              <p><strong>Genres:</strong> ${genres}</p>
              <p><strong>Status:</strong> ${status}</p>
              <p><strong>Rating:</strong> ⭐ ${rating}</p>
            </div>
          </div>

          <a href="index.html" class="btn btn-outline-light mt-3">
            ← Retour à l'accueil
          </a>
        </div>
      </div>
    `;

  } catch (error) {
    container.innerHTML = `
      <div class="alert alert-danger">
        Impossible de charger les détails.
      </div>
    `;
  }
}

loadDetail();