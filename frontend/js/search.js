const params = new URLSearchParams(window.location.search);
const q = params.get("q");

let allSearchResults = [];
let currentSearchPage = 1;
const itemsPerPage = 12;

async function loadSearchResults() {
  const container = document.getElementById("search-results");

  try {
    const data = await safeFetch(
      `/series/search?q=${encodeURIComponent(q)}&page=${currentSearchPage}&limit=${itemsPerPage}`
    );

    allSearchResults = data.results.map(
      item => item.show || item
    );

    totalPages = data.total_pages;

    renderSearchPage();

  } catch (err) {
    container.innerHTML =
      `<p class="text-danger">${err.message}</p>`;
  }
}

function renderSearchPage() {
  const container = document.getElementById("search-results");
  const pagination = document.getElementById("search-pagination");

  const start = (currentSearchPage - 1) * itemsPerPage;
  const end = start + itemsPerPage;

  const showsToDisplay = allSearchResults.slice(start, end);

  container.innerHTML = showsToDisplay
    .map(show => createSeriesCard(show))
    .join("");

  const totalPages = Math.ceil(
    allSearchResults.length / itemsPerPage
  );

  pagination.innerHTML = `
    <button class="btn btn-outline-light"
      onclick="prevSearchPage()"
      ${currentSearchPage === 1 ? "disabled" : ""}>
      ← Previous
    </button>

    <span class="mx-3">
      Page ${currentSearchPage} / ${totalPages || 1}
    </span>

    <button class="btn btn-outline-light"
      onclick="nextSearchPage()"
      ${currentSearchPage === totalPages || totalPages === 0 ? "disabled" : ""}>
      Next →
    </button>
  `;
}

function nextSearchPage() {
  const totalPages = Math.ceil(
    allSearchResults.length / itemsPerPage
  );

  if (currentSearchPage < totalPages) {
    currentSearchPage++;
    renderSearchPage();

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
}

function prevSearchPage() {
  if (currentSearchPage > 1) {
    currentSearchPage--;
    renderSearchPage();

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
}

loadSearchResults();