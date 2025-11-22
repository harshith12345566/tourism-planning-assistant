"""
Flask Web Application for Multi-Agent Tourism System

This module provides a web interface for the tourism system.
"""

from flask import Flask, render_template, request, jsonify
from agents.parent_agent import ParentAgent
import sys
import os

# Set Gemini API Key provided by user
os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Allow Unicode in JSON responses

# Initialize the parent agent
parent_agent = ParentAgent()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_place():
    """
    API endpoint to search for tourism information about a place.
    
    Expected JSON payload:
    {
        "place": "Paris"
    }
    
    Returns JSON response with tourism information.
    """
    try:
        data = request.get_json()
        
        if not data or 'place' not in data:
            return jsonify({
                'success': False,
                'error': 'Place name is required'
            }), 400
        
        place_name = data['place'].strip()
        limit = data.get('limit', 5)  # Default to 5 attractions
        
        if not place_name:
            return jsonify({
                'success': False,
                'error': 'Place name cannot be empty'
            }), 400
        
        # Process the place using the parent agent
        result = parent_agent.process_place(place_name, attractions_limit=limit)
        
        # Return the result as JSON
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


