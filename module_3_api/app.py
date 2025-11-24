from flask import Flask, jsonify
import pandas as pd
import os
from flask_cors import CORS # 1. Import the CORS module

# Create the Flask application instance
app = Flask(__name__)

# 2. Initialize CORS
# This allows ANY origin (*) to access your API endpoints. 
# For a production app, you would restrict this to your specific frontend domain.
CORS(app)
# File path for the scored ideas data
DATA_FILE = 'scored_ideas.csv'

def load_data():
    """Loads the scored ideas from the CSV file into a dictionary list."""
    if not os.path.exists(DATA_FILE):
        return {"error": "Data file not found. Run Module 2 first."}, 500
    
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(DATA_FILE)
    
    # Convert the DataFrame rows into a list of dictionaries (JSON format)
    # The 'index' and 'header' arguments specify how the data is oriented
    data_list = df.to_dict(orient='records')
    
    return data_list, 200

@app.route('/api/v1/ideas', methods=['GET'])
def get_ideas():
    """API endpoint to return the list of scored SaaS ideas."""
    data, status = load_data()
    
    if status != 200:
        return jsonify(data), status
    
    # Return the data as a JSON response
    return jsonify({
        "status": "success",
        "total_ideas": len(data),
        "ideas": data
    })

# Run the application
if __name__ == '__main__':
    print(f"--- Module 3: Backend API Running ---")
    print(f"Data Source: {os.path.abspath(DATA_FILE)}")
    # Run Flask in debug mode for development
    app.run(debug=True)