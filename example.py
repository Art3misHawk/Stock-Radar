"""
Simple example to get started with stock fetching

This is a basic example that shows how to use the StockFetcher class.
"""

from stock_fetcher import StockFetcher, format_quote_display

def simple_example():
    """
    A simple example to fetch a stock quote
    """
    print("🚀 Simple Stock Price Fetcher Example")
    print("=" * 40)
    
    # Replace 'demo' with your actual API key from Alpha Vantage
    # Get your free API key here: https://www.alphavantage.co/support/#api-key
    api_key = "demo"  # This is a demo key with limited functionality
    
    # Create the fetcher
    fetcher = StockFetcher(api_key)
    
    # Example: Get Apple stock quote
    print("Fetching Apple (AAPL) stock quote...")
    apple_quote = fetcher.get_quote("AAPL")
    
    if apple_quote:
        print(format_quote_display(apple_quote))
    else:
        print("❌ Failed to fetch quote. You might need a real API key.")
        print("Get your free API key at: https://www.alphavantage.co/support/#api-key")

if __name__ == "__main__":
    simple_example()
