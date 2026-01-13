<script setup lang="ts"></script>

<template>
  <div class="app">
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --bg-0: #070c16;
  --bg-1: #0b1324;
  --bg-2: #0f2037;

  --text: rgba(232, 240, 249, 0.92);
  --muted: rgba(232, 240, 249, 0.68);
  --subtle: rgba(232, 240, 249, 0.12);

  --accent: #d7b554;
  --accent-2: #f0d98b;
  --accent-ink: #1a1506;

  --card-bg: rgba(14, 23, 38, 0.72);
  --card-border: rgba(215, 181, 84, 0.18);
  --shadow: 0 14px 50px rgba(0, 0, 0, 0.45);
  --ring: 0 0 0 3px rgba(215, 181, 84, 0.22);
}

html,
body,
#app {
  height: 100%;
}

body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, 'Apple Color Emoji',
    'Segoe UI Emoji';
  color: var(--text);
  background: radial-gradient(900px 520px at 20% 10%, rgba(215, 181, 84, 0.18), transparent 55%),
    radial-gradient(900px 520px at 80% 20%, rgba(87, 125, 164, 0.22), transparent 60%),
    linear-gradient(140deg, var(--bg-0), var(--bg-1) 45%, var(--bg-2));
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
  padding: 38px 0 56px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.03)), var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 18px;
  padding: 22px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.title {
  margin: 0;
  font-size: 20px;
  letter-spacing: 0.2px;
  line-height: 1.35;
}

.subtitle {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

.bullets {
  margin: 0 0 18px;
  padding: 0 0 0 18px;
  color: rgba(232, 240, 249, 0.9);
  font-size: 14px;
  line-height: 1.7;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.btn {
  appearance: none;
  border-radius: 14px;
  cursor: pointer;
  border: 1px solid rgba(232, 240, 249, 0.14);
  color: var(--text);
  background: rgba(255, 255, 255, 0.06);
  font-size: 14px;
  padding: 10px 14px;
  transition: transform 120ms ease, background 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
}

.btn:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.btn:hover {
  background: rgba(255, 255, 255, 0.09);
  border-color: rgba(215, 181, 84, 0.32);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0px);
}

.btn-primary {
  background: linear-gradient(180deg, rgba(240, 217, 139, 0.96), rgba(215, 181, 84, 0.92));
  border-color: rgba(240, 217, 139, 0.44);
  color: var(--accent-ink);
  font-weight: 650;
  box-shadow: 0 12px 30px rgba(215, 181, 84, 0.24);
}

.btn-primary:hover {
  background: linear-gradient(180deg, rgba(250, 232, 166, 0.98), rgba(229, 197, 92, 0.95));
  border-color: rgba(240, 217, 139, 0.6);
}

.btn-ghost {
  background: transparent;
  border-color: rgba(232, 240, 249, 0.14);
  color: rgba(232, 240, 249, 0.78);
  font-size: 13px;
  padding: 8px 12px;
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(215, 181, 84, 0.26);
  color: var(--text);
}

.btn-option {
  min-width: 92px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.03));
  border-color: rgba(215, 181, 84, 0.18);
}

.muted {
  color: var(--muted);
}

.error {
  color: rgba(255, 210, 210, 0.95);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
