<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* Global — fond blanc partout */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: #fafafa;  /* blanc cassé très léger */
  color: #1a1a1a;             /* noir pour le texte */
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f1f1; }
::-webkit-scrollbar-thumb { background: #c0c0c0; border-radius: 9999px; }
::-webkit-scrollbar-thumb:hover { background: #6c8fff; }
</style>