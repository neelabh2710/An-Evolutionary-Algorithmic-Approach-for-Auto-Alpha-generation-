import Plot from 'react-plotly.js';

export function Selector({ options, value, onChange, label }) {
  return (
    <div>
      <div className="label">{label}</div> {/* Adding a label */}
      <select onChange={(e) => onChange(e.target.value)} value={value}>
        {options.map(option => <option key={option} value={option}>{option}</option>)}
      </select>
    </div>
  );
}
export function ConceptButtons({ concepts, selected, onSelect }) {
  return (
    <div>
      {concepts.map(concept => (
        <button
          key={concept}
          className={selected === concept ? 'activeButton' : 'button'}
          onClick={() => onSelect(concept)}
        >
          {concept}
        </button>
      ))}
    </div>
  );
}
export function Graph({ graphData }) {
  return (
    <Plot
      data={graphData.data}
      layout={graphData.layout}
      style={{ width: "100%", height: "400px" }}
    />
  );
}
export function DateSelector({ dates, value, onChange }) {
  return (
    <select onChange={(e) => onChange(e.target.value)} value={value}>
      {dates.map(date => (
        <option key={date} value={date}>{date}</option>
      ))}
    </select>
  );
}
export function InsightPanel({ insight, capitalize }) {
  return (
    <div className="insight-panel">
      {insight && Object.entries(insight).map(([key, value]) => (
        <div key={key} className="insight-content">
          <h3 className="insight-key">{capitalize(key)}:</h3>
          <p className="insight-text">{value.map(sentence => capitalize(sentence)).join(', ')}</p>
        </div>
      ))}
    </div>
  );
}

