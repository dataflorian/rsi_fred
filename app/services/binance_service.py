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
    
    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Optional[List[List]]:
        """
        Fetch OHLCV data for RSI calculation
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            timeframe (str): Timeframe for candles (default: '1h')
            limit (int): Number of candles to fetch (default: 100)
            
        Returns:
            Optional[List[List]]: OHLCV data or None if failed
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            logger.info(f"Fetched {len(ohlcv)} {timeframe} candles for {symbol}")
            return ohlcv
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            return None
    
    def get_top_coins_by_volume(self, limit: int = 50) -> List[Dict]:
        """
        Get top coins by 24h volume for initial screening
        
        Args:
            limit (int): Number of top coins to return
            
        Returns:
            List[Dict]: List of top coins with volume data
        """
        try:
            tickers = self.exchange.fetch_tickers()
            
            # Filter USDT pairs and sort by volume
            usdt_tickers = []
            for symbol, ticker in tickers.items():
                if symbol.endswith('/USDT') and ticker['baseVolume']:
                    usdt_tickers.append({
                        'symbol': symbol,
                        'base': symbol.split('/')[0],
                        'volume_24h': ticker['baseVolume'],
                        'price': ticker['last'],
                        'change_24h': ticker['percentage']
                    })
            
            # Sort by volume and return top coins
            top_coins = sorted(usdt_tickers, key=lambda x: x['volume_24h'], reverse=True)[:limit]
            logger.info(f"Fetched top {len(top_coins)} coins by volume")
            return top_coins
            
        except Exception as e:
            logger.error(f"Failed to fetch top coins by volume: {e}")
            return []
    
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
