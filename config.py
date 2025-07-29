"""
Configuration file for the Stock Price Fetcher

Instructions:
1. Get your free API key from: https://www.alphavantage.co/support/#api-key
2. Replace 'YOUR_API_KEY_HERE' with your actual API key
3. Save this file
"""

# Replace this with your actual Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"

# API Configuration
BASE_URL = "https://www.alphavantage.co/query"

# Rate limiting (free tier allows 5 requests per minute, 25 per day)
REQUESTS_PER_MINUTE = 5
REQUESTS_PER_DAY = 25

# Default delay between requests (in seconds)
DEFAULT_DELAY = 1
