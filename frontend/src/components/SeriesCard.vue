<template>
  <div class="col-md-3 mb-4">
    <div
      class="card h-100 shadow-sm"
      style="cursor: pointer;"
      @click="goToDetail"
    >
      <img
        :src="getImage()"
        class="card-img-top"
        :alt="series.name || 'Série'"
      />

      <div class="card-body">
        <h5 class="card-title text-white">
          {{ series.name || "Titre indisponible" }}
        </h5>

        <p class="text-light small mb-1">
          {{ series.language || "Langue non disponible" }}
        </p>

        <p class="text-info small">
          ⭐ {{ getRating() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  series: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const fallbackImage =
  "https://picsum.photos/300/450";

const getImage = () => {
  return (
    props.series?.image?.original ||
    props.series?.image?.medium ||
    fallbackImage
  );
};

const getRating = () => {
  return (
    props.series?.rating?.average ||
    "N/A"
  );
};

const goToDetail = () => {
  if (!props.series?.id) return;

  router.push(`/detail/${props.series.id}`);
};
</script>

<style scoped>
.card {
  background-color: #11131d;
  border: 1px solid #262b3f;
  transition: transform 0.25s ease,
              box-shadow 0.25s ease;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

.card img {
  width: 100%;
  height: 380px;
  object-fit: cover;
  object-position: center;
}
</style>