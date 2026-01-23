<template>
  <router-view />
</template>

<style>
html,
body,
#app {
  height: 100%;
}

body {
  margin: 0;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 16px;
  background: #ffffff;
}

.field {
  display: block;
  margin: 10px 0;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.muted {
  color: #6b7280;
}

.error {
  color: #b91c1c;
}
</style>
