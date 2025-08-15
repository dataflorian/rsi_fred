import json
import logging
import time
from typing import Dict, List, Optional, Callable
from websocket import create_connection, WebSocketConnectionClosedException
import threading
from collections import defaultdict

logger = logging.getLogger(__name__)

class BinanceWebSocketService:
    """WebSocket service for real-time Binance data without rate limiting"""
    
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.subscriptions = defaultdict(list)
        self.data_cache = {}
        self.callbacks = {}
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        
        # WebSocket URLs - Use the correct Binance WebSocket endpoint
        self.ws_url = "wss://stream.binance.com:9443/ws"
        
        # Rate limiting (WebSocket is much more generous)
        self.max_subscriptions = 200  # Binance allows up to 200 streams
        
    def connect(self) -> bool:
        """Establish WebSocket connection"""
        try:
            logger.info("Connecting to Binance WebSocket...")
            self.ws = create_connection(self.ws_url, timeout=10)
            self.is_connected = True
            self.reconnect_attempts = 0
            logger.info("✅ WebSocket connected successfully")
            return True
        except Exception as e:
            logger.error(f"❌ WebSocket connection failed: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Close WebSocket connection"""
        if self.ws:
            try:
                self.ws.close()
                self.is_connected = False
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
    
    def subscribe_to_ticker(self, symbols: List[str], callback: Callable = None):
        """Subscribe to ticker streams for multiple symbols"""
        if not self.is_connected:
            if not self.connect():
                return False
        
        try:
            # Format symbols for WebSocket (lowercase, no separator)
            ws_symbols = [symbol.lower().replace('/', '') for symbol in symbols]
            
            # Create subscription message - Use the correct format
            subscription = {
                "method": "SUBSCRIBE",
                "params": [f"{symbol}@ticker" for symbol in ws_symbols],
                "id": int(time.time() * 1000)
            }
            
            logger.info(f"Sending subscription: {json.dumps(subscription)}")
            
            # Send subscription
            self.ws.send(json.dumps(subscription))
            logger.info(f"Subscribed to {len(symbols)} ticker streams")
            
            # Store callback for data processing
            for symbol in symbols:
                self.callbacks[symbol] = callback
            
            return True
            
        except Exception as e:
            logger.error(f"Subscription failed: {e}")
            return False
    
    def subscribe_to_klines(self, symbol: str, interval: str = '1h', callback: Callable = None):
        """Subscribe to kline/candlestick data for RSI calculation"""
        if not self.is_connected:
            if not self.connect():
                return False
        
        try:
            # Format symbol for WebSocket
            ws_symbol = symbol.lower().replace('/', '')
            
            # Create subscription message
            subscription = {
                "method": "SUBSCRIBE",
                "params": [f"{ws_symbol}@kline_{interval}"],
                "id": int(time.time() * 1000)
            }
            
            # Send subscription
            self.ws.send(json.dumps(subscription))
            logger.info(f"Subscribed to {symbol} klines ({interval})")
            
            # Store callback
            self.callbacks[f"{symbol}_klines"] = callback
            
            return True
            
        except Exception as e:
            logger.error(f"Kline subscription failed: {e}")
            return False
    
    def start_listening(self):
        """Start listening for WebSocket messages in a separate thread"""
        def listen():
            while self.is_connected:
                try:
                    message = self.ws.recv()
                    data = json.loads(message)
                    self._process_message(data)
                except WebSocketConnectionClosedException:
                    logger.warning("WebSocket connection closed, attempting reconnect...")
                    self._reconnect()
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    time.sleep(1)
        
        # Start listening thread
        self.listener_thread = threading.Thread(target=listen, daemon=True)
        self.listener_thread.start()
        logger.info("WebSocket listener started")
    
    def _process_message(self, data: Dict):
        """Process incoming WebSocket messages"""
        try:
            # Handle subscription confirmation messages
            if 'result' in data and 'id' in data:
                logger.info(f"Subscription confirmed: {data}")
                return
            
            # Handle error messages
            if 'error' in data:
                logger.error(f"WebSocket error: {data}")
                return
            
            # Handle actual data messages
            if 'stream' in data:
                stream_data = data['data']
                stream_type = data['stream']
                
                if 'ticker' in stream_type:
                    self._process_ticker_data(stream_data)
                elif 'kline' in stream_type:
                    self._process_kline_data(stream_data)
            else:
                # Direct data (for some message types)
                if 's' in data and 'c' in data:  # Ticker data
                    self._process_ticker_data(data)
                elif 's' in data and 'k' in data:  # Kline data
                    self._process_kline_data(data)
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def _process_ticker_data(self, data: Dict):
        """Process ticker data and update cache"""
        try:
            symbol = data['s']
            ticker_info = {
                'symbol': symbol,
                'price': float(data['c']),
                'volume': float(data['v']),
                'price_change': float(data['P']),
                'volume_quote': float(data['q']),
                'timestamp': data['E']
            }
            
            self.data_cache[symbol] = ticker_info
            logger.info(f"Updated ticker for {symbol}: ${ticker_info['price']}")
            
        except Exception as e:
            logger.error(f"Error processing ticker data: {e}")
    
    def _process_kline_data(self, data: Dict):
        """Process kline data for technical analysis"""
        try:
            symbol = data['s']
            kline = data['k']
            
            kline_data = {
                'symbol': symbol,
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
                'timestamp': kline['t'],
                'interval': kline['i']
            }
            
            # Store in cache with symbol_klines key
            cache_key = f"{symbol}_klines"
            if cache_key not in self.data_cache:
                self.data_cache[cache_key] = []
            
            self.data_cache[cache_key].append(kline_data)
            
            # Keep only last 100 klines for RSI calculation
            if len(self.data_cache[cache_key]) > 100:
                self.data_cache[cache_key] = self.data_cache[cache_key][-100:]
            
            logger.info(f"Updated klines for {symbol}: {len(self.data_cache[cache_key])} candles")
            
        except Exception as e:
            logger.error(f"Error processing kline data: {e}")
    
    def _reconnect(self):
        """Attempt to reconnect to WebSocket"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error("Max reconnection attempts reached")
            return False
        
        self.reconnect_attempts += 1
        logger.info(f"Attempting reconnection {self.reconnect_attempts}/{self.max_reconnect_attempts}")
        
        try:
            self.disconnect()
            time.sleep(2 ** self.reconnect_attempts)  # Exponential backoff
            return self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            return False
    
    def get_ticker_data(self, symbol: str) -> Optional[Dict]:
        """Get current ticker data from cache"""
        return self.data_cache.get(symbol)
    
    def get_kline_data(self, symbol: str) -> Optional[List[Dict]]:
        """Get kline data from cache"""
        cache_key = f"{symbol}_klines"
        return self.data_cache.get(cache_key, [])
    
    def get_top_coins_by_volume(self, limit: int = 50) -> List[Dict]:
        """Get top coins by volume from cached ticker data"""
        try:
            # Filter USDT pairs and sort by volume
            usdt_tickers = []
            for symbol, ticker in self.data_cache.items():
                if symbol.endswith('USDT') and 'volume_quote' in ticker:
                    usdt_tickers.append({
                        'symbol': ticker['symbol'],
                        'volume': ticker['volume_quote'],
                        'price': ticker['price'],
                        'change': ticker['price_change']
                    })
            
            # Sort by volume and return top coins
            usdt_tickers.sort(key=lambda x: x['volume'], reverse=True)
            return usdt_tickers[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get top coins by volume: {e}")
            return []
    
    def test_connection(self) -> Dict:
        """Test WebSocket connection and basic functionality"""
        try:
            if not self.connect():
                return {
                    'success': False,
                    'message': 'Failed to establish WebSocket connection',
                    'error': 'Connection timeout or network issue'
                }
            
            # Test basic subscription
            test_symbols = ['BTCUSDT', 'ETHUSDT']
            if self.subscribe_to_ticker(test_symbols):
                # Start listening for messages
                self.start_listening()
                
                # Wait for data with timeout
                timeout = 10  # seconds
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    # Check if we received data
                    btc_data = self.get_ticker_data('BTCUSDT')
                    eth_data = self.get_ticker_data('ETHUSDT')
                    
                    if btc_data and eth_data:
                        return {
                            'success': True,
                            'message': 'WebSocket connected and receiving data successfully',
                            'total_streams': len(self.data_cache),
                            'sample_data': {
                                'BTC/USDT': f"${btc_data['price']:.2f}",
                                'ETH/USDT': f"${eth_data['price']:.2f}"
                            }
                        }
                    
                    time.sleep(0.5)  # Check every 500ms
                
                # Timeout reached
                return {
                    'success': False,
                    'message': 'Connected but no data received within timeout',
                    'error': 'Data reception timeout - check subscription format'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to subscribe to test streams',
                    'error': 'Subscription failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection test failed: {str(e)}',
                'error': str(e)
            }
        finally:
            self.disconnect()
