<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import intertekLogo from '@/assets/images/logo/79ae3f51f0781097858acc751cacf304.png'

const router = useRouter()
const store = useQuestionnaireStore()

const friendlyError = computed(() => {
  const raw = store.error ?? ''
  const lower = raw.toLowerCase()
  if (lower.includes('failed to fetch') || lower.includes('load_failed')) {
    return '后端未启动或不可达（127.0.0.1:8000）'
  }
  if (lower.includes('tree_http_') || lower.includes('results_http_')) {
    return '后端接口返回异常'
  }
  return raw
})

onMounted(async () => {
  await store.load()
})

async function start() {
  store.reset()
  await store.load()
  await router.push({ name: 'question', params: { id: store.startId } })
}

async function retry() {
  await store.load()
}
</script>

<template>
  <div class="welcome-page">
    <header class="welcome-nav">
      <div class="nav-inner">
        <div class="brand">
          <div class="brand-icon">
            <img class="brand-logo-img" :src="intertekLogo" alt="Intertek" />
          </div>
          <div class="brand-text">
            <h2 class="brand-title">Intertek</h2>
            <span class="brand-subtitle">Compliance Portal</span>
          </div>
        </div>

        <nav class="nav-links" aria-label="Primary">
          <a class="nav-link" href="#">Resources</a>
          <a class="nav-link" href="#">Global Support</a>
        </nav>
      </div>
    </header>

    <main class="welcome-main">
      <section class="hero">
        <div class="hero-bg circuit-pattern" aria-hidden="true"></div>
        <div class="hero-bg-blob" aria-hidden="true"></div>

        <div class="hero-inner">
          <div class="hero-pill">
            <span class="ping" aria-hidden="true">
              <span class="ping-outer"></span>
              <span class="ping-inner"></span>
            </span>
            <span class="hero-pill-text">2024 Regulatory Update</span>
          </div>

          <h1 class="hero-h1">Navigate the <span class="hero-primary">EU AI Act</span> with Confidence</h1>
          <p class="hero-lead">
            Intertek’s expert-led digital assessment tool helps you determine regulatory obligations and risk
            classifications for your AI systems in minutes.
          </p>

          <div class="hero-actions">
            <button class="btn-primary" type="button" :disabled="!!store.error || store.loading" @click="start">
              <span>Start Assessment</span>
              <span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span>
            </button>
            <button class="btn-secondary" type="button" disabled>Watch Demo</button>
          </div>

          <p class="hero-step">Step 1 of 4: Preliminary Identification</p>

          <div v-if="store.loading" class="hero-status">加载中…</div>
          <div v-else-if="store.error" class="hero-error">
            <div>加载失败：{{ friendlyError }}</div>
            <button class="btn-retry" type="button" @click="retry">重试</button>
          </div>
        </div>
      </section>

      <section class="features">
        <div class="features-head">
          <h2 class="features-title">Why use this tool?</h2>
          <div class="features-line" aria-hidden="true"></div>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <span class="material-symbols-outlined" aria-hidden="true">verified_user</span>
            </div>
            <div class="feature-body">
              <h3 class="feature-title">Fully Up-to-Date</h3>
              <p class="feature-text">
                Our logic engine is synchronized with the final 2024 European Parliament AI Act framework, ensuring
                regulatory alignment.
              </p>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <span class="material-symbols-outlined" aria-hidden="true">bolt</span>
            </div>
            <div class="feature-body">
              <h3 class="feature-title">Streamlined Path</h3>
              <p class="feature-text">
                Avoid dense legal texts. Answer specific, guided questions about your system’s technical deployment and
                use case.
              </p>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <span class="material-symbols-outlined" aria-hidden="true">description</span>
            </div>
            <div class="feature-body">
              <h3 class="feature-title">Actionable Insight</h3>
              <p class="feature-text">
                Receive an instant summary report detailing risk categories, mandatory obligations, and immediate next
                steps for compliance.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="cta">
        <div class="cta-card">
          <div class="cta-blob" aria-hidden="true"></div>
          <div class="cta-inner">
            <div class="cta-text">
              <h3 class="cta-title">Ready to secure your AI deployment?</h3>
              <p class="cta-subtitle">
                The assessment typically takes 5–10 minutes. No specialized legal knowledge required for the initial phase.
              </p>
            </div>
            <button class="cta-btn" type="button" :disabled="!!store.error || store.loading" @click="start">
              Begin Assessment
            </button>
          </div>
        </div>
      </section>
    </main>

    <footer class="welcome-footer">
      <div class="footer-grid">
        <div class="footer-about">
          <div class="footer-brand">
            <div class="footer-brand-icon" aria-hidden="true">
              <svg class="footer-brand-svg" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path
                  clip-rule="evenodd"
                  d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z"
                  fill="currentColor"
                  fill-rule="evenodd"
                ></path>
                <path
                  clip-rule="evenodd"
                  d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z"
                  fill="currentColor"
                  fill-rule="evenodd"
                ></path>
              </svg>
            </div>
            <h2 class="footer-brand-title">Intertek</h2>
          </div>
          <p class="footer-about-text">
            Intertek is a leading Total Quality Assurance provider to industries worldwide. Our network of more than 1,000
            laboratories and offices in over 100 countries delivers innovative and bespoke Assurance, Testing, Inspection
            and Certification solutions.
          </p>
        </div>

        <div class="footer-col">
          <h4 class="footer-col-title">Compliance</h4>
          <ul class="footer-list">
            <li><a class="footer-link" href="#">EU AI Act Guide</a></li>
            <li><a class="footer-link" href="#">Risk Assessment</a></li>
            <li><a class="footer-link" href="#">Certification Services</a></li>
            <li><a class="footer-link" href="#">Technical Files</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4 class="footer-col-title">Legal</h4>
          <ul class="footer-list">
            <li>
              <a class="footer-link" href="https://www.intertek.com/privacy-policy/" target="_blank" rel="noreferrer">
                Privacy Policy
              </a>
            </li>
            <li>
              <a class="footer-link" href="https://www.intertek.com/website-terms-of-use/" target="_blank" rel="noreferrer">
                Terms of Use
              </a>
            </li>
            <li>
              <a class="footer-link" href="https://www.intertek.com/cookie-policy/" target="_blank" rel="noreferrer">
                Cookie Policy
              </a>
            </li>
            <li><a class="footer-link" href="#">Accessibility</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="footer-copy">© 2024 Intertek Group plc. All rights reserved.</p>
        <div class="footer-icons">
          <a class="footer-icon-link" href="#" aria-label="Language">
            <span class="material-symbols-outlined" aria-hidden="true">language</span>
          </a>
          <a class="footer-icon-link" href="#" aria-label="Global">
            <span class="material-symbols-outlined" aria-hidden="true">public</span>
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.welcome-page {
  --w-primary: #0e6b7c;
  --w-accent-yellow: #ffcc00;
  --w-bg-light: #fafaf9;
  --w-card-border: #d0e3e7;

  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: var(--w-bg-light);
  color: rgba(15, 23, 42, 0.95);
  overflow-x: hidden;
  font-family: Manrope, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, 'Apple Color Emoji',
    'Segoe UI Emoji';
}

