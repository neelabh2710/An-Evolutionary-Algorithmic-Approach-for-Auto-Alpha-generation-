import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


def beautify_plot(df, concept):
    """
    Generate an interactive Plotly graph for time series data of a specified financial concept.

    Args:
    df (DataFrame): The dataframe containing the data.
    concept (str): The financial concept to visualize.

    Returns:
    Plotly Figure: The interactive plot.
    """

    # Filter the data based on the number of years from current year
    def filter_data(df, years):
        if years:
            cutoff_date = datetime.now().year - years
            filtered_df = df[df['end'].dt.year >= cutoff_date]
            return filtered_df
        return df

    # Create a Plotly graph object
    fig = go.Figure()

    # Add traces for various timeframes to the plot
    timeframes = [(5, 'Last 5 Years'), (10, 'Last 10 Years'), (None, 'All Time')]
    for years, name in timeframes:
        filtered_df = filter_data(df, years)
        fig.add_trace(go.Scatter(
            x=filtered_df['end'],
            y=filtered_df['val'],
            mode='markers+lines',
            marker=dict(size=10, color='green'),
            name=name,
            visible=(name == 'Last 5 Years'))  # Default view
        )

    # Update plot layout
    fig.update_layout(
        template='plotly_white',
        title=f"Time Series Plot for {concept} over Time",
        xaxis_title="Date",
        yaxis_title=concept,
        legend_title_text='Time Frame',
        title_x=0.5,
        hovermode='closest',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Define buttons for interactivity
    buttons = [
        {"label": name, "method": "update", "args": [{"visible": [name == frame for _, frame in timeframes]}]}
        for _, name in timeframes
    ]

    # Add dropdown to switch between timeframes
    fig.update_layout(
        updatemenus=[
            dict(type="buttons",
                 direction="down",
                 buttons=buttons,
                 pad={"r": 10, "t": 10},
                 showactive=True,
                 x=0.1,
                 xanchor="left",
                 y=1.1,
                 yanchor="top")
        ]
    )

    return fig


def visualise_filings(ticker, concept):
    """
    Fetch and visualize filing data for a specific ticker and financial concept.

    Args:
    ticker (str): The stock ticker symbol.
    concept (str): The financial concept to visualize.

    Returns:
    Plotly Figure: Interactive plot of the financial concept over time.
    """
    # Set the headers for HTTP requests
    headers = {'User-Agent': "udishj@gmail.com"}

    # Retrieve company tickers and CIK
    companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
    companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')
    companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)
    cik = list(companyData[companyData.ticker == ticker].cik_str)[0]

    # Fetch financial concept data
    companyConcept = requests.get(f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json',
                                  headers=headers)
    unit = list(companyConcept.json()['units'].keys())[0]
    conceptData = pd.DataFrame.from_dict(companyConcept.json()['units'][unit])
    filteredData = conceptData[conceptData.form == '10-Q'].reset_index(drop=True)
    filteredData['end'] = pd.to_datetime(filteredData['end'])

    return beautify_plot(filteredData, concept)


def filing_dates(ticker, concept='Assets'):
    """
    Retrieve filing dates for a specified ticker and concept.

    Args:
    ticker (str): The stock ticker symbol.
    concept (str): The financial concept.

    Returns:
    list: Sorted list of filing dates.
    """
    headers = {'User-Agent': "udishj@gmail.com"}

    # Fetch company data and filter by ticker
    companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
    companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')
    companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)
    cik = list(companyData[companyData.ticker == ticker].cik_str)[0]

    # Fetch and process the concept data
    companyConcept = requests.get(f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json',
                                  headers=headers)
    unit = list(companyConcept.json()['units'].keys())[0]
    conceptData = pd.DataFrame.from_dict(companyConcept.json()['units'][unit])
    filteredData = conceptData[conceptData.form == '10-K'].reset_index(drop=True)
    filteredData['end'] = pd.to_datetime(filteredData['end'])

    dates = sorted(set(filteredData.filed))
    return dates
