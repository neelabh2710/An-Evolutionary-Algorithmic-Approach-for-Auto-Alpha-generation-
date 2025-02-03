from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings
import sec_parser as sp
from sec_parser.semantic_elements.semantic_elements import TextElement
from sec_parser.semantic_elements.top_section_title import TopSectionTitle
from sec_parser.semantic_elements.title_element import TitleElement
import warnings
import pandas as pd
import re

def create_dataframe(ticker, elements, acc_num, file_date):
    """
    Create a pandas DataFrame from parsed SEC filing elements.

    Args:
        ticker (str): The stock ticker symbol.
        elements (list): Parsed elements from the SEC filing.
        acc_num (str): The accession number of the filing.
        file_date (str): The filing date.

    Returns:
        DataFrame: The DataFrame containing filing details.
    """
    # Initialize a dictionary to hold the filing data
    data = {
        'ticker': ticker,
        'form_type': '10-K',
        'accession_number': acc_num,
        'filing_date': file_date
    }

    # Variables to manage current section and text appending
    current_section = None
    append_next_title = False

    # Process each element to build the section and content
    for element in elements:
        if isinstance(element, (TopSectionTitle, TitleElement)):
            text = element.text.strip()
            upper_text = text.upper()

            # Determine if the text indicates a new section
            if "ITEM" in upper_text and len(text) < 100:
                if text.endswith('.'):
                    current_section = text
                    append_next_title = True
                else:
                    current_section = text
                    data[current_section] = ''
                    append_next_title = False
            elif append_next_title and element.text.isupper():
                current_section += " " + text
                data[current_section] = ''
                append_next_title = False
            else:
                append_next_title = False

        elif isinstance(element, TextElement):
            if current_section:
                if current_section not in data:
                    data[current_section] = ''
                data[current_section] += element.text.strip() + ' '

    # Convert the dictionary to a DataFrame and clean column names
    df = pd.DataFrame([data])
    df.columns = [re.sub(r'\s+', ' ', col).strip() for col in df.columns]

    return df

def get_filing_data(ticker, years):
    """
    Retrieve SEC filing data for a specific ticker and time period.

    Args:
        ticker (str): The stock ticker symbol.
        years (int): Number of years of filings to retrieve.

    Returns:
        DataFrame: The DataFrame containing consolidated filing data.
    """
    email = "udishj@gmail.com"
    dl = Downloader("Company", email)
    df = pd.DataFrame()

    # Retrieve metadata for filings
    metadatas = dl.get_filing_metadatas(RequestedFilings(ticker_or_cik=ticker, form_type="10-K", limit=years))
    for data in metadatas:
        accesssion_number = data.accession_number
        primary_doc_url = data.primary_doc_url
        filing_date = data.filing_date

        # Download and parse the filing
        html = dl.download_filing(url=primary_doc_url).decode()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Invalid section type for")
            elements = sp.Edgar10QParser().parse(html)
            row = create_dataframe(ticker, elements, accesssion_number, filing_date)
            df = pd.concat([df, row], ignore_index=True)

    return df
