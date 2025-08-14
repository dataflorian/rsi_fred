# 🚀 RSI Crypto Screener

A real-time cryptocurrency screening tool that identifies top-performing coins based on RSI (Relative Strength Index) analysis. Built with Python Flask and integrated with Binance API.

## ✨ Features

- **Real-time RSI Analysis**: Calculates RSI (14) for top cryptocurrencies
- **Smart Ranking**: Performance scoring based on RSI, volume, and price changes
- **Auto-refresh**: Updates every 15 minutes automatically
- **Direct Trading Links**: One-click access to Binance trading pairs
- **Professional UI**: Clean, responsive design with color-coded indicators
- **Mobile Friendly**: Optimized for all device sizes

## 🏗️ Architecture

```
RSI_Fred/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Web routes and views
│   ├── services/
│   │   ├── binance_service.py    # Binance API integration
│   │   ├── rsi_calculator.py     # RSI calculation engine
│   │   └── data_updater.py       # Data screening and ranking
├── config.py                # Configuration management
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Internet connection for Binance API access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd RSI_Fred
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Click "🚀 Main RSI Screener" to access the main tool

## 📊 Usage

### Main Screener
- **View top 10 performing coins** ranked by RSI performance
- **Real-time data** with 15-minute auto-refresh
- **Color-coded RSI values**:
  - 🟢 Green (50-70): Optimal strength range
  - 🟡 Orange (40-50): Good potential
  - 🔴 Red (70+): Overbought
  - 🟢 Green (30-): Oversold

### Manual Refresh
- Click "🔄 Refresh Data" button for immediate updates
- Useful for checking market changes during active trading

### Trading Links
- Click "📈 Trade" to open Binance trading page
- Direct access to buy/sell the selected cryptocurrency

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode |
| `RSI_PERIOD` | `14` | RSI calculation period |
| `TOP_COINS_LIMIT` | `10` | Number of top coins to display |
| `REFRESH_INTERVAL_MINUTES` | `15` | Auto-refresh interval |
| `OHLCV_LIMIT` | `100` | Historical data points for RSI |

### Example Configuration
```bash
export FLASK_ENV=production
export RSI_PERIOD=14
export TOP_COINS_LIMIT=15
export REFRESH_INTERVAL_MINUTES=10
```

## 🌐 Deployment

### Free Hosting Options

#### 1. Render.com (Recommended)
- **Free tier**: 750 hours/month
- **Auto-deploy**: Git-based deployment
- **SSL included**: HTTPS by default

**Deployment Steps:**
1. Push code to GitHub
2. Connect repository to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn run:app`
5. Add environment variables in Render dashboard

#### 2. Railway.app
- **Free tier**: 500 hours/month
- **Easy deployment**: GitHub integration
- **Custom domains**: Supported

#### 3. Heroku (Free tier discontinued)
- **Alternative**: Use paid plans or migrate to Render

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure logging level
- [ ] Set up monitoring (optional)
- [ ] Test auto-refresh functionality
- [ ] Verify mobile responsiveness

## 🔧 Development

### Project Structure
- **Modular design**: Services separated by functionality
- **Clean architecture**: Easy to extend and maintain
- **Error handling**: Comprehensive error management
- **Logging**: Structured logging for debugging

### Adding New Features
1. **New indicators**: Extend `rsi_calculator.py`
2. **Additional exchanges**: Create new service in `services/`
3. **UI improvements**: Modify routes and templates
4. **Data sources**: Integrate new APIs

### Testing
```bash
# Run basic tests
python -m pytest tests/

# Test specific functionality
python -m pytest tests/test_rsi_calculator.py
```

## 📈 Performance Considerations

### Current Limitations
- **Refresh time**: ~30-60 seconds for full data update
- **API rate limits**: Binance API constraints
- **Data processing**: Sequential coin analysis

### Future Optimizations
- **Background updates**: Async data processing
- **Incremental updates**: Only refresh changed data
- **WebSocket integration**: Real-time price updates
- **Caching strategies**: Redis or database persistence
- **Parallel processing**: Concurrent API calls

## 🛡️ Security

### API Security
- **Rate limiting**: Built-in Binance API rate limiting
- **No API keys**: Public data only (no trading access)
- **Input validation**: Sanitized user inputs

### Production Security
- **Environment variables**: Secure configuration
- **HTTPS only**: SSL/TLS encryption
- **Error handling**: No sensitive data exposure

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Submit pull request with description

### Code Standards
- **Python**: PEP 8 compliance
- **Documentation**: Docstrings for all functions
- **Error handling**: Comprehensive exception management
- **Testing**: Unit tests for new features

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

### Common Issues
- **API connection errors**: Check internet connection and Binance status
- **Slow refresh**: Normal for first load, subsequent updates are faster
- **Mobile display**: Ensure responsive design is working

### Getting Help
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check this README first
- **Community**: Join our discussion forum

## 🎯 Roadmap

### Phase 1: Core Features ✅
- [x] RSI calculation engine
- [x] Binance API integration
- [x] Basic screening functionality

### Phase 2: Enhanced UI ✅
- [x] Professional interface
- [x] Auto-refresh system
- [x] Mobile responsiveness

### Phase 3: Performance (Future)
- [ ] Background data updates
- [ ] WebSocket integration
- [ ] Advanced caching

### Phase 4: Advanced Features (Future)
- [ ] Multiple timeframe analysis
- [ ] Additional technical indicators
- [ ] Portfolio tracking
- [ ] Alert system

---

**Built with ❤️ for the crypto trading community**

*Disclaimer: This tool is for educational and informational purposes only. Always do your own research before making investment decisions.*
