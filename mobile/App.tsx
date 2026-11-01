* {
  box-sizing: border-box;
}

:root {
  --bg: #06131f;
  --bg-strong: #0a1d2d;
  --panel: rgba(9, 18, 28, 0.82);
  --panel-border: rgba(148, 163, 184, 0.18);
  --text: #edf6ff;
  --muted: #a8c3db;
  --accent: #60a5fa;
  --green: #4ade80;
  --amber: #fbbf24;
  --blue: #60a5fa;
  --red: #f87171;
  --purple: #8b5cf6;
}

html, body, #root {
  margin: 0;
  min-height: 100%;
  min-height: 100vh;
  background: radial-gradient(circle at top, rgba(96, 165, 250, 0.18), transparent 25%), var(--bg);
  color: var(--text);
  font-family: Inter, 'Segoe UI', sans-serif;
}

button {
  font: inherit;
}

.app-shell {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 20px 60px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  letter-spacing: 0.15em;
  font-size: 11px;
  text-transform: uppercase;
  color: var(--accent);
}

h1 {
  margin: 0;
  font-size: clamp(2.2rem, 5vw, 3.5rem);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.live-pill,
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 0.4rem 0.8rem;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: rgba(74, 222, 128, 0.18);
  color: #d9fbe7;
  border: 1px solid rgba(74, 222, 128, 0.36);
}

.badge.warn {
  background: rgba(251, 191, 36, 0.14);
  color: #fef3c7;
  border-color: rgba(251, 191, 36, 0.28);
}

.badge.info,
.badge.ghost {
  background: rgba(96, 165, 250, 0.12);
  color: #dbeafe;
  border-color: rgba(96, 165, 250, 0.28);
}

.refresh-btn,
.tiny {
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.refresh-btn {
  background: linear-gradient(135deg, var(--accent), var(--purple));
  padding: 0.7rem 1rem;
  color: white;
  font-weight: 700;
}

.refresh-btn:hover,
.tiny:hover {
  transform: translateY(-1px);
}

.stats-grid,
.hero-grid,
.lower-grid {
  display: grid;
  gap: 20px;
  margin-bottom: 20px;
}

.stats-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.hero-grid {
  grid-template-columns: 1.5fr 1fr;
}

.lower-grid {
  grid-template-columns: 1.2fr 0.8fr;
}

.stat-card,
.panel {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  box-shadow: 0 18px 30px rgba(2, 6, 23, 0.28);
}

.stat-card {
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-card span {
  color: var(--muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.stat-card strong {
  font-size: clamp(1.3rem, 2vw, 2.1rem);
}

.panel {
  padding: 20px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  gap: 12px;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.office-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.desk {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(15, 23, 42, 0.58);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 12px;
  padding: 12px 14px;
}

.desk strong,
.memory-item strong,
.approval-item strong {
  display: block;
  margin-bottom: 4px;
}

.desk small,
.memory-meta,
.approval-item small {
  color: var(--muted);
}

.signal {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 0 0 5px rgba(255, 255, 255, 0.04);
}

.signal-green { background: var(--green); }
.signal-amber { background: var(--amber); }
.signal-blue { background: var(--blue); }
.signal-red { background: var(--red); }

.brain-map {
  position: relative;
  height: 220px;
  border-radius: 16px;
  background:
    radial-gradient(circle, rgba(96, 165, 250, 0.2), transparent 38%),
    linear-gradient(180deg, rgba(15, 23, 42, 0.9), rgba(7, 16, 27, 0.9));
  border: 1px solid rgba(148, 163, 184, 0.18);
  overflow: hidden;
}

.brain-map::before {
  content: "";
  position: absolute;
  inset: 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.08), rgba(139, 92, 246, 0.12));
}

.node {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 76px;
  height: 76px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #def1ff;
  background: radial-gradient(circle, rgba(96, 165, 250, 0.24), rgba(10, 20, 32, 0.9));
  border: 1px solid rgba(96, 165, 250, 0.38);
  box-shadow: 0 0 18px rgba(96, 165, 250, 0.18);
  animation: pulse 2.6s ease-in-out infinite;
  animation-delay: var(--delay);
}

.node:nth-child(1) { left: 24%; top: 26%; }
.node:nth-child(2) { left: 28%; top: 68%; }
.node:nth-child(3) { left: 52%; top: 32%; }
.node:nth-child(4) { left: 72%; top: 44%; }
.node:nth-child(5) { left: 62%; top: 76%; }
.node:nth-child(6) { left: 40%; top: 52%; }

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.07); }
}

.stack-list,
.memory-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.approval-item,
.memory-item {
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.52);
  padding: 12px 14px;
}

.approval-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.approval-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tiny {
  padding: 0.44rem 0.7rem;
  color: white;
  font-size: 0.72rem;
}

.tiny.success { background: rgba(34, 197, 94, 0.18); border: 1px solid rgba(34, 197, 94, 0.42); }
.tiny.danger { background: rgba(239, 68, 68, 0.16); border: 1px solid rgba(239, 68, 68, 0.42); }
.tiny.neutral { background: rgba(148, 163, 184, 0.14); border: 1px solid rgba(148, 163, 184, 0.3); }

.memory-item strong {
  margin-bottom: 8px;
}

.memory-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.7rem;
}

.alert {
  margin-bottom: 16px;
  border-radius: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(248, 113, 113, 0.4);
  background: rgba(127, 29, 29, 0.26);
  color: #fecaca;
}

.loading-panel {
  display: grid;
  place-items: center;
  min-height: 220px;
  border-radius: 18px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(15, 23, 42, 0.7);
}

.empty-state {
  color: var(--muted);
  margin: 0;
}

@media (max-width: 860px) {
  .hero-grid,
  .lower-grid {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .approval-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
