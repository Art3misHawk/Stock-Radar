"""
Unified Stock Price Fetcher with Multiple Data Sources

This module provides a unified interface to fetch stock data from multiple sources,
including both API-key-required and API-key-free options.
"""

from yahoo_stock_fetcher import YahooStockFetcher
from fmp_stock_fetcher import FMPStockFetcher
from robust_stock_fetcher import RobustStockFetcher
from stock_fetcher import StockFetcher  # Alpha Vantage (requires API key)
import time

class UnifiedStockFetcher:
    def __init__(self, provider='yahoo', api_key=None):
        """
        Initialize the Unified Stock Fetcher
        
        Args:
            provider (str): Data provider ('yahoo', 'fmp', 'alphavantage')
            api_key (str): API key (only required for Alpha Vantage)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        
        # Initialize the appropriate fetcher
        if self.provider == 'yahoo':
            self.fetcher = RobustStockFetcher()  # Use robust implementation
        elif self.provider == 'fmp':
            self.fetcher = FMPStockFetcher()
        elif self.provider == 'alphavantage':
            if not api_key:
                raise ValueError("API key is required for Alpha Vantage")
            self.fetcher = StockFetcher(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def get_quote(self, symbol):
        """
        Get real-time quote for a stock symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            dict: Stock quote data or None if error
        """
        try:
            return self.fetcher.get_quote(symbol)
        except Exception as e:
            print(f"Error with {self.provider}: {e}")
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
            return self.fetcher.search_symbol(keywords)
        except Exception as e:
            print(f"Error with {self.provider}: {e}")
            return None
    
    def get_daily_data(self, symbol):
        """
        Get historical daily data for a stock symbol
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            dict: Historical data or None if error
        """
        try:
            return self.fetcher.get_daily_data(symbol)
        except Exception as e:
            print(f"Error with {self.provider}: {e}")
            return None
    
    def get_provider_info(self):
        """
        Get information about the current provider
        
        Returns:
            dict: Provider information
        """
        provider_info = {
            'yahoo': {
                'name': 'Yahoo Finance',
                'requires_api_key': False,
                'rate_limit': 'Generous',
                'features': ['Real-time quotes', 'Historical data', 'Symbol search'],
                'reliability': 'High'
            },
            'fmp': {
                'name': 'Financial Modeling Prep',
                'requires_api_key': False,
                'rate_limit': 'Limited (250 requests/day)',
                'features': ['Real-time quotes', 'Historical data', 'Symbol search'],
                'reliability': 'Medium'
            },
            'alphavantage': {
                'name': 'Alpha Vantage',
                'requires_api_key': True,
                'rate_limit': '5 requests/minute (free tier)',
                'features': ['Real-time quotes', 'Historical data', 'Symbol search', 'Technical indicators'],
                'reliability': 'High'
            }
        }
        
        return provider_info.get(self.provider, {})

# Provider comparison and recommendation
def get_provider_recommendations():
    """
    Get recommendations for different use cases
    
    Returns:
        dict: Provider recommendations
    """
    return {
        'no_api_key_needed': [
            {
                'provider': 'yahoo',
                'name': 'Yahoo Finance',
                'pros': ['No API key required', 'High reliability', 'Real-time data', 'Generous rate limits'],
                'cons': ['May change without notice', 'No official API support'],
                'best_for': 'General use, prototyping, personal projects'
            },
            {
                'provider': 'fmp',
                'name': 'Financial Modeling Prep (Free)',
                'pros': ['No registration required for basic quotes', 'Real-time data'],
                'cons': ['Limited to 250 requests/day', 'Some features require registration'],
                'best_for': 'Light usage, testing'
            }
        ],
        'api_key_required': [
            {
                'provider': 'alphavantage',
                'name': 'Alpha Vantage',
                'pros': ['Official API', 'Technical indicators', 'Reliable', 'Good documentation'],
                'cons': ['Requires free registration', '5 requests/minute limit'],
                'best_for': 'Professional applications, technical analysis'
            }
        ]
    }

def main():
    """
    Demo function to show different providers
    """
    print("📈 Unified Stock Price Fetcher")
    print("=" * 50)
    print("Available providers:")
    print("1. Yahoo Finance (No API key required) ✅")
    print("2. Financial Modeling Prep (No API key required) ✅")
    print("3. Alpha Vantage (API key required) 🔑")
    print()
    
    recommendations = get_provider_recommendations()
    
    print("🎯 Recommendations for API-key-free providers:")
    for provider in recommendations['no_api_key_needed']:
        print(f"\n📊 {provider['name']}:")
        print(f"   Best for: {provider['best_for']}")
        print(f"   Pros: {', '.join(provider['pros'])}")
        print(f"   Cons: {', '.join(provider['cons'])}")
    
    print("\n" + "="*50)
    
    # Demo with Yahoo Finance (most reliable free option)
    print("🔥 Demo with Yahoo Finance (recommended free option):")
    
    try:
        fetcher = UnifiedStockFetcher('yahoo')
        print(f"\n📡 Using: {fetcher.get_provider_info()['name']}")
        
        # Test with a popular stock
        symbol = 'AAPL'
        print(f"\n🔍 Testing quote for {symbol}...")
        
        quote = fetcher.get_quote(symbol)
        if quote:
            print(f"✅ Success! Current price: ${float(quote['05. price']):.2f}")
            print(f"📈 Change: ${float(quote['09. change']):.2f} ({quote['10. change percent']})")
        else:
            print("❌ Failed to fetch quote")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
