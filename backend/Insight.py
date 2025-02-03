from Parser import get_filing_data
import nltk
from transformers import pipeline

# Download necessary NLTK package for tokenization
nltk.download('punkt')

# Initialize the summarization pipeline with a pre-trained T5 model
summarizer = pipeline('summarization', model='t5-base')

# Define the model for classifying sentiments of text segments
classifier_model_name = 'ProsusAI/finbert'
classifier_emotions = ['positive', 'neutral', 'negative']

# Initialize the classification pipeline with the specified model
classifier = pipeline('text-classification', model=classifier_model_name)

def find_emotional_sentences(text, emotions, threshold):
    """
    Identify and categorize sentences by their emotional tone based on a defined threshold.

    Args:
        text (str): The complete text to analyze.
        emotions (list): List of emotions to detect.
        threshold (float): Minimum confidence level to consider for classification.

    Returns:
        dict: Dictionary of sentences categorized by emotion.
    """
    sentences_by_emotion = {e: [] for e in emotions}
    sentences = nltk.sent_tokenize(text)
    for s in sentences:
        prediction = classifier(s)
        if prediction[0]['label'] != 'neutral' and prediction[0]['score'] > threshold:
            sentences_by_emotion[prediction[0]['label']].append(s)
    return sentences_by_emotion

def summarize_sentences(sentences_by_emotion, min_length, max_length):
    """
    Summarize the sentences categorized by emotion.

    Args:
        sentences_by_emotion (dict): Dictionary of sentences categorized by emotion.
        min_length (int): Minimum length of the summary.
        max_length (int): Maximum length of the summary.

    Returns:
        dict: Dictionary of summaries for each emotion category.
    """
    summaries_by_emotion = {}
    for k, sentences in sentences_by_emotion.items():
        if sentences:
            text = ' '.join(sentences)
            summary = summarizer(text, min_length=min_length, max_length=max_length)
            sentences = [sentence.strip() for sentence in summary[0]['summary_text'].split('.') if sentence]
            summaries_by_emotion[k] = sentences
    return summaries_by_emotion

def filing_insight(ticker, filing_year):
    """
    Generate insights from the filing data for a specific ticker and year.

    Args:
        ticker (str): Stock ticker symbol.
        filing_year (str): Specific year of the filing to analyze.

    Returns:
        dict: Summaries categorized by emotional tone derived from the filing text.
    """
    df10k = get_filing_data(ticker, 30)  # Assuming '30' represents the years of data requested
    # Extract relevant column for analysis
    cols = [col for col in df10k.columns if "ITEM 7." in col.upper()][0]
    text = df10k[df10k['filing_date'] == filing_year].iloc[0][cols]
    sentences_by_emotion = find_emotional_sentences(text, classifier_emotions, 0.9)
    return summarize_sentences(sentences_by_emotion, min_length=30, max_length=200)
