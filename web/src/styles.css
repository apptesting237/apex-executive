import { useMemo, useState } from 'react';

const overview = {
  revenue: 214850,
  approvals: 3,
  threats: 1842,
  activeVentures: 12,
};

const ventureData = [
  { id: 'V-101', sector: 'Trade', title: 'Titanium Arbitrage', value: '$54,200', status: 'Pipeline' },
  { id: 'V-102', sector: 'Biotech', title: 'Oncology Protocol', value: '$120,000', status: 'In review' },
  { id: 'V-103', sector: 'Real Estate', title: 'Austin Logistics Park', value: '$84,000', status: 'Approved' },
];

const approvals = [
  { id: 'APR-104', title: 'Release Letter of Credit', amount: '$126,000', owner: 'Trade Desk' },
  { id: 'APR-221', title: 'Board Memo Draft Approval', amount: '$0', owner: 'Legal' },
  { id: 'APR-309', title: 'Austin Closing SOW', amount: '$84,000', owner: 'Real Estate' },
];

const riskCards = [
  { title: 'Compliance', value: 'Low', detail: 'Policy checks clear' },
  { title: 'Threat Defense', value: '1842', detail: 'Blocked injections' },
  { title: 'AI Safety', value: 'Human review', detail: 'Required for actions' },
];

const initialDocument = `
<h1>Board Summary</h1>
<p><strong>Executive summary:</strong> Revenue remains disciplined and pipeline quality is improving across the trading, biotech, and real-estate portfolio.</p>
<ul>
  <li>Maintain strategic patience before large capital deployments.</li>
  <li>Continue safe AI-assisted briefings with human approval.</li>
  <li>Prioritize compliance and leadership review over speed.</li>
</ul>
`;

function RichTextEditor({ initialHtml }) {
  const [html, setHtml] = useState(initialHtml);

  const applyFormat = (format) => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      setHtml((current) => current + `<${format}>New content</${format}>`);
      return;
    }

    const range = selection.getRangeAt(0);
    const selectedText = range.toString();

    if (!selectedText) {
      const element = document.createElement(format === 'b' ? 'b' : format === 'i' ? 'i' : 'mark');
      element.textContent = format === 'b' ? 'bold text' : format === 'i' ? 'italic text' : 'highlight';
      range.insertNode(element);
      setHtml(document.getElementById('editor').innerHTML);
      return;
    }

    const wrapper = document.createElement(format === 'b' ? 'b' : format === 'i' ? 'i' : 'mark');
    wrapper.textContent = selectedText;
    range.deleteContents();
    range.insertNode(wrapper);
    setHtml(document.getElementById('editor').innerHTML);
  };

  return (
    <div className="panel document-panel">
      <div className="panel-header">
        <h3>Board Notes</h3>
        <div className="toolbar">
          <button type="button" onClick={() => applyFormat('b')}>Bold</button>
          <button type="button" onClick={() => applyFormat('i')}>Italic</button>
          <button type="button" onClick={() => applyFormat('mark')}>Highlight</button>
        </div>
      </div>
      <div
        id="editor"
        className="rich-editor"
        dangerouslySetInnerHTML={{ __html: html }}
        contentEditable
        onInput={(event) => setHtml(event.currentTarget.innerHTML)}
      />
    </div>
  );
}

function App() {
  const summary = useMemo(
    () => [
      { label: 'MTD Revenue', value: `$${overview.revenue.toLocaleString()}` },
      { label: 'Approvals', value: overview.approvals },
      { label: 'Threats Blocked', value: overview.threats.toLocaleString() },
      { label: 'Active Ventures', value: overview.activeVentures },
    ],
    []
  );

  const [chatInput, setChatInput] = useState('Summarize the safest next move for the executive team.');
  const [assistantReply, setAssistantReply] = useState(
    'The company should maintain a cautious capital deployment plan, prioritize the approved pipeline, and keep all material actions under human review.'
  );

  const handleAsk = () => {
    setAssistantReply(
      'Recommended action: maintain a measured operating rhythm, keep the approval queue visible to leadership, and proceed only with verified opportunities. AI is advisory; execution remains human-approved.'
    );
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-wrap">
          <div className="brand-mark">A</div>
          <div>
            <div className="brand-title">APEX</div>
            <div className="brand-subtitle">Executive OS</div>
          </div>
        </div>

        <nav className="nav">
          <button type="button" className="nav-item active">Overview</button>
          <button type="button" className="nav-item">Ventures</button>
          <button type="button" className="nav-item">Approvals</button>
          <button type="button" className="nav-item">Documents</button>
          <button type="button" className="nav-item">Risk</button>
          <button type="button" className="nav-item">AI</button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">CEO cockpit</div>
            <h1>Executive command center</h1>
          </div>
          <button type="button" className="primary-btn">Approve queue</button>
        </header>

        <section className="summary-grid">
          {summary.map((item) => (
            <div key={item.label} className="metric-card">
              <div className="metric-label">{item.label}</div>
              <div className="metric-value">{item.value}</div>
            </div>
          ))}
        </section>

        <section className="content-grid">
          <div className="left-stack">
            <div className="panel">
              <div className="panel-header">
                <h3>Active ventures</h3>
              </div>
              <div className="table-list">
                {ventureData.map((item) => (
                  <div className="list-row" key={item.id}>
                    <div>
                      <div className="row-title">{item.title}</div>
                      <div className="row-meta">{item.sector} • {item.id}</div>
                    </div>
                    <div className="row-right">
                      <div className="row-value">{item.value}</div>
                      <span className="pill">{item.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h3>Approvals</h3>
              </div>
              <div className="table-list">
                {approvals.map((item) => (
                  <div className="list-row" key={item.id}>
                    <div>
                      <div className="row-title">{item.title}</div>
                      <div className="row-meta">{item.owner}</div>
                    </div>
                    <div className="row-right">
                      <div className="row-value">{item.amount}</div>
                      <button type="button" className="tiny-btn">Review</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="right-stack">
            <div className="panel">
              <div className="panel-header">
                <h3>Risk & compliance</h3>
              </div>
              <div className="risk-grid">
                {riskCards.map((card) => (
                  <div className="risk-card" key={card.title}>
                    <div className="risk-title">{card.title}</div>
                    <div className="risk-value">{card.value}</div>
                    <div className="risk-detail">{card.detail}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h3>AI advisor</h3>
              </div>
              <div className="chat-box">
                <textarea
                  value={chatInput}
                  onChange={(event) => setChatInput(event.target.value)}
                  rows={3}
                />
                <button type="button" className="primary-btn full" onClick={handleAsk}>Ask advisor</button>
                <div className="assistant-reply">
                  {assistantReply}
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="bottom-row">
          <RichTextEditor initialHtml={initialDocument} />
        </section>
      </main>
    </div>
  );
}

export default App;
