<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import intertekLogo from '@/assets/images/logo/79ae3f51f0781097858acc751cacf304.png'

const route = useRoute()
const showHero = computed(() => route.name !== 'result')

const intertekHome = 'https://www.intertek.com/'
const intertekPrivacy = 'https://www.intertek.com/privacy-policy/'
const intertekCookies = 'https://www.intertek.com/cookie-policy/'
const intertekTerms = 'https://www.intertek.com/website-terms-of-use/'
</script>

<template>
  <div class="app">
    <header class="site-header">
      <div class="header-inner">
        <div class="brand-left">
          <div class="brand-kicker">Developed By</div>
          <div class="brand-name">Intertek AI</div>
        </div>
        <div class="brand-center">
          <a class="brand-logo" :href="intertekHome" target="_blank" rel="noreferrer">
            <img class="brand-logo-img" :src="intertekLogo" alt="Intertek" />
          </a>
        </div>
        <div class="brand-right" />
      </div>
    </header>
    <main class="container">
      <section v-if="showHero" class="hero">
        <h1 class="hero-title">EU AI Act Risk Classifier</h1>
        <p class="hero-subtitle">Determine your risk level under the EU AI Act.</p>
      </section>
      <router-view v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </router-view>
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-top">
          <a class="footer-brand" :href="intertekHome" target="_blank" rel="noreferrer">Intertek</a>
          <nav class="footer-links" aria-label="Legal">
            <a :href="intertekPrivacy" target="_blank" rel="noreferrer">Privacy Policy</a>
            <span class="footer-sep">·</span>
            <a :href="intertekCookies" target="_blank" rel="noreferrer">Cookie Policy</a>
            <span class="footer-sep">·</span>
            <a :href="intertekTerms" target="_blank" rel="noreferrer">Terms of Use</a>
          </nav>
        </div>
        <div class="footer-disclaimer">
          This tool is provided for informational purposes only and does not constitute legal advice. Intertek makes no
          warranties regarding completeness or accuracy, and you remain responsible for assessing your obligations under
          applicable laws and regulations.
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
:root {
  --bg: #ffffff;

  --text: #0c0f12;
  --muted: rgba(12, 15, 18, 0.68);
  --muted-2: rgba(12, 15, 18, 0.52);

  --surface: #ffffff;
  --surface-border: rgba(12, 15, 18, 0.12);
  --surface-border-2: rgba(12, 15, 18, 0.18);
  --shadow: 0 18px 44px rgba(0, 0, 0, 0.12);

  --primary: #d3a700;
  --primary-hi: #c29600;
  --primary-ink: #0c0f12;
  --ring: 0 0 0 3px rgba(211, 167, 0, 0.22);

  --radius: 4px;
  --header-gap: 64px;
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
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  text-rendering: geometricPrecision;
}

a {
  color: inherit;
}

.app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.site-header {
  min-height: 25vh;
  padding: var(--header-gap) 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: saturate(180%) blur(10px);
  border-bottom: 0;
  display: flex;
  align-items: flex-start;
}

.header-inner {
  width: min(1180px, calc(100% - 56px));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 18px;
  color: var(--text);
}

.brand-left {
  display: flex;
  flex-direction: column;
  gap: 6px;
  justify-self: start;
}

.brand-kicker {
  font-size: 14px;
  letter-spacing: 0.4px;
  color: var(--muted);
}

.brand-name {
  font-weight: 800;
  letter-spacing: 0.5px;
  font-size: 24px;
  line-height: 1.1;
}

.brand-center {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  justify-self: center;
}

.brand-right {
  justify-self: end;
}

.brand-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 10px;
  border-radius: 999px;
  border: 1px solid rgba(12, 15, 18, 0.1);
  background: #ffffff;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
  text-decoration: none;
}

.brand-logo:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.brand-logo-img {
  height: 108px;
  width: auto;
  display: block;
}

.container {
  width: min(1180px, calc(100% - 56px));
  margin: 0 auto;
  padding: 0 0 76px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  flex: 1 0 auto;
}

.hero {
  text-align: center;
  margin-top: 0;
}

.hero-title {
  margin: 0;
  font-size: 44px;
  line-height: 1.1;
  letter-spacing: 0.2px;
  color: var(--text);
}

.hero-subtitle {
  margin: 10px 0 0;
  font-size: 14px;
  letter-spacing: 0.3px;
  color: var(--muted);
}

