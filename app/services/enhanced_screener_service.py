import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json

from app.services.technical_indicators import TechnicalIndicators
from app.services.historical_data_service import HistoricalDataService
from app.services.websocket_service import BinanceWebSocketService

logger = logging.getLogger(__name__)

class EnhancedScreenerService:
    """Enhanced screener service with multiple indicators and historical analysis"""
    
    def __init__(self):
        self.technical_indicators = TechnicalIndicators()
        self.historical_data = HistoricalDataService()
        self.websocket_service = BinanceWebSocketService()
        self.available_indicators = [
            'rsi', 'returns_vs_btc', 'mansfield_rs', 'roc', 'vwap'
        ]
        
        # Initialize with some mock data for testing
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize some mock data for testing when no real data is available"""
        try:
            logger.info("Initializing mock data for testing...")
            
            # Add some popular coins to the database
            mock_coins = [
                {'symbol': 'BTCUSDT', 'name': 'Bitcoin'},
                {'symbol': 'ETHUSDT', 'name': 'Ethereum'},
                {'symbol': 'BNBUSDT', 'name': 'Binance Coin'},
                {'symbol': 'ADAUSDT', 'name': 'Cardano'},
                {'symbol': 'SOLUSDT', 'name': 'Solana'},
                {'symbol': 'DOTUSDT', 'name': 'Polkadot'},
                {'symbol': 'MATICUSDT', 'name': 'Polygon'},
                {'symbol': 'LINKUSDT', 'name': 'Chainlink'},
                {'symbol': 'UNIUSDT', 'name': 'Uniswap'},
                {'symbol': 'AVAXUSDT', 'name': 'Avalanche'}
            ]
            
            logger.info(f"Adding {len(mock_coins)} mock coins to database")
            
            for coin in mock_coins:
                logger.debug(f"Adding coin: {coin['symbol']}")
                self.historical_data.add_coin(coin['symbol'], coin['name'])
                
                # Add some mock price data
                mock_price_data = {
                    'price': 100 + (hash(coin['symbol']) % 1000),  # Random price
                    'volume_24h': 1000000 + (hash(coin['symbol']) % 9000000),  # Random volume
                    'price_change_24h': (hash(coin['symbol']) % 40) - 20,  # Random change -20% to +20%
                    'rsi': 30 + (hash(coin['symbol']) % 40)  # Random RSI 30-70
                }
                
                logger.debug(f"Adding mock price data for {coin['symbol']}: {mock_price_data}")
                self.historical_data.update_price_data(coin['symbol'], mock_price_data)
                
            logger.info("Mock data initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing mock data: {e}")
    
    def get_screening_results(self, 
                            selected_indicator: str = 'rsi',
                            percentile: float = 95,
                            limit: int = 100) -> Dict:
        """Get comprehensive screening results"""
        try:
            logger.info(f"Starting screening for indicator: {selected_indicator}")
            
            # Get top coins by volume
            top_coins = self._get_top_coins_by_volume(limit)
            logger.info(f"Retrieved {len(top_coins)} top coins by volume")
            
            if not top_coins:
                logger.warning("No coins data available")
                return {
                    'success': False,
                    'message': 'No coins data available',
                    'data': []
                }
            
            # Get BTC data for relative calculations
            btc_data = self._get_btc_data()
            logger.info(f"BTC data: {btc_data}")
            
            # Calculate indicators for all coins
            coins_with_indicators = self._calculate_indicators_for_coins(top_coins, btc_data)
            logger.info(f"Calculated indicators for {len(coins_with_indicators)} coins")
            
            if not coins_with_indicators:
                logger.warning("No coins with indicators available")
                return {
                    'success': False,
                    'message': 'No coins with indicators available',
                    'data': []
                }
            
            # Rank coins by selected indicator
            ranked_coins = self.technical_indicators.rank_coins_by_indicator(
                coins_with_indicators, selected_indicator, btc_data
            )
            logger.info(f"Ranked {len(ranked_coins)} coins by {selected_indicator}")
            
            # Get top percentile coins
            top_percentile_coins = self.technical_indicators.get_top_percentile_coins(
                ranked_coins, percentile
            )
            logger.info(f"Selected {len(top_percentile_coins)} top percentile coins")
            
            # Prepare results
            results = {
                'success': True,
                'selected_indicator': selected_indicator,
                'indicator_description': self.technical_indicators.get_indicator_description(selected_indicator),
                'percentile': percentile,
                'total_coins_analyzed': len(ranked_coins),
                'top_percentile_count': len(top_percentile_coins),
                'timestamp': datetime.now().isoformat(),
                'coins': top_percentile_coins,
                'available_indicators': self.available_indicators
            }
            
            logger.info(f"Screening completed successfully: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error getting screening results: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'data': []
            }
    
    def get_heatmap_data(self, 
                         selected_indicator: str = 'rsi',
                         days: int = 30,
                         top_coins_limit: int = 50) -> Dict:
        """Get data for heatmap visualization"""
        try:
            logger.info(f"Getting heatmap data for indicator: {selected_indicator}, days: {days}")
            
            # Get top coins by volume
            top_coins = self._get_top_coins_by_volume(top_coins_limit)
            logger.info(f"Retrieved {len(top_coins)} top coins for heatmap")
            
            if not top_coins:
                logger.warning("No coins data available for heatmap")
                return {
                    'success': False,
                    'message': 'No coins data available for heatmap',
                    'data': {}
                }
            
            # Get BTC data for relative calculations
            btc_data = self._get_btc_data()
            logger.info(f"BTC data for heatmap: {btc_data}")
            
            # Prepare heatmap data structure
            heatmap_data = {
                'metadata': {
                    'indicator': selected_indicator,
                    'days': days,
                    'total_coins': len(top_coins),
                    'timestamp': datetime.now().isoformat()
                },
                'coins': []
            }
            
            # Generate timestamps for the last N days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            timestamps = pd.date_range(start=start_date, end=end_date, freq='D')
            
            logger.info(f"Generated {len(timestamps)} timestamps for heatmap")
            
            # Process each coin
            for coin_symbol in top_coins[:10]:  # Limit to top 10 for preview
                logger.debug(f"Processing coin {coin_symbol} for heatmap")
                
                # Get historical data for this coin
                historical_data = self.historical_data.get_historical_data(coin_symbol, days)
                
                if not historical_data.empty:
                    # Prepare historical values for this indicator
                    historical_values = self._prepare_historical_values(
                        historical_data, selected_indicator, timestamps
                    )
                    
                    # Get current coin data
                    current_data = self._get_coin_data(coin_symbol)
                    
                    coin_heatmap_data = {
                        'symbol': coin_symbol,
                        'current_value': current_data.get(selected_indicator, 0),
                        'signal': self.technical_indicators.get_indicator_signal(
                            selected_indicator, current_data.get(selected_indicator, 0)
                        ),
                        'price': current_data.get('price', 0),
                        'volume_24h': current_data.get('volume_24h', 0),
                        'historical_values': historical_values
                    }
                    
                    heatmap_data['coins'].append(coin_heatmap_data)
                    logger.debug(f"Added heatmap data for {coin_symbol}")
                else:
                    logger.warning(f"No historical data for {coin_symbol}")
            
            logger.info(f"Generated heatmap data for {len(heatmap_data['coins'])} coins")
            
            return {
                'success': True,
                'data': heatmap_data
            }
            
        except Exception as e:
            logger.error(f"Error getting heatmap data: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'data': {}
            }
    
    def _get_top_coins_by_volume(self, limit: int) -> List[str]:
        """Get top coins by volume from WebSocket service"""
        try:
            logger.info(f"Getting top {limit} coins by volume")
            
            # Ensure WebSocket is connected and has data
            if not self.websocket_service.is_connected:
                logger.info("WebSocket not connected, testing connection...")
                # Test connection to get some initial data
                connection_result = self.websocket_service.test_connection()
                if not connection_result['success']:
                    logger.warning("WebSocket not connected, falling back to historical data")
                    historical_coins = self.historical_data.get_top_coins_by_volume(limit)
                    logger.info(f"Historical data returned {len(historical_coins)} coins")
                    return historical_coins
            
            # Try to get from WebSocket service first
            websocket_coins = self.websocket_service.get_top_coins_by_volume(limit)
            logger.info(f"WebSocket returned {len(websocket_coins)} coins")
            
            if websocket_coins:
                # Convert the WebSocket format to the expected format
                # WebSocket returns: [{'symbol': 'BTCUSDT', 'volume': 123, 'price': 456, 'change': 789}]
                # We need: ['BTCUSDT', 'ETHUSDT', ...]
                symbols = [coin['symbol'] for coin in websocket_coins if 'symbol' in coin]
                logger.info(f"Converted WebSocket data to {len(symbols)} symbols: {symbols[:5]}")
                return symbols
            
            # Fallback to historical data service
            logger.info("Falling back to historical data service")
            historical_coins = self.historical_data.get_top_coins_by_volume(limit)
            logger.info(f"Historical data returned {len(historical_coins)} coins")
            return historical_coins
            
        except Exception as e:
            logger.error(f"Error getting top coins by volume: {e}")
            return []
    
    def _get_btc_data(self) -> Dict:
        """Get Bitcoin data for relative calculations"""
        try:
            logger.debug("Getting BTC data")
            
            btc_data = self.websocket_service.get_ticker_data('BTCUSDT')
            if btc_data:
                logger.debug(f"WebSocket BTC data: {btc_data}")
                converted_btc_data = {
                    'price': btc_data.get('price', 0),
                    'price_change_24h': btc_data.get('price_change', 0),
                    'volume_24h': btc_data.get('volume_quote', 0)
                }
                logger.debug(f"Converted WebSocket BTC data: {converted_btc_data}")
                return converted_btc_data
            
            # Fallback to historical data
            logger.debug("Falling back to historical BTC data")
            btc_historical = self.historical_data.get_historical_data('BTCUSDT', 1)
            if not btc_historical.empty:
                latest = btc_historical.iloc[-1]
                historical_btc_data = {
                    'price': latest.get('price', 0),
                    'price_change_24h': latest.get('price_change_24h', 0),
                    'volume_24h': latest.get('volume_24h', 0)
                }
                logger.debug(f"Historical BTC data: {historical_btc_data}")
                return historical_btc_data
            
            logger.warning("No BTC data available, using defaults")
            return {'price': 0, 'price_change_24h': 0, 'volume_24h': 0}
            
        except Exception as e:
            logger.error(f"Error getting BTC data: {e}")
            return {'price': 0, 'price_change_24h': 0, 'volume_24h': 0}
    
    def _get_coin_data(self, symbol: str) -> Dict:
        """Get current data for a specific coin"""
        try:
            logger.debug(f"Getting data for coin: {symbol}")
            
            # Try WebSocket first
            websocket_data = self.websocket_service.get_ticker_data(symbol)
            if websocket_data:
                logger.debug(f"WebSocket data for {symbol}: {websocket_data}")
                # Convert WebSocket format to expected format
                converted_data = {
                    'symbol': symbol,
                    'price': websocket_data.get('price', 0),
                    'volume_24h': websocket_data.get('volume_quote', 0),
                    'price_change_24h': websocket_data.get('price_change', 0),
                    'rsi': 0  # WebSocket doesn't provide RSI, will be calculated
                }
                logger.debug(f"Converted WebSocket data for {symbol}: {converted_data}")
                return converted_data
            
            # Fallback to historical data
            logger.debug(f"Falling back to historical data for {symbol}")
            historical_data = self.historical_data.get_historical_data(symbol, 1)
            if not historical_data.empty:
                latest = historical_data.iloc[-1]
                historical_coins_data = {
                    'symbol': symbol,
                    'price': latest.get('price', 0),
                    'volume_24h': latest.get('volume_24h', 0),
                    'price_change_24h': latest.get('price_change_24h', 0),
                    'rsi': latest.get('rsi', 0)
                }
                logger.debug(f"Historical data for {symbol}: {historical_coins_data}")
                return historical_coins_data
            
            logger.warning(f"No data available for {symbol}")
            return {}
            
        except Exception as e:
            logger.error(f"Error getting coin data for {symbol}: {e}")
            return {}
    
    def _calculate_indicators_for_coins(self, coins: List[str], btc_data: Dict) -> List[Dict]:
        """Calculate indicators for a list of coins"""
        try:
            if not coins:
                logger.warning("No coins provided for indicator calculation")
                return []
                
            coins_with_indicators = []
            
            for coin_symbol in coins:
                coin_data = self._get_coin_data(coin_symbol)
                if coin_data:
                    # Calculate all indicators
                    indicators = self.technical_indicators.calculate_all_indicators(coin_data, btc_data)
                    
                    # Add indicators to coin data
                    coin_data.update(indicators)
                    coins_with_indicators.append(coin_data)
                else:
                    logger.warning(f"No data available for coin: {coin_symbol}")
            
            logger.info(f"Calculated indicators for {len(coins_with_indicators)} out of {len(coins)} coins")
            return coins_with_indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators for coins: {e}")
            return []
    
    def _prepare_historical_values(self, 
                                 historical_data: pd.DataFrame, 
                                 indicator: str, 
                                 timestamps: pd.DatetimeIndex) -> List[float]:
        """Prepare historical values for heatmap visualization"""
        try:
            logger.debug(f"Preparing historical values for indicator: {indicator}, timestamps: {len(timestamps)}")
            
            values = []
            
            for ts in timestamps:
                # Find closest historical data point
                if not historical_data.empty:
                    # Get data for this timestamp or closest available
                    ts_str = ts.strftime('%Y-%m-%d')
                    day_data = historical_data[historical_data.index.strftime('%Y-%m-%d') == ts_str]
                    
                    if not day_data.empty:
                        # Use the first available data point for the day
                        if indicator == 'rsi':
                            value = day_data.iloc[0].get('rsi', 0)
                        elif indicator == 'price_change_24h':
                            value = day_data.iloc[0].get('price_change_24h', 0)
                        else:
                            value = 0  # Default for other indicators
                        
                        values.append(value)
                        logger.debug(f"Added value {value} for {ts_str}")
                    else:
                        values.append(0)  # No data for this day
                        logger.debug(f"No data for {ts_str}, using 0")
                else:
                    values.append(0)
                    logger.debug(f"Historical data empty, using 0 for {ts}")
            
            logger.debug(f"Prepared {len(values)} historical values")
            return values
            
        except Exception as e:
            logger.error(f"Error preparing historical values: {e}")
            return [0] * len(timestamps)
    
    def get_screening_stats(self) -> Dict:
        """Get screening service statistics"""
        try:
            logger.info("Getting screening service statistics")
            
            db_stats = self.historical_data.get_database_stats()
            logger.info(f"Database stats: {db_stats}")
            
            websocket_status = 'Connected' if self.websocket_service.is_connected else 'Disconnected'
            logger.info(f"WebSocket status: {websocket_status}")
            
            stats = {
                'database_stats': db_stats,
                'websocket_status': websocket_status,
                'available_indicators': len(self.available_indicators),
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"Screening stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting screening stats: {e}")
            return {}
