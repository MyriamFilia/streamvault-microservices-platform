document
  .getElementById("global-search-form")
  ?.addEventListener("submit", (e) => {
    e.preventDefault();

    const q = document
      .getElementById("global-search-input")
      .value
      .trim();

    if (!q) return;

    window.location.href = `search.html?q=${encodeURIComponent(q)}`;
});

function goToDetail(id) {
  window.location.href = `detail.html?id=${id}`;
}

function cleanHtml(html) {
  if (!html) return "Aucun résumé disponible.";

  return html.replace(/<[^>]+>/g, "").trim();
}

function createSeriesCard(show) {
  return `
    <div class="col-md-3">
      <div class="card h-100 shadow-sm"
        style="cursor:pointer"
        onclick="goToDetail(${show.id})">
        
        <img src="${show.image?.original || show.image?.medium|| 'https://picsum.photos/300/450'}",class="card-img-top">

        <div class="card-body">
          <h5>${show.name}</h5>
          <p>${show.language || ""}</p>
        </div>
      </div>
    </div>
  `;
}

function goToDetail(id) {
  window.location.href =
    `detail.html?id=${id}`;
}