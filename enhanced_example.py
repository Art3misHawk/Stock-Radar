"""
Enhanced Stock Price Fetcher with Configuration

This version reads the API key from config.py for easier setup.
"""

from stock_fetcher import StockFetcher, format_quote_display
import config

def enhanced_example():
    """
    Enhanced example that uses the config file
    """
    print("🚀 Enhanced Stock Price Fetcher")
    print("=" * 40)
    
    # Check if API key is configured
    if config.ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please configure your API key in config.py")
        print("1. Open config.py")
        print("2. Replace 'YOUR_API_KEY_HERE' with your actual API key")
        print("3. Get your free API key at: https://www.alphavantage.co/support/#api-key")
        return
    
    # Create the fetcher
    fetcher = StockFetcher(config.ALPHA_VANTAGE_API_KEY)
    
    # Example stocks to fetch
    stocks = ["AAPL", "GOOGL", "MSFT"]
    
    print(f"Fetching quotes for: {', '.join(stocks)}")
    print("=" * 50)
    
    for symbol in stocks:
        print(f"\n🔍 Fetching {symbol}...")
        quote = fetcher.get_quote(symbol)
        
        if quote:
            print(format_quote_display(quote))
        else:
            print(f"❌ Failed to fetch quote for {symbol}")
        
        # Small delay to respect rate limits
        import time
        time.sleep(config.DEFAULT_DELAY)

if __name__ == "__main__":
    enhanced_example()
