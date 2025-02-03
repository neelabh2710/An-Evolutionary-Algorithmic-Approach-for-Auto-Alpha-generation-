from flask import Flask, jsonify, request, Response
import json
from Insight import filing_insight
from Visualise import filing_dates, visualise_filings
from flask_cors import CORS
import plotly.io as pio

app = Flask(__name__)
CORS(app)

@app.route('/api/visualize', methods=['GET'])
def visualize():
    # Retrieve query parameters with default values
    ticker = request.args.get('ticker', default='AAPL')
    concept = request.args.get('concept', default='Assets')

    # Generate a visualization based on the ticker and concept
    fig = visualise_filings(ticker, concept)

    # Convert Plotly figure to JSON for easy transfer over HTTP
    fig_json = pio.to_json(fig)
    return Response(fig_json, mimetype='application/json')

@app.route('/api/filing-dates/<ticker>', methods=['GET'])
def get_filing_dates(ticker):
    # Retrieve filing dates for the given ticker
    dates = filing_dates(ticker)
    return jsonify(dates)

@app.route('/api/filing-insight', methods=['POST'])
def get_filing_insight():
    # Parse JSON data from the request body
    data = request.get_json()
    ticker = data['ticker']
    filing_year = data['filing_year']

    # Retrieve and return insights from the specified filing
    insight = filing_insight(ticker, filing_year)
    return jsonify(insight)

if __name__ == '__main__':
    app.run(debug=True)
