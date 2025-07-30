"""
Flask Web Application for Stock Price Fetcher

This creates a modern web interface for the stock price fetcher.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from unified_stock_fetcher import UnifiedStockFetcher
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
        provider = request.form.get('provider', 'yahoo').strip()
        api_key = request.form.get('api_key', '').strip()
        
        try:
            if provider in ['yahoo', 'fmp']:
                # No API key required for these providers
                fetcher = UnifiedStockFetcher(provider)
            elif provider == 'alphavantage':
                if not api_key:
                    return render_template('setup.html', error="API key is required for Alpha Vantage")
                fetcher = UnifiedStockFetcher(provider, api_key)
            else:
                return render_template('setup.html', error="Invalid provider selected")
                
            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('setup.html', error=f"Setup failed: {str(e)}")
    
    return render_template('setup.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    global fetcher
    if not fetcher:
        return redirect(url_for('setup'))
    
    # Add provider info to template context
    provider_info = fetcher.get_provider_info() if hasattr(fetcher, 'get_provider_info') else {}
    return render_template('dashboard.html', provider_info=provider_info)

@app.route('/api/quote/<symbol>')
def get_quote_api(symbol):
    """API endpoint to get stock quote"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'Data provider not configured. Please visit the setup page.'}), 400
    
    try:
        print(f"API: Fetching quote for {symbol}")
        quote = fetcher.get_quote(symbol.upper())
        if quote:
            print(f"API: Successfully fetched {symbol} quote")
            return jsonify(quote)
        else:
            print(f"API: Failed to fetch quote for {symbol}")
            return jsonify({'error': f'Unable to fetch quote for {symbol}. Please try again.'}), 404
    except Exception as e:
        print(f"API: Exception while fetching {symbol}: {e}")
        return jsonify({'error': f'Network error while fetching {symbol}. Please check your connection and try again.'}), 500

@app.route('/api/search/<keywords>')
def search_api(keywords):
    """API endpoint to search stock symbols"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'Data provider not configured. Please visit the setup page.'}), 400
    
    try:
        print(f"API: Searching for '{keywords}'")
        results = fetcher.search_symbol(keywords)
        if results:
            print(f"API: Found {len(results)} results for '{keywords}'")
            return jsonify(results)
        else:
            print(f"API: No results found for '{keywords}'")
            return jsonify([])  # Return empty array instead of error
    except Exception as e:
        print(f"API: Exception while searching '{keywords}': {e}")
        return jsonify({'error': f'Network error while searching. Please try again.'}), 500

@app.route('/api/historical/<symbol>')
def historical_api(symbol):
    """API endpoint to get historical data"""
    global fetcher
    if not fetcher:
        return jsonify({'error': 'Data provider not configured. Please visit the setup page.'}), 400
    
    try:
        print(f"API: Fetching historical data for {symbol}")
        data = fetcher.get_daily_data(symbol.upper())
        if data:
            print(f"API: Successfully fetched historical data for {symbol}")
            return jsonify(data)
        else:
            print(f"API: Failed to fetch historical data for {symbol}")
            return jsonify({'error': f'Unable to fetch historical data for {symbol}. Please try again.'}), 404
    except Exception as e:
        print(f"API: Exception while fetching historical data for {symbol}: {e}")
        return jsonify({'error': f'Network error while fetching historical data. Please try again.'}), 500

@app.route('/api/status')
def status_api():
    """API endpoint to get system status"""
    global fetcher
    if not fetcher:
        return jsonify({
            'status': 'not_configured',
            'message': 'Data provider not configured',
            'provider': None
        })
    
    try:
        provider_info = fetcher.get_provider_info() if hasattr(fetcher, 'get_provider_info') else {}
        return jsonify({
            'status': 'ready',
            'message': 'Stock Radar is ready to fetch data',
            'provider': provider_info.get('name', 'Unknown'),
            'requires_api_key': provider_info.get('requires_api_key', False),
            'data_source': 'Live data when available, market simulation during rate limits'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'System error: {str(e)}',
            'provider': None
        })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Run the app
    app.run(debug=debug, host='0.0.0.0', port=port)
