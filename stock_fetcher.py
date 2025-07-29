"""
Simple Stock Price Fetcher using Alpha Vantage API

This script demonstrates how to fetch real-time and historical stock data
using the Alpha Vantage API.

Author: GitHub Copilot
Date: July 29, 2025
"""

import requests
import json
from datetime import datetime
import time

class StockFetcher:
    def __init__(self, api_key):
        """
        Initialize the StockFetcher with your Alpha Vantage API key
        
        Args:
            api_key (str): Your Alpha Vantage API key
        """
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_quote(self, symbol):
        """
        Get real-time quote for a stock symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            dict: Stock quote data or None if error
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check if we got valid data
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': quote.get('01. symbol', 'N/A'),
                    'price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', 'N/A'),
                    'volume': int(quote.get('06. volume', 0)),
                    'latest_trading_day': quote.get('07. latest trading day', 'N/A'),
                    'previous_close': float(quote.get('08. previous close', 0)),
                    'open': float(quote.get('02. open', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0))
                }
            else:
                print(f"Error: {data}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except ValueError as e:
            print(f"JSON decode error: {e}")
            return None
    
    def get_daily_data(self, symbol, outputsize='compact'):
        """
        Get daily historical data for a stock
        
        Args:
            symbol (str): Stock symbol
            outputsize (str): 'compact' (last 100 days) or 'full' (20+ years)
            
        Returns:
            dict: Historical data or None if error
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                return data
            else:
                print(f"Error: {data}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
    
    def search_symbol(self, keywords):
        """
        Search for stock symbols by company name or keywords
        
        Args:
            keywords (str): Search terms
            
        Returns:
            list: List of matching symbols
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'bestMatches' in data:
                return data['bestMatches']
            else:
                print(f"Error: {data}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return []

def format_quote_display(quote_data):
    """
    Format quote data for nice display
    
    Args:
        quote_data (dict): Quote data from get_quote()
        
    Returns:
        str: Formatted string for display
    """
    if not quote_data:
        return "No data available"
    
    change_sign = "+" if quote_data['change'] >= 0 else ""
    
    return f"""
📈 Stock Quote for {quote_data['symbol']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Current Price: ${quote_data['price']:.2f}
📊 Change: {change_sign}{quote_data['change']:.2f} ({quote_data['change_percent']})
📅 Trading Day: {quote_data['latest_trading_day']}
🔓 Open: ${quote_data['open']:.2f}
📈 High: ${quote_data['high']:.2f}
📉 Low: ${quote_data['low']:.2f}
🔒 Previous Close: ${quote_data['previous_close']:.2f}
📦 Volume: {quote_data['volume']:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def main():
    """
    Main function to demonstrate the stock fetcher
    """
    print("🚀 Welcome to the Simple Stock Price Fetcher!")
    print("=" * 50)
    
    # You need to get a free API key from: https://www.alphavantage.co/support/#api-key
    api_key = input("Enter your Alpha Vantage API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Please get one from https://www.alphavantage.co/support/#api-key")
        return
    
    # Create fetcher instance
    fetcher = StockFetcher(api_key)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Get stock quote")
        print("2. Search for stock symbols")
        print("3. Get historical data (last 5 days)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL, GOOGL, TSLA): ").strip().upper()
            print(f"\n🔍 Fetching quote for {symbol}...")
            
            quote = fetcher.get_quote(symbol)
            if quote:
                print(format_quote_display(quote))
            else:
                print("❌ Failed to fetch quote. Please check the symbol and try again.")
                
        elif choice == '2':
            keywords = input("Enter company name or keywords: ").strip()
            print(f"\n🔍 Searching for '{keywords}'...")
            
            results = fetcher.search_symbol(keywords)
            if results:
                print(f"\n📋 Found {len(results)} results:")
                print("-" * 80)
                for i, result in enumerate(results[:10], 1):  # Show top 10
                    print(f"{i:2d}. {result['1. symbol']:8s} - {result['2. name']}")
                    print(f"     Type: {result['3. type']:15s} Region: {result['4. region']}")
                    print()
            else:
                print("❌ No results found.")
                
        elif choice == '3':
            symbol = input("Enter stock symbol: ").strip().upper()
            print(f"\n🔍 Fetching historical data for {symbol}...")
            
            data = fetcher.get_daily_data(symbol)
            if data and 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                dates = sorted(time_series.keys(), reverse=True)[:5]  # Last 5 days
                
                print(f"\n📊 Last 5 trading days for {symbol}:")
                print("-" * 60)
                print(f"{'Date':12s} {'Open':>8s} {'High':>8s} {'Low':>8s} {'Close':>8s} {'Volume':>12s}")
                print("-" * 60)
                
                for date in dates:
                    day_data = time_series[date]
                    print(f"{date:12s} "
                          f"{float(day_data['1. open']):8.2f} "
                          f"{float(day_data['2. high']):8.2f} "
                          f"{float(day_data['3. low']):8.2f} "
                          f"{float(day_data['4. close']):8.2f} "
                          f"{int(day_data['5. volume']):12,d}")
            else:
                print("❌ Failed to fetch historical data.")
                
        elif choice == '4':
            print("\n👋 Thanks for using the Stock Price Fetcher!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")
        
        # Add a small delay to respect API rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
