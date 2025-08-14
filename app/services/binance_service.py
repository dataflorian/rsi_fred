import ccxt
import logging
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceService:
    def __init__(self):
        """Initialize Binance exchange connection"""
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot'
                }
            })
            logger.info("Binance service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance service: {e}")
            raise
    
    def get_markets(self) -> List[Dict]:
        """Fetch all available trading markets"""
        try:
            markets = self.exchange.load_markets()
            # Filter for USDT pairs only (most common)
            usdt_pairs = [
                {
                    'symbol': symbol,
                    'base': market['base'],
                    'quote': market['quote'],
                    'active': market['active']
                }
                for symbol, market in markets.items()
                if market['quote'] == 'USDT' and market['active']
            ]
            logger.info(f"Fetched {len(usdt_pairs)} USDT trading pairs")
            return usdt_pairs
        except Exception as e:
            logger.error(f"Failed to fetch markets: {e}")
            return []
    
    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Fetch current ticker data for a symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': ticker['symbol'],
                'last_price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'change_24h': ticker['change'],
                'change_percent_24h': ticker['percentage']
            }
        except Exception as e:
            logger.error(f"Failed to fetch ticker for {symbol}: {e}")
            return None
    
    def test_connection(self) -> Dict:
        """Test the API connection and return status"""
        try:
            # Try to fetch basic market info
            markets = self.get_markets()
            return {
                'status': 'connected',
                'message': f'Successfully connected to Binance. Found {len(markets)} USDT pairs.',
                'sample_pairs': markets[:5] if markets else []
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}',
                'sample_pairs': []
            }
