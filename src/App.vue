<template>
  <div class="app">
    <header class="app-header">
      <h1 class="app-title">AI Questionnaire</h1>
    </header>
    <main class="app-main">
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
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, 'Apple Color Emoji', 'Segoe UI Emoji';
  line-height: 1.5;
  color: #111827;
  background: #ffffff;
}

.app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.app-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.app-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.app-main {
  width: min(960px, calc(100% - 32px));
  margin: 0 auto;
  padding: 16px 0 24px;
  flex: 1 1 auto;
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