.welcome-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
  border-bottom: 1px solid rgba(208, 227, 231, 0.5);
  background: rgba(250, 250, 249, 0.8);
  backdrop-filter: blur(12px);
  padding: 14px 16px;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #ffffff;
  border: 1px solid rgba(208, 227, 231, 0.7);
  display: grid;
  place-items: center;
}

.brand-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
  display: block;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-title {
  margin: 0;
  color: var(--w-primary);
  font-size: 18px;
  font-weight: 850;
  letter-spacing: -0.02em;
  line-height: 1;
}

.brand-subtitle {
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 800;
  color: rgba(100, 116, 139, 0.95);
  line-height: 1;
}

.nav-links {
  display: none;
  align-items: center;
  gap: 20px;
  white-space: nowrap;
}

.nav-link {
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  color: rgba(15, 23, 42, 0.86);
  transition: color 120ms ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--w-primary);
}

.welcome-main {
  flex: 1 0 auto;
}

.hero {
  position: relative;
  overflow: hidden;
  padding: 80px 24px 64px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.circuit-pattern {
  background-image: radial-gradient(var(--w-primary) 0.5px, transparent 0.5px);
  background-size: 24px 24px;
  opacity: 0.05;
}

.hero-bg-blob {
  position: absolute;
  top: -96px;
  left: 50%;
  transform: translateX(-50%);
  width: 800px;
  height: 400px;
  background: rgba(14, 107, 124, 0.05);
  filter: blur(120px);
  border-radius: 999px;
  pointer-events: none;
}

.hero-inner {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 204, 0, 0.1);
  border: 1px solid rgba(255, 204, 0, 0.3);
  margin-bottom: 24px;
}