.card {
  background: var(--surface);
  border: 0;
  border-radius: var(--radius);
  padding: 0;
  box-shadow: var(--shadow);
  position: relative;
  width: min(980px, 100%);
  display: flex;
  flex-direction: column;
}

.card-body {
  padding: 30px 42px 26px;
  color: var(--text);
}

.card-footer {
  background: var(--primary);
  padding: 18px 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.footer-btn {
  appearance: none;
  background: transparent;
  border: 0;
  color: var(--primary-ink);
  font-weight: 800;
  font-size: 16px;
  letter-spacing: 0.2px;
  cursor: pointer;
  padding: 6px 8px;
}

.footer-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.footer-btn:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
}

.title {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.1px;
  line-height: 1.28;
  color: var(--text);
}

.subtitle {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

.muted {
  color: var(--muted);
}

.bullets {
  margin: 14px 0 0;
  padding: 0 0 0 18px;
  color: var(--text);
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
  margin-top: 18px;
  justify-content: flex-start;
}

.btn {
  appearance: none;
  border-radius: 3px;
  cursor: pointer;
  border: 1px solid var(--surface-border);
  color: var(--text);
  background: #ffffff;
  font-size: 14px;
  padding: 10px 14px;
  transition: transform 120ms ease, background 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
}

.btn:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.btn:hover {
  background: rgba(211, 167, 0, 0.07);
  border-color: var(--surface-border-2);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0px);
}

.btn-primary {
  background: var(--primary);
  border-color: rgba(0, 0, 0, 0);
  color: var(--primary-ink);
  font-weight: 700;
  letter-spacing: 0.2px;
  box-shadow: 0 10px 26px rgba(211, 167, 0, 0.22);
}

.btn-primary:hover {
  background: var(--primary-hi);
  border-color: rgba(0, 0, 0, 0);
}

.btn-option {
  min-width: 150px;
  padding: 14px 16px;
  border-radius: 3px;
  background: #ffffff;
  border-color: var(--surface-border);
  font-weight: 700;
}

.page-center {
  text-align: center;
}

.page-center .btn {
  align-self: center;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 180ms ease, transform 240ms cubic-bezier(0.2, 0.9, 0.2, 1);
  will-change: opacity, transform;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.992);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.992);
}

.page-enter-to,
.page-leave-from {
  opacity: 1;
  transform: translateY(0px) scale(1);
}

.error {
  color: rgba(163, 20, 20, 0.95);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.site-footer {
  padding: 22px 0 30px;
  color: var(--muted);
}

.footer-inner {
  width: min(1180px, calc(100% - 56px));
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.footer-brand {
  text-decoration: none;
  font-weight: 800;
  letter-spacing: 0.2px;
  color: rgba(12, 15, 18, 0.78);
}

.footer-links {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.footer-links a {
  color: rgba(12, 15, 18, 0.72);
  text-decoration: none;
  font-weight: 650;
  letter-spacing: 0.1px;
  font-size: 13px;
}

.footer-links a:hover {
  text-decoration: underline;
  text-decoration-thickness: 1px;
}

.footer-sep {
  color: rgba(12, 15, 18, 0.4);
}

.footer-disclaimer {
  font-size: 12px;
  line-height: 1.65;
  color: rgba(12, 15, 18, 0.6);
}

@media (prefers-reduced-motion: reduce) {
  .btn {
    transition: none;
  }

  .page-enter-active,
  .page-leave-active {
    transition: none;
  }

  .page-enter-from,
  .page-leave-to {
    opacity: 1;
    transform: none;
  }
}

@media (max-width: 640px) {
  :root {
    --header-gap: 28px;
  }

  .header-inner {
    width: min(1180px, calc(100% - 28px));
  }

  .brand-logo-img {
    height: 78px;
  }

  .brand-kicker {
    font-size: 13px;
  }

  .brand-name {
    font-size: 20px;
  }

  .container {
    width: min(1180px, calc(100% - 28px));
    padding: 0 0 48px;
    gap: 18px;
  }

  .footer-inner {
    width: min(1180px, calc(100% - 28px));
  }

  .footer-top {
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-links {
    justify-content: flex-start;
  }

  .card {
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.24);
  }

  .card-body {
    padding: 20px 16px 18px;
  }

  .card-footer {
    padding: 14px 16px;
  }

  .btn-option {
    min-width: 100%;
  }
}
</style>
