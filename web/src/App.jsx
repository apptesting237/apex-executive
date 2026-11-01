import { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  const fetchSummary = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await fetch(`${API_URL}/`);
      if (!response.ok) {
        throw new Error('Unable to reach the backend');
      }

      const data = await response.json();
      setSummary(data);
    } catch (err) {
      setError(err.message || 'Failed to load Apex Executive backend summary');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const statCards = summary
    ? [
        { label: 'Total teams', value: summary.total_teams ?? 0 },
        { label: 'Running crews', value: summary.running_crews ?? 0 },
        { label: 'Alerts', value: summary.alerts ?? 0 },
        { label: 'Healthy status', value: summary.system_status ?? 'Unknown' },
      ]
    : [];

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Operations dashboard</p>
          <h1>Apex Executive</h1>
        </div>
        <button className="refresh-button" onClick={fetchSummary} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </header>

      <main className="content-area">
        {error ? (
          <div className="error-panel">
            <strong>Connection error</strong>
            <p>{error}</p>
          </div>
        ) : null}

        {loading && !summary ? (
          <div className="loading-panel">Loading system summary…</div>
        ) : null}

        {summary ? (
          <>
            <section className="hero-panel">
              <div>
                <p className="eyebrow">System overview</p>
                <h2>{summary.name || 'Executive control center'}</h2>
              </div>
              <span className={`status-badge ${summary.system_status === 'healthy' ? 'healthy' : 'warning'}`}>
                {summary.system_status || 'Unknown'}
              </span>
            </section>

            <section className="stats-grid">
              {statCards.map((card) => (
                <article className="stat-card" key={card.label}>
                  <span>{card.label}</span>
                  <strong>{card.value}</strong>
                </article>
              ))}
            </section>

            <section className="details-panel">
              <h3>Latest summary</h3>
              <pre>{JSON.stringify(summary, null, 2)}</pre>
            </section>
          </>
        ) : null}
      </main>
    </div>
  );
}

export default App;
