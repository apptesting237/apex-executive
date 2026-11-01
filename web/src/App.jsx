import { useEffect, useState } from 'react';

const API_URL =
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://apex-executive-backend.onrender.com';

function App() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  const fetchSummary = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/health`);
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

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Enterprise control layer</p>
          <h1>Apex Executive</h1>
        </div>
        <button onClick={fetchSummary} className="refresh-btn">
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </header>

      {error && <div className="status-banner error">{error}</div>}

      {loading ? (
        <div className="loading-panel">Loading executive overview…</div>
      ) : (
        <section className="panel-grid">
          <article className="panel">
            <h2>Backend status</h2>
            <ul className="list">
              <li>Service: {summary?.service || 'Unknown'}</li>
              <li>Status: {summary?.status || 'Unknown'}</li>
              <li>Version: {summary?.version || 'Unknown'}</li>
            </ul>
          </article>
        </section>
      )}
    </div>
  );
}

export default App;
