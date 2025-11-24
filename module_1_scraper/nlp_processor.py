import nltk
from nltk.corpus import stopwords
from collections import Counter
import re
import os

def download_nltk_resources():
    """Ensures necessary NLTK data files are downloaded."""
    # 🚨 CHANGE THIS LINE: Add 'punkt_tab'
    resources = ['stopwords', 'punkt', 'punkt_tab'] 
    
    for resource in resources:
        try:
            # Note: We keep the check generic to simplify
            nltk.data.find(f'tokenizers/{resource}') 
        except LookupError:
            print(f"Downloading NLTK resource: {resource}...")
            # Some resources require just the name for download
            nltk.download(resource)
            print(f"{resource} downloaded.")

# Run the downloader function right at the start
download_nltk_resources()



# --- Configuration ---
INPUT_FILE = 'raw_complaints.txt'
# ... the rest of the file remains the same ...
OUTPUT_FILE = 'idea_keywords.txt'
COMMON_WORDS_TO_IGNORE = set(stopwords.words('english'))
# Add common domain-specific words that are noise (e.g., the name of the tool we scraped)
COMMON_WORDS_TO_IGNORE.update(['jira', 'atlassian', 'questions', 'ticket', 'problem', 'need', 'issue', 'us', 'get', 'using', 'way', 'how', 'want', 'new'])


def load_complaints(filename):
    """Loads all text complaints from the input file."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        print(f"Error: Input file '{filename}' not found or is empty. Run scraper.py first!")
        return ""
    with open(filename, 'r', encoding='utf-8') as f:
        # Read the whole file and join lines to treat it as one body of text
        return f.read().replace('\n---\n', ' ')

def process_text_and_extract_keywords(text):
    """Cleans the text and finds the most frequent non-stop words."""
    
    # 1. Clean the text: remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    
    # 2. Tokenize: split the text into individual words
    words = nltk.word_tokenize(text)
    
    # 3. Filter: remove short words and stop words
    filtered_words = [
        word for word in words 
        if word not in COMMON_WORDS_TO_IGNORE and len(word) > 2
    ]
    
    # 4. Count frequency
    word_counts = Counter(filtered_words)
    
    # 5. Get the top 20 most common words (our raw SaaS ideas!)
    top_keywords = word_counts.most_common(20)
    
    return top_keywords

def save_keywords(keywords, filename):
    """Saves the top keywords and their counts to a new file."""
    with open(filename, 'w', encoding='utf-8') as f:
        print(f"--- Top {len(keywords)} Pain Points Extracted ---")
        for word, count in keywords:
            line = f"{word}: {count}"
            print(line)
            f.write(line + '\n')

# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Load the data
    all_complaints_text = load_complaints(INPUT_FILE)
    
    if all_complaints_text:
        # 2. Process and extract
        top_ideas = process_text_and_extract_keywords(all_complaints_text)
        
        # 3. Save the results
        save_keywords(top_ideas, OUTPUT_FILE)
        
    print("\nModule 1 NLP execution finished.")