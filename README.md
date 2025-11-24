  Automated SaaS Idea Finder & Scorer

This project is a multi-module pipeline designed to identify high-potential Software as a Service (SaaS) opportunities by scraping real developer pain points from professional forums (Stack Exchange) and community discussions (Reddit), processing them using Natural Language Processing (NLP), and scoring them against real-time market data (Demand and Competition).

 Project Architecture

The system is organized into four distinct modules that run sequentially:

Module 1: Data Collection & NLP (module_1_scraper): Gathers raw text data (complaints, frustrations, problems) from various online developer communities.

Module 2: Scorer (module_2_scorer): Takes the most frequent keywords from the NLP output and scores them using external APIs (Google Trends for Demand, SEMrush/Search for Competition).

Module 3: API (module_3_api): A Flask REST API that serves the final calculated scores from the CSV file.

Module 4: Frontend (module_4_frontend): A React dashboard that visualizes the ranked opportunities.

  Prerequisites

You need Python (with a virtual environment) and Node/npm installed.

Python Dependencies

Ensure you are in your virtual environment (venv) and install all required libraries:

# Navigate to the root of the project
cd saas_idea_finder_project 

# Activate your virtual environment (assuming it's set up)
source venv/bin/activate 

# Install dependencies across all modules
pip install requests pandas praw nltk flask flask-cors


Critical API Setup

1. Reddit User-Agent (Mandatory)

Due to API restrictions, you must identify your scraping script.

Open module_1_scraper/scraper.py.

Replace the placeholder in the REDDIT_USER_AGENT line with your actual Reddit username:

REDDIT_USER_AGENT = 'SaaS_Idea_Finder_Script_v1.0 (by /u/YOUR_REDDIT_USERNAME)' 


(e.g., (by /u/CodeMaster99))

2. Competition/Demand API Keys (Module 2)

The scorer module (module_2_scorer/scorer.py) relies on external tools to get Demand and Competition data. You must configure these API keys (e.g., SEMrush, Google Trends) within scorer.py before running Module 2.

🏃 How to Run the Pipeline

The modules must be executed in order (1 → 2 → 3), and then the React front-end (4) can be viewed.

1. Data Collection & NLP (Module 1)

This step scrapes the data and extracts the initial keywords.

# Step 1a: Run the Scraper
cd module_1_scraper
python3 scraper.py
# This creates raw_complaints.txt and tries to scrape Reddit/StackExchange.

# Step 1b: Run the NLP Processor
python3 nlp_processor.py
# This reads the raw data and creates idea_keywords.txt


2. Scoring (Module 2)

This step calculates the final Opportunity Score for each keyword.

# Step 2a: Move the keywords to the scorer module
cp idea_keywords.txt ../module_2_scorer/

# Step 2b: Run the Scorer
cd ../module_2_scorer
python3 scorer.py
# This creates opportunity_scores.csv (Requires API keys configured in scorer.py)


3. API & Frontend (Modules 3 & 4)

This step starts the backend server and displays the results in the web dashboard.

# Step 3: Start the Flask API
cd ../module_3_api
python3 app.py
# The server will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)

# Step 4: View the Dashboard (Module 4 - React)
# The React application is available in the browser preview.
# It automatically fetches the data from the running Flask API.


  Git Management

The following files and directories are automatically ignored to prevent committing sensitive data and large build artifacts (as defined in .gitignore):

Sensitive Data: raw_complaints.txt, idea_keywords.txt, opportunity_scores.csv

Environment: venv/, __pycache__/

Build Artifacts: node_modules/, build/
