# 📈 Simple Stock Price Fetcher

A Python application that fetches real-time and historical stock data using the Alpha Vantage API.

## 🚀 Features

- **Real-time stock quotes** - Get current price, change, volume, and more
- **Stock symbol search** - Find symbols by company name
- **Historical data** - View past trading data
- **User-friendly interface** - Interactive command-line menu
- **Error handling** - Robust error handling for network issues

## 📋 Requirements

- Python 3.7+
- `requests` library
- Alpha Vantage API key (free)

## 🔧 Setup

### 1. Get Your Free API Key

1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free account
3. Get your API key (you get 25 requests per day for free)

### 2. Install Dependencies

The `requests` library is already installed in this environment.

### 3. Run the Application

#### Option 1: Interactive Menu (Recommended)
```bash
python stock_fetcher.py
```

#### Option 2: Simple Example
```bash
python example.py
```

## 📖 How to Use

### Basic Usage

```python
from stock_fetcher import StockFetcher

# Initialize with your API key
fetcher = StockFetcher("YOUR_API_KEY_HERE")

# Get a stock quote
quote = fetcher.get_quote("AAPL")
print(quote)

# Search for symbols
results = fetcher.search_symbol("Apple")
print(results)

# Get historical data
data = fetcher.get_daily_data("AAPL")
print(data)
```

### Example Output

```
📈 Stock Quote for AAPL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Current Price: $193.60
📊 Change: +2.40 (+1.25%)
📅 Trading Day: 2025-07-28
🔓 Open: $191.20
📈 High: $194.50
📉 Low: $190.80
🔒 Previous Close: $191.20
📦 Volume: 45,123,456
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔍 Popular Stock Symbols

Here are some popular stock symbols you can try:

- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc. (Google)
- **MSFT** - Microsoft Corporation
- **TSLA** - Tesla, Inc.
- **AMZN** - Amazon.com Inc.
- **NVDA** - NVIDIA Corporation
- **META** - Meta Platforms (Facebook)
- **SPY** - SPDR S&P 500 ETF

## ⚠️ API Limits

With a free Alpha Vantage API key:
- **25 requests per day**
- **5 API requests per minute**

The application includes a 1-second delay between requests to respect rate limits.

## 🛠️ Files Explained

- **`stock_fetcher.py`** - Main application with interactive menu
- **`example.py`** - Simple example script
- **`StockFetcher` class** - Core functionality for API calls

## 🎯 Learning Objectives

This project teaches you:

1. **API Integration** - How to work with REST APIs
2. **HTTP Requests** - Using the `requests` library
3. **JSON Parsing** - Handling API responses
4. **Error Handling** - Dealing with network and data errors
5. **Class Design** - Creating reusable code with classes
6. **User Interface** - Building interactive command-line apps

## 🚀 Next Steps

Want to enhance this project? Try adding:

1. **Data Visualization** - Plot stock prices with matplotlib
2. **Database Storage** - Save historical data to SQLite
3. **Technical Indicators** - Calculate moving averages, RSI
4. **Web Interface** - Create a Flask/Django web app
5. **Real-time Updates** - Auto-refresh prices every minute
6. **Portfolio Tracking** - Track multiple stocks

## 📚 Learn More

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [Requests Library Documentation](https://docs.python-requests.org/)
- [Python JSON Tutorial](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

Happy coding! 🐍📈
