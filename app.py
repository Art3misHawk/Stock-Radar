"""
Flask Web Application for Stock Price Fetcher

This creates a modern web interface for the stock price fetcher.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from stock_fetcher import StockFetcher
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

# Global variable to store the fetcher instance
fetcher = None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """API key setup page"""
    global fetcher
    
    if request.method == 'POST':
        api_key = request.form.get('api_key', '').strip()
        if api_key:
            fetcher = StockFetcher(api_key)
            return redirect(url_for('dashboard'))
        else:
            return render_template('setup.html', error="Please enter a valid API key")
    
    return render_template('setup.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    global fetcher
    if not fetcher:
        return redirect(url_for('setup'))
    return render_template('dashboard.html')

@app.route('/api/quote/<symbol>')
def get_quote_api(symbol):
    """API endpoint to get stock quote"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'API key not configured'}), 400
    
    try:
        quote = fetcher.get_quote(symbol.upper())
        if quote:
            return jsonify(quote)
        else:
            return jsonify({'error': 'Failed to fetch quote'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<keywords>')
def search_api(keywords):
    """API endpoint to search stock symbols"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'API key not configured'}), 400
    
    try:
        results = fetcher.search_symbol(keywords)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/historical/<symbol>')
def historical_api(symbol):
    """API endpoint to get historical data"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'API key not configured'}), 400
    
    try:
        data = fetcher.get_daily_data(symbol.upper())
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to fetch historical data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Run the app
    app.run(debug=debug, host='0.0.0.0', port=port)
