import { useEffect, useState } from 'react';

const API_URL =
  import.meta.env.VITE_API_URL ||
  (window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : window.location.origin);

function App() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  const fetchSummary = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/`);
      if (!response.ok) {
        throw new Error('Unable to reach backend');
      }
      const data = await response.json();
      setSummary(data);
    } catch (err) {
      setError(err.message || 'Failed to load Apex Executive backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const statCards = summary
    ? [
        { label: 'Company', value: summary.company || 'Apex Executive' },
        { label: 'Status', value: summary.status || 'Online' },
        { label: 'Version', value: summary.version || 'N/A' },
        { label: 'Firewall', value: summary.firewall || 'Active' },
      ]
    : [];

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Enterprise control layer</p>
          <h1>Apex Executive</h1>
        </div>
        <button onClick={fetchSummary} className="refresh-btn">
          Refresh
        </button>
      </header>

      {error && <div className="status-banner error">{error}</div>}

      {loading ? (
        <div className="loading-panel">Loading executive overview…</div>
      ) : (
        <>
          <section className="stats-grid">
            {statCards.map((card) => (
              <article className="stat-card" key={card.label}>
                <span>{card.label}</span>
                <strong>{card.value}</strong>
              </article>
            ))}
          </section>

          <section className="panel-grid">
            <article className="panel">
              <h2>Operating status</h2>
              <ul className="list">
                <li>AI executive cockpit online</li>
                <li>Human approval required for critical actions</li>
                <li>Risk controls enabled by default</li>
              </ul>
            </article>

            <article className="panel">
              <h2>Execution flow</h2>
              <ul className="list">
                <li>Intake &amp; policy scan</li>
                <li>Scenario risk review</li>
                <li>Leadership approval queue</li>
                <li>Action log and audit trail</li>
              </ul>
            </article>
          </section>
        </>
      )}
    </div>
  );
}

export default App;
