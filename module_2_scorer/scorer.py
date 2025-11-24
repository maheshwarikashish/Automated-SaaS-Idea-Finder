import pandas as pd
import random
import time
import os

# --- Configuration ---
INPUT_FILE = 'idea_keywords.txt'
OUTPUT_FILE = 'scored_ideas.csv'

def load_keywords(filename):
    """Loads keywords from the text file into a list."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        print(f"Error: Keyword file '{filename}' not found or is empty. Run Module 1 first!")
        return []
        
    keywords = []
    with open(filename, 'r') as f:
        for line in f:
            # Extract just the keyword (ignoring the count)
            keyword = line.split(':')[0].strip()
            keywords.append(keyword)
    return keywords

def simulate_market_analysis(keyword):
    """
    SIMULATED FUNCTION: Replaces API calls to Google Trends (Demand) 
    and Google Search (Competition).
    
    In a real app, this function would use pytrends and a search API.
    """
    # 1. Demand (Search Volume / Trends): Scale 1 to 100
    # High score means high search interest (Good Demand)
    demand_score = random.randint(30, 95) 

    # 2. Competition (Number of existing software products): Scale 1 to 100
    # Low score means low competition (Good Competition)
    # Give 'apis' a slightly higher, but not dominant, score for realism
    if keyword == 'apis':
        competition_score = random.randint(60, 85) # Simulating medium-high competition
    else:
        competition_score = random.randint(10, 70) # Simulating a range of lower competition
    
    # Pause to simulate API request time (good practice)
    time.sleep(0.5) 
    
    print(f"-> Analyzed '{keyword}': Demand={demand_score}, Competition={competition_score}")
    
    return demand_score, competition_score

def score_ideas(keywords):
    """Applies market analysis and calculates the Opportunity Score."""
    
    results = []
    
    for keyword in keywords:
        demand, competition = simulate_market_analysis(keyword)
        
        # --- The Scoring Formula (The Magic) ---
        # Opportunity Score = (Demand Score) * (100 - Competition Score)
        # We multiply Demand by the INVERSE of Competition.
        # High score means High Demand AND Low Competition.
        
        opportunity_score = int(demand * ((100 - competition) / 100))

        results.append({
            'Idea': keyword,
            'Demand_Score (Search Trend)': demand,
            'Competition_Score (0-100)': competition,
            'Opportunity_Score': opportunity_score
        })
        
    # Create a Pandas DataFrame for easy sorting and saving
    df = pd.DataFrame(results)
    
    # Sort by the final Opportunity Score
    df_sorted = df.sort_values(by='Opportunity_Score', ascending=False)
    
    return df_sorted

# --- Main Execution ---
if __name__ == "__main__":
    
    print("--- Module 2: Market Analysis & Scoring ---")
    
    # 1. Load keywords from Module 1
    ideas = load_keywords(INPUT_FILE)
    
    if ideas:
        # 2. Score the ideas
        scored_df = score_ideas(ideas)
        
        # 3. Save the results
        scored_df.to_csv(OUTPUT_FILE, index=False)
        
        print(f"\n✅ Analysis Complete! Results saved to '{OUTPUT_FILE}'")
        print("\n--- Top Scored Ideas ---")
        print(scored_df)
        
    print("\nModule 2 execution finished.")