import ccxt
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceService:
    def __init__(self):
        """Initialize Binance exchange connection"""
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True, 
                'options': {'defaultType': 'spot'},
                'timeout': 30000  # 30 second timeout
            })
            logger.info("Binance service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance service: {e}")
            raise

    def test_connection(self) -> Dict:
        """Test connection to Binance API with detailed error reporting"""
        try:
            # Test basic connectivity
            markets = self.exchange.load_markets()
            logger.info(f"Successfully loaded {len(markets)} markets")
            
            # Filter USDT pairs
            usdt_pairs = [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
            logger.info(f"Found {len(usdt_pairs)} USDT pairs")
            
            # Test ticker endpoint
            try:
                btc_ticker = self.exchange.fetch_ticker('BTC/USDT')
                logger.info(f"BTC ticker test successful: {btc_ticker['last']}")
            except Exception as e:
                logger.warning(f"BTC ticker test failed: {e}")
            
            return {
                'success': True,
                'message': f'Successfully connected to Binance. Found {len(usdt_pairs)} USDT pairs.',
                'total_markets': len(markets),
                'usdt_pairs': len(usdt_pairs),
                'sample_pairs': usdt_pairs[:5] if usdt_pairs else []
            }
            
        except Exception as e:
            logger.error(f"Binance connection test failed: {e}")
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}',
                'error': str(e),
                'total_markets': 0,
                'usdt_pairs': 0,
                'sample_pairs': []
            }

    def get_markets(self) -> Dict:
        """Get all available markets"""
        try:
            markets = self.exchange.load_markets()
            return {'success': True, 'markets': markets}
        except Exception as e:
            logger.error(f"Failed to get markets: {e}")
            return {'success': False, 'error': str(e)}

    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Get ticker for a specific symbol"""
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            return None

    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Optional[List[List]]:
        """Get OHLCV data for RSI calculation"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            logger.info(f"Successfully fetched {len(ohlcv)} OHLCV data points for {symbol}")
            return ohlcv
        except Exception as e:
            logger.error(f"Failed to get OHLCV for {symbol}: {e}")
            return None

    def get_top_coins_by_volume(self, limit: int = 50) -> List[Dict]:
        """Get top coins by 24h volume"""
        try:
            tickers = self.exchange.fetch_tickers()
            logger.info(f"Successfully fetched {len(tickers)} tickers")
            
            # Filter USDT pairs and sort by volume
            usdt_tickers = []
            for symbol, ticker in tickers.items():
                if symbol.endswith('/USDT') and ticker.get('quoteVolume'):
                    usdt_tickers.append({
                        'symbol': symbol,
                        'volume': ticker['quoteVolume'],
                        'price': ticker['last'],
                        'change': ticker.get('percentage', 0)
                    })
            
            # Sort by volume and return top coins
            usdt_tickers.sort(key=lambda x: x['volume'], reverse=True)
            top_coins = usdt_tickers[:limit]
            
            logger.info(f"Successfully processed {len(top_coins)} top coins by volume")
            return top_coins
            
        except Exception as e:
            logger.error(f"Failed to get top coins by volume: {e}")
            return []