.ping {
  position: relative;
  width: 8px;
  height: 8px;
  display: inline-block;
}

.ping-outer {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  background: var(--w-accent-yellow);
  opacity: 0.75;
  animation: ping 1.4s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.ping-inner {
  position: relative;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--w-accent-yellow);
  display: inline-block;
}

@keyframes ping {
  0% {
    transform: scale(1);
    opacity: 0.75;
  }
  100% {
    transform: scale(2.2);
    opacity: 0;
  }
}

.hero-pill-text {
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(51, 65, 85, 0.95);
}

.hero-h1 {
  margin: 0 0 24px;
  font-size: 40px;
  line-height: 1.1;
  font-weight: 900;
  letter-spacing: -0.03em;
}

.hero-primary {
  color: var(--w-primary);
}

.hero-lead {
  margin: 0 auto 40px;
  font-size: 18px;
  line-height: 1.75;
  color: rgba(71, 85, 105, 0.95);
  max-width: 640px;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.btn-primary,
.btn-secondary,
.cta-btn,
.btn-retry {
  appearance: none;
  border: 0;
  cursor: pointer;
  font-family: inherit;
}

.btn-primary {
  min-width: 200px;
  height: 56px;
  padding: 0 32px;
  border-radius: 12px;
  background: var(--w-primary);
  color: #ffffff;
  font-size: 18px;
  font-weight: 850;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 18px 36px rgba(14, 107, 124, 0.2);
  transition: transform 140ms ease, box-shadow 160ms ease, opacity 120ms ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 22px 44px rgba(14, 107, 124, 0.32);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled,
.cta-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  min-width: 200px;
  height: 56px;
  padding: 0 32px;
  border-radius: 12px;
  background: transparent;
  border: 2px solid rgba(226, 232, 240, 1);
  color: rgba(51, 65, 85, 0.95);
  font-size: 18px;
  font-weight: 850;
}

.hero-step {
  margin: 24px 0 0;
  font-size: 14px;
  font-weight: 700;
  color: rgba(100, 116, 139, 0.95);
}

.hero-status {
  margin-top: 16px;
  color: rgba(100, 116, 139, 0.95);
  font-weight: 650;
}

.hero-error {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  color: rgba(163, 20, 20, 0.95);
}

.btn-retry {
  height: 40px;
  padding: 0 14px;
  border-radius: 10px;
  background: rgba(14, 107, 124, 0.08);
  border: 1px solid rgba(14, 107, 124, 0.18);
  color: rgba(15, 23, 42, 0.86);
  font-weight: 750;
}

.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 64px 24px;
}

.features-head {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 24px;
  padding: 0 8px;
}

.features-title {
  margin: 0;
  font-size: 24px;
  font-weight: 850;
  color: rgba(15, 23, 42, 0.95);
}

.features-line {
  height: 1px;
  flex: 1;
  background: linear-gradient(to right, rgba(208, 227, 231, 0.6), transparent);
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: 18px;
  border-radius: 18px;
  border: 1px solid var(--w-card-border);
  background: #ffffff;
  padding: 28px;
  transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
}

.feature-card:hover {
  border-color: rgba(14, 107, 124, 0.5);
  box-shadow: 0 24px 52px rgba(14, 107, 124, 0.06);
  transform: translateY(-2px);
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(14, 107, 124, 0.1);
  color: var(--w-primary);
  display: grid;
  place-items: center;
  transition: background 160ms ease, color 160ms ease;
}

.feature-card:hover .feature-icon {
  background: var(--w-primary);
  color: #ffffff;
}

