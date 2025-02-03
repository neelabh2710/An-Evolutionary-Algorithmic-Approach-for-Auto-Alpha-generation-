import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import './App.css'; // Ensure the CSS path is correct
import { Selector, ConceptButtons, Graph, DateSelector, InsightPanel } from './Beautify';

const tickers = [
  'MSFT', 'AAPL', 'NVDA', 'GOOGL', 'AMZN', 'META', 'BRK-B', 'LLY', 'TSM', 'AVGO', 'TSLA', 'NVO',
  'V', 'JPM', 'WMT', 'XOM', 'SPY', 'UNH', 'MA', 'PG', 'ASML', 'JNJ', 'LTMAY', 'HD', 'MRK', 'COST',
  'ORCL', 'TM', 'CVX', 'BAC', 'ABBV', 'KO', 'CRM', 'AMD', 'PEP', 'NFLX', 'AZN', 'SHEL', 'TMO', 'SAP',
  'LIN', 'FMX', 'WFC', 'ADBE', 'DIS', 'NVS', 'MCD', 'TMUS', 'CSCO', 'ACN'
];
const concepts = ["Assets", "StockholdersEquity", "CommonStockDividendsPerShareDeclared", "EarningsPerShareDiluted"];

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [dates, setDates] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [insight, setInsight] = useState('');
  const [selectedConcept, setSelectedConcept] = useState('Assets');
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    fetchVisualization();
    fetchFilingDates();
  }, [ticker, selectedConcept]);

  const fetchVisualization = async () => {
    try {
      const { data } = await axios.get(`http://localhost:5000/api/visualize?ticker=${ticker}&concept=${selectedConcept}`);
      setGraphData(data);
    } catch (error) {
      console.error('Error fetching visualization:', error);
    }
  };

  const fetchFilingDates = async () => {
    try {
      const { data } = await axios.get(`http://localhost:5000/api/filing-dates/${ticker}`);
      setDates(data);
      setSelectedDate(data[0] || '');
    } catch (error) {
      console.error('Error fetching filing dates:', error);
    }
  };

  const fetchInsight = async () => {
    try {
      const { data } = await axios.post('http://localhost:5000/api/filing-insight', { ticker, filing_year: selectedDate });
      setInsight(data);
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  const capitalizeFirstLetter = (sentence) => sentence.charAt(0).toUpperCase() + sentence.slice(1);

  return (
    <div className="dashboard">
      <h2>Sec-Filings Analyzer</h2>
      <Selector options={tickers} value={ticker} onChange={setTicker} label="Select a Company:" />
      <ConceptButtons concepts={concepts} selected={selectedConcept} onSelect={setSelectedConcept} />
      {graphData && <Graph graphData={graphData} />}
      <div className="inline-container">
        <div className="label">Choose Filing Year:</div>
        <DateSelector dates={dates} value={selectedDate} onChange={setSelectedDate} />
        <button className="button" onClick={fetchInsight}>Get Insights</button>
      </div>
      <InsightPanel insight={insight} capitalize={capitalizeFirstLetter} />
    </div>
  );
}

export default App;