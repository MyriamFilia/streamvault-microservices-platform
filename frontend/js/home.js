let allPopularShows = [];
let currentPage = 1;
const itemsPerPage = 12;

async function loadPopularSeries() {
  const container = document.getElementById("popular-series");

  try {
    const data = await safeFetch("/series/popular");

    // route popular renvoie directement des shows
    allPopularShows = data.results || [];

    renderPopularPage();

  } catch (err) {
    container.innerHTML =
      `<p class="text-danger">${err.message}</p>`;
  }
}

function renderPopularPage() {
  const container = document.getElementById("popular-series");
  const pagination = document.getElementById("pagination");

  const start = (currentPage - 1) * itemsPerPage;
  const end = start + itemsPerPage;

  const showsToDisplay = allPopularShows.slice(start, end);

  container.innerHTML = showsToDisplay
    .map(show => createSeriesCard(show))
    .join("");

  const totalPages = Math.ceil(
    allPopularShows.length / itemsPerPage
  );

  pagination.innerHTML = `
    <button class="btn btn-outline-light"
      onclick="prevPage()"
      ${currentPage === 1 ? "disabled" : ""}>
      ← Previous
    </button>

    <span class="mx-3">
      Page ${currentPage} / ${totalPages}
    </span>

    <button class="btn btn-outline-light"
      onclick="nextPage()"
      ${currentPage === totalPages ? "disabled" : ""}>
      Next →
    </button>
  `;
}

function nextPage() {
  const totalPages = Math.ceil(
    allPopularShows.length / itemsPerPage
  );

  if (currentPage < totalPages) {
    currentPage++;
    renderPopularPage();

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    renderPopularPage();

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
}

loadPopularSeries();