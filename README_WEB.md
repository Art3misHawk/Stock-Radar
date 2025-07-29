# Stock Price Fetcher Web App

A modern web interface for fetching real-time stock data using the Alpha Vantage API.

## 🌐 Live Demo

Your web application will be available at:
- Local development: http://localhost:5000
- Production: (deployment URL will be here)

## 🚀 Features

- **Modern Web Interface** - Clean, responsive design with Bootstrap
- **Real-time Stock Quotes** - Get current prices and market data
- **Symbol Search** - Find stocks by company name
- **Historical Data** - View past trading information
- **Mobile Friendly** - Works great on phones and tablets

## 📱 How to Use

1. **Setup**: Enter your Alpha Vantage API key
2. **Search**: Find stocks by company name
3. **Quote**: Get real-time stock prices
4. **History**: View historical trading data

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit http://localhost:5000 in your browser.

## 🌐 Deployment Options

### Option 1: Heroku (Recommended)
1. Create a Heroku account
2. Install Heroku CLI
3. Deploy with these commands:

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-stock-app-name

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Option 2: Railway
1. Connect your GitHub repository to Railway
2. Deploy automatically on push

### Option 3: Render
1. Connect your GitHub repository to Render
2. Configure build settings
3. Deploy automatically

### Option 4: PythonAnywhere
1. Upload your files
2. Configure WSGI settings
3. Set environment variables

## 📋 Environment Variables

For production deployment, set these environment variables:
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`

## 🔧 Project Structure

```
├── app.py              # Main Flask application
├── stock_fetcher.py    # Core stock fetching logic
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── setup.html
│   └── dashboard.html
└── static/            # CSS and JavaScript
    ├── style.css
    └── script.js
```

## 🔐 Security Notes

- API keys are stored in memory only (not persistent)
- CORS is enabled for API endpoints
- Input validation on all forms
- Error handling for network issues

## 📊 API Endpoints

- `GET /` - Home page
- `GET /setup` - API key setup
- `GET /dashboard` - Main dashboard
- `GET /api/quote/<symbol>` - Get stock quote
- `GET /api/search/<keywords>` - Search stocks
- `GET /api/historical/<symbol>` - Get historical data

## 🎯 Next Steps

- Add user authentication
- Implement data caching
- Add more chart visualizations
- Create portfolio tracking
- Add price alerts

## 📞 Support

Built with Python Flask and Alpha Vantage API.
