# ingestion/utils.py

def extract_keywords(text):
    """
    A simple keyword extraction: returns the first 10 unique words.
    For more advanced extraction, consider integrating with an NLP library.
    """
    words = text.split()
    unique_words = list(dict.fromkeys(words))  # Preserves order and removes duplicates
    return unique_words[:10]
