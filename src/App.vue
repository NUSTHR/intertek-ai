<script setup lang="ts"></script>

<template>
  <div class="app">
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<style>
html,
body,
#app {
  height: 100%;
}

body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, 'Apple Color Emoji',
    'Segoe UI Emoji';
  background: #0b1220;
  color: #e6edf3;
}

a {
  color: inherit;
}

.app {
  min-height: 100%;
  display: flex;
}

.container {
  width: min(960px, calc(100% - 32px));
  margin: 0 auto;
  padding: 28px 0 48px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