.feature-icon .material-symbols-outlined {
  font-size: 28px;
}

.feature-title {
  margin: 0;
  font-size: 20px;
  font-weight: 850;
  color: rgba(15, 23, 42, 0.95);
}

.feature-text {
  margin: 8px 0 0;
  color: rgba(71, 85, 105, 0.95);
  line-height: 1.7;
}

.cta {
  max-width: 1200px;
  margin: 0 auto 96px;
  padding: 0 24px;
}

.cta-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  border: 1px solid rgba(14, 107, 124, 0.2);
  background: rgba(14, 107, 124, 0.05);
  padding: 28px;
}

.cta-blob {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(33%, -50%);
  width: 256px;
  height: 256px;
  border-radius: 999px;
  background: rgba(14, 107, 124, 0.1);
  filter: blur(48px);
  pointer-events: none;
}

.cta-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  text-align: center;
}

.cta-title {
  margin: 0 0 8px;
  font-size: 22px;
  font-weight: 850;
  color: rgba(15, 23, 42, 0.95);
}

.cta-subtitle {
  margin: 0;
  color: rgba(71, 85, 105, 0.95);
  line-height: 1.65;
}

.cta-btn {
  height: 48px;
  padding: 0 40px;
  border-radius: 12px;
  background: var(--w-primary);
  color: #ffffff;
  font-size: 16px;
  font-weight: 850;
  box-shadow: 0 18px 36px rgba(14, 107, 124, 0.2);
  transition: transform 140ms ease, box-shadow 160ms ease;
  white-space: nowrap;
}

.cta-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 22px 44px rgba(14, 107, 124, 0.32);
}

.welcome-footer {
  border-top: 1px solid rgba(208, 227, 231, 0.5);
  background: #ffffff;
  padding: 48px 24px;
}

.footer-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
}

.footer-about-text {
  margin: 0;
  font-size: 14px;
  color: rgba(100, 116, 139, 0.95);
  line-height: 1.7;
  max-width: 520px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.footer-brand-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: rgba(148, 163, 184, 0.55);
  color: rgba(15, 23, 42, 0.85);
  display: grid;
  place-items: center;
}

.footer-brand-svg {
  width: 16px;
  height: 16px;
}

.footer-brand-title {
  margin: 0;
  font-size: 18px;
  font-weight: 850;
  color: rgba(15, 23, 42, 0.95);
}

.footer-col-title {
  margin: 0 0 18px;
  font-size: 12px;
  font-weight: 850;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(15, 23, 42, 0.95);
}

.footer-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 14px;
  font-size: 14px;
  color: rgba(100, 116, 139, 0.95);
}

.footer-link {
  color: inherit;
  text-decoration: none;
  font-weight: 650;
}

.footer-link:hover {
  color: var(--w-primary);
}

.footer-bottom {
  max-width: 1200px;
  margin: 48px auto 0;
  padding-top: 18px;
  border-top: 1px solid rgba(208, 227, 231, 0.3);
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.footer-copy {
  margin: 0;
  font-size: 12px;
  color: rgba(148, 163, 184, 1);
}

.footer-icons {
  display: flex;
  gap: 24px;
}

.footer-icon-link {
  color: rgba(148, 163, 184, 1);
  text-decoration: none;
}

.footer-icon-link:hover {
  color: var(--w-primary);
}

@media (min-width: 640px) {
  .hero-actions {
    flex-direction: row;
    gap: 16px;
  }
}

@media (min-width: 768px) {
  .nav-links {
    display: inline-flex;
    transform: translateX(-28px);
  }

  .hero-h1 {
    font-size: 60px;
  }

  .features-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }

  .cta-card {
    padding: 44px;
  }

  .cta-inner {
    flex-direction: row;
    text-align: left;
  }

  .footer-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 48px;
  }

  .footer-about {
    grid-column: span 2;
  }

  .footer-bottom {
    flex-direction: row;
  }
}

@media (min-width: 1024px) {
  .welcome-nav {
    padding: 14px 24px;
  }

  .nav-links {
    gap: 32px;
    transform: translateX(0);
  }
}
</style>
