import requests
import json
import os
import praw
from praw.exceptions import PRAWException

# --- Configuration ---
# Target URLs
STACK_EXCHANGE_URL = 'https://api.stackexchange.com/2.3/questions?pagesize=50&order=desc&sort=hot&tagged=jira&site=stackoverflow' 
REDDIT_SUBREDDITS = ['saas', 'startups', 'webdev', 'programming'] # Subreddits to scan
OUTPUT_FILE = 'raw_complaints.txt'

# --- Reddit API Configuration (UPDATED FOR READ-ONLY ACCESS) ---
# Since you cannot create a developer app, we will use empty credentials. 
# PRAW will attempt to use read-only mode, identified by the User Agent.
REDDIT_CLIENT_ID = '' 
REDDIT_SECRET = ''
REDDIT_USER_AGENT = 'SaaS_Idea_Finder_Script_v1.0 (by /u/FluffyAssignment304)' 
# IMPORTANT: Replace YOUR_REDDIT_USERNAME above with your actual Reddit username. 
# This is required for ethical scraping and API identification.

def fetch_stack_exchange_data(url):
    """Fetches question titles from the Stack Exchange API."""
    print(f"-> 1. Fetching data from Stack Exchange API...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        titles = [item['title'] for item in data.get('items', [])]
        print(f"-> Found {len(titles)} titles from Stack Exchange.")
        return titles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Stack Exchange data: {e}")
        return []

def fetch_reddit_data(subreddits):
    """Fetches submission titles from specified subreddits using PRAW."""
    print(f"-> 2. Fetching data from Reddit (Subreddits: {', '.join(subreddits)})...")
    
    # We attempt to initialize PRAW without Client ID/Secret, relying on the User Agent.
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        
        # Test if read-only is working (it should be True if successful)
        if not reddit.read_only:
             print("Warning: PRAW may not be in read-only mode. If scraping fails, you must contact Reddit support.")

        all_titles = []
        for sub in subreddits:
            # Search for 'problem', 'frustrated', 'help' in the subreddits' hot submissions
            subreddit = reddit.subreddit(sub)
            for submission in subreddit.hot(limit=20):
                # Filter for text that indicates a struggle or problem (high value for SaaS ideas)
                if 'problem' in submission.title.lower() or 'struggle' in submission.title.lower() or 'frustrated' in submission.title.lower():
                     all_titles.append(submission.title)
        
        print(f"-> Found {len(all_titles)} titles from Reddit.")
        return all_titles
        
    except PRAWException as e:
        # This will catch errors like "Missing: client_id" if read-only mode fails
        print(f"Error fetching Reddit data (PRAW). The read-only mode failed: {e}")
        print("Please ensure your User Agent is unique and try again, or you will need to contact Reddit support.")
        return []
    except Exception as e:
         print(f"General error during Reddit fetch: {e}")
         return []

def save_complaints(complaints, filename):
    """Saves the combined list of extracted complaints to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for complaint in complaints:
            f.write(complaint + '\n---\n') 
    print(f"\n✅ Successfully saved {len(complaints)} complaints to {filename}")


# --- Main Execution ---
if __name__ == "__main__":
    
    print("--- Module 1: Multi-Source Data Collection Initiated ---")
    
    # 1. Fetch data from Stack Exchange
    stack_complaints = fetch_stack_exchange_data(STACK_EXCHANGE_URL)
    
    # 2. Fetch data from Reddit
    reddit_complaints = fetch_reddit_data(REDDIT_SUBREDDITS)
    
    # 3. Combine both data sources
    all_complaints_list = stack_complaints + reddit_complaints
    
    # 4. Save the combined results
    save_complaints(all_complaints_list, OUTPUT_FILE)
        
    print("\nModule 1 Data Collection finished.")