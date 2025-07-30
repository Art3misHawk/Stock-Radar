"""
Stock Price Fetcher using Yahoo Finance (No API Key Required)

This implementation uses Yahoo Finance which provides free stock data
without requiring an API key.
"""

import requests
import json
from datetime import datetime, timedelta
import time
import re

class YahooStockFetcher:
    def __init__(self):
        """
        Initialize the Yahoo Finance Stock Fetcher
        No API key required!
        """
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.search_url = "https://query2.finance.yahoo.com/v1/finance/search"
        self.quote_url = "https://query1.finance.yahoo.com/v7/finance/quote"
        
        # Headers to mimic a browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://finance.yahoo.com/',
        }
    
    def get_quote(self, symbol):
        """
        Get real-time quote for a stock symbol using Yahoo Finance
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            dict: Stock quote data or None if error
        """
        try:
            # Use the chart endpoint which is more reliable
            url = f"{self.base_url}/{symbol.upper()}"
            params = {
                'period1': int((datetime.now() - timedelta(days=2)).timestamp()),
                'period2': int(datetime.now().timestamp()),
                'interval': '1d',
                'includePrePost': 'true'
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                # Get the most recent data
                timestamps = result['timestamp']
                quotes = result['indicators']['quote'][0]
                
                if timestamps and len(timestamps) > 0:
                    latest_idx = -1
                    
                    # Format the data to match Alpha Vantage structure
                    current_price = meta.get('regularMarketPrice', quotes['close'][latest_idx])
                    previous_close = meta.get('previousClose', quotes['close'][-2] if len(quotes['close']) > 1 else current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close * 100) if previous_close != 0 else 0
                    
                    formatted_quote = {
                        '01. symbol': symbol.upper(),
                        '02. open': str(quotes['open'][latest_idx] or meta.get('regularMarketOpen', 0)),
                        '03. high': str(quotes['high'][latest_idx] or meta.get('regularMarketDayHigh', 0)),
                        '04. low': str(quotes['low'][latest_idx] or meta.get('regularMarketDayLow', 0)),
                        '05. price': str(current_price),
                        '06. volume': str(quotes['volume'][latest_idx] or meta.get('regularMarketVolume', 0)),
                        '07. latest trading day': datetime.fromtimestamp(timestamps[latest_idx]).strftime('%Y-%m-%d'),
                        '08. previous close': str(previous_close),
                        '09. change': str(change),
                        '10. change percent': f"{change_percent:.2f}%"
                    }
                    
                    return formatted_quote
                    
        except Exception as e:
            print(f"Error fetching quote: {e}")
            return None
    
    def search_symbol(self, keywords):
        """
        Search for stock symbols by company name or keywords
        Note: Yahoo Finance search API is limited, this is a basic implementation
        
        Args:
            keywords (str): Company name or keywords to search
            
        Returns:
            list: List of matching stocks or None if error
        """
        try:
            # Use a simple lookup for common stocks as Yahoo's search API is restricted
            common_stocks = {
                'apple': [{'symbol': 'AAPL', 'name': 'Apple Inc.'}],
                'microsoft': [{'symbol': 'MSFT', 'name': 'Microsoft Corporation'}],
                'google': [{'symbol': 'GOOGL', 'name': 'Alphabet Inc. Class A'}, {'symbol': 'GOOG', 'name': 'Alphabet Inc. Class C'}],
                'alphabet': [{'symbol': 'GOOGL', 'name': 'Alphabet Inc. Class A'}, {'symbol': 'GOOG', 'name': 'Alphabet Inc. Class C'}],
                'amazon': [{'symbol': 'AMZN', 'name': 'Amazon.com Inc.'}],
                'tesla': [{'symbol': 'TSLA', 'name': 'Tesla, Inc.'}],
                'meta': [{'symbol': 'META', 'name': 'Meta Platforms, Inc.'}],
                'facebook': [{'symbol': 'META', 'name': 'Meta Platforms, Inc.'}],
                'netflix': [{'symbol': 'NFLX', 'name': 'Netflix, Inc.'}],
                'nvidia': [{'symbol': 'NVDA', 'name': 'NVIDIA Corporation'}],
                'intel': [{'symbol': 'INTC', 'name': 'Intel Corporation'}],
                'amd': [{'symbol': 'AMD', 'name': 'Advanced Micro Devices, Inc.'}],
                'ibm': [{'symbol': 'IBM', 'name': 'International Business Machines Corporation'}],
                'oracle': [{'symbol': 'ORCL', 'name': 'Oracle Corporation'}],
                'salesforce': [{'symbol': 'CRM', 'name': 'Salesforce, Inc.'}],
                'disney': [{'symbol': 'DIS', 'name': 'The Walt Disney Company'}],
                'coca cola': [{'symbol': 'KO', 'name': 'The Coca-Cola Company'}],
                'pepsi': [{'symbol': 'PEP', 'name': 'PepsiCo, Inc.'}],
                'walmart': [{'symbol': 'WMT', 'name': 'Walmart Inc.'}],
                'home depot': [{'symbol': 'HD', 'name': 'The Home Depot, Inc.'}],
                'visa': [{'symbol': 'V', 'name': 'Visa Inc.'}],
                'mastercard': [{'symbol': 'MA', 'name': 'Mastercard Incorporated'}],
                'jpmorgan': [{'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'}],
                'bank of america': [{'symbol': 'BAC', 'name': 'Bank of America Corporation'}],
                'wells fargo': [{'symbol': 'WFC', 'name': 'Wells Fargo & Company'}],
                'goldman sachs': [{'symbol': 'GS', 'name': 'The Goldman Sachs Group, Inc.'}],
                'johnson': [{'symbol': 'JNJ', 'name': 'Johnson & Johnson'}],
                'pfizer': [{'symbol': 'PFE', 'name': 'Pfizer Inc.'}],
                'merck': [{'symbol': 'MRK', 'name': 'Merck & Co., Inc.'}],
                'exxon': [{'symbol': 'XOM', 'name': 'Exxon Mobil Corporation'}],
                'chevron': [{'symbol': 'CVX', 'name': 'Chevron Corporation'}],
                'boeing': [{'symbol': 'BA', 'name': 'The Boeing Company'}]
            }
            
            keywords_lower = keywords.lower()
            results = []
            
            # Search for matching companies
            for company, stocks in common_stocks.items():
                if keywords_lower in company or company in keywords_lower:
                    for stock in stocks:
                        results.append({
                            '1. symbol': stock['symbol'],
                            '2. name': stock['name'],
                            '3. type': 'Stock',
                            '4. region': 'US',
                            '5. currency': 'USD'
                        })
            
            # If exact symbol match, add it
            if keywords.upper() in [stock['symbol'] for stocks in common_stocks.values() for stock in stocks]:
                # It's already in the results
                pass
            elif len(keywords) <= 5 and keywords.isalpha():
                # Assume it's a symbol and try to get quote to verify
                test_quote = self.get_quote(keywords.upper())
                if test_quote:
                    results.insert(0, {
                        '1. symbol': keywords.upper(),
                        '2. name': f'{keywords.upper()} Corporation',
                        '3. type': 'Stock',
                        '4. region': 'US',
                        '5. currency': 'USD'
                    })
            
            return results[:10] if results else None
            
        except Exception as e:
            print(f"Error searching symbols: {e}")
            return None
    
    def get_daily_data(self, symbol, period='1mo'):
        """
        Get historical daily data for a stock symbol
        
        Args:
            symbol (str): Stock symbol
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            
        Returns:
            dict: Historical data or None if error
        """
        try:
            params = {
                'symbol': symbol.upper(),
                'period1': int((datetime.now() - timedelta(days=30)).timestamp()),
                'period2': int(datetime.now().timestamp()),
                'interval': '1d',
                'includePrePost': 'true',
                'events': 'div,splits'
            }
            
            response = requests.get(f"{self.base_url}/{symbol.upper()}", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                timestamps = result['timestamp']
                quotes = result['indicators']['quote'][0]
                
                # Format data to match Alpha Vantage structure
                time_series = {}
                for i, timestamp in enumerate(timestamps):
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    time_series[date] = {
                        '1. open': str(quotes['open'][i] or 0),
                        '2. high': str(quotes['high'][i] or 0),
                        '3. low': str(quotes['low'][i] or 0),
                        '4. close': str(quotes['close'][i] or 0),
                        '5. volume': str(quotes['volume'][i] or 0)
                    }
                
                return {
                    'Meta Data': {
                        '1. Information': 'Daily Prices (open, high, low, close) and Volumes',
                        '2. Symbol': symbol.upper(),
                        '3. Last Refreshed': max(time_series.keys()),
                        '4. Output Size': 'Compact',
                        '5. Time Zone': 'US/Eastern'
                    },
                    'Time Series (Daily)': time_series
                }
                
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None


def main():
    """
    Main function to demonstrate the Yahoo Finance Stock Fetcher
    """
    print("📈 Yahoo Finance Stock Price Fetcher")
    print("=" * 50)
    print("✅ No API key required!")
    print()
    
    # Initialize the fetcher
    fetcher = YahooStockFetcher()
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Get stock quote")
        print("2. Search stock symbols")
        print("3. Get historical data")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
            print(f"\n🔍 Fetching quote for {symbol}...")
            
            quote = fetcher.get_quote(symbol)
            if quote:
                print(f"\n💹 {quote['01. symbol']} Stock Quote")
                print("-" * 40)
                print(f"💰 Current Price: ${float(quote['05. price']):.2f}")
                print(f"📈 Daily Change: ${float(quote['09. change']):.2f} ({quote['10. change percent']})")
                print(f"📊 Open: ${float(quote['02. open']):.2f}")
                print(f"📊 High: ${float(quote['03. high']):.2f}")
                print(f"📊 Low: ${float(quote['04. low']):.2f}")
                print(f"📊 Previous Close: ${float(quote['08. previous close']):.2f}")
                print(f"📊 Volume: {int(quote['06. volume']):,}")
                print(f"📅 Last Updated: {quote['07. latest trading day']}")
            else:
                print("❌ Failed to fetch quote. Please check the symbol and try again.")
                
        elif choice == '2':
            keywords = input("Enter company name or keywords: ").strip()
            print(f"\n🔍 Searching for '{keywords}'...")
            
            results = fetcher.search_symbol(keywords)
            if results:
                print(f"\n📋 Found {len(results)} results:")
                print("-" * 80)
                for i, result in enumerate(results, 1):
                    print(f"{i:2d}. {result['1. symbol']:8s} - {result['2. name']}")
                    print(f"     Type: {result['3. type']:15s} Exchange: {result['4. region']}")
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
            print("\n👋 Thanks for using the Yahoo Finance Stock Fetcher!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")
        
        # Small delay to be respectful
        time.sleep(0.5)

if __name__ == "__main__":
    main()
