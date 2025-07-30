"""
Stock Price Fetcher using Financial Modeling Prep API (Free Tier)

This implementation uses Financial Modeling Prep which offers limited
free access without requiring registration for basic quotes.
"""

import requests
import json
from datetime import datetime, timedelta
import time

class FMPStockFetcher:
    def __init__(self):
        """
        Initialize the Financial Modeling Prep Stock Fetcher
        Uses free tier - no API key required for basic quotes!
        """
        self.base_url = "https://financialmodelingprep.com/api/v3"
        
        # Headers to mimic a browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
    
    def get_quote(self, symbol):
        """
        Get real-time quote for a stock symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            dict: Stock quote data or None if error
        """
        try:
            url = f"{self.base_url}/quote/{symbol.upper()}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                quote = data[0]
                
                # Format the data to match Alpha Vantage structure
                change_percent = f"{quote.get('changesPercentage', 0):.2f}%"
                
                formatted_quote = {
                    '01. symbol': quote.get('symbol', ''),
                    '02. open': str(quote.get('open', 0)),
                    '03. high': str(quote.get('dayHigh', 0)),
                    '04. low': str(quote.get('dayLow', 0)),
                    '05. price': str(quote.get('price', 0)),
                    '06. volume': str(quote.get('volume', 0)),
                    '07. latest trading day': datetime.now().strftime('%Y-%m-%d'),
                    '08. previous close': str(quote.get('previousClose', 0)),
                    '09. change': str(quote.get('change', 0)),
                    '10. change percent': change_percent
                }
                
                return formatted_quote
                
        except Exception as e:
            print(f"Error fetching quote: {e}")
            return None
    
    def search_symbol(self, keywords):
        """
        Search for stock symbols by company name or keywords
        
        Args:
            keywords (str): Company name or keywords to search
            
        Returns:
            list: List of matching stocks or None if error
        """
        try:
            url = f"{self.base_url}/search"
            params = {'query': keywords, 'limit': 10}
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data:
                results = []
                for item in data:
                    results.append({
                        '1. symbol': item.get('symbol', ''),
                        '2. name': item.get('name', ''),
                        '3. type': 'Stock',
                        '4. region': item.get('exchangeShortName', 'US'),
                        '5. currency': item.get('currency', 'USD')
                    })
                
                return results
                
        except Exception as e:
            print(f"Error searching symbols: {e}")
            return None
    
    def get_daily_data(self, symbol, days=30):
        """
        Get historical daily data for a stock symbol
        
        Args:
            symbol (str): Stock symbol
            days (int): Number of days of historical data
            
        Returns:
            dict: Historical data or None if error
        """
        try:
            url = f"{self.base_url}/historical-price-full/{symbol.upper()}"
            params = {'timeseries': days}
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if 'historical' in data:
                historical = data['historical']
                
                # Format data to match Alpha Vantage structure
                time_series = {}
                for day in historical:
                    date = day['date']
                    time_series[date] = {
                        '1. open': str(day.get('open', 0)),
                        '2. high': str(day.get('high', 0)),
                        '3. low': str(day.get('low', 0)),
                        '4. close': str(day.get('close', 0)),
                        '5. volume': str(day.get('volume', 0))
                    }
                
                return {
                    'Meta Data': {
                        '1. Information': 'Daily Prices (open, high, low, close) and Volumes',
                        '2. Symbol': symbol.upper(),
                        '3. Last Refreshed': max(time_series.keys()) if time_series else datetime.now().strftime('%Y-%m-%d'),
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
    Main function to demonstrate the FMP Stock Fetcher
    """
    print("📈 Financial Modeling Prep Stock Price Fetcher")
    print("=" * 50)
    print("✅ No API key required for basic quotes!")
    print()
    
    # Initialize the fetcher
    fetcher = FMPStockFetcher()
    
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
            print("\n👋 Thanks for using the FMP Stock Fetcher!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")
        
        # Small delay to be respectful
        time.sleep(0.5)

if __name__ == "__main__":
    main()
