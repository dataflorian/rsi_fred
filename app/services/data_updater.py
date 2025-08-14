import logging
from typing import List, Dict, Optional
from app.services.binance_service import BinanceService
from app.services.rsi_calculator import RSICalculator
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataUpdater:
    def __init__(self, rsi_period: int = 14, top_coins_limit: int = 10):
        """
        Initialize Data Updater for RSI screening
        
        Args:
            rsi_period (int): RSI calculation period (default: 14)
            top_coins_limit (int): Number of top coins to return (default: 10)
        """
        self.rsi_period = rsi_period
        self.top_coins_limit = top_coins_limit
        self.binance_service = BinanceService()
        self.rsi_calculator = RSICalculator(period=rsi_period)
        self.last_update = None
        self.cached_results = []
        
        logger.info(f"Data Updater initialized with RSI period {rsi_period} and top {top_coins_limit} coins")
    
    def get_top_performing_coins(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get top performing coins based on RSI analysis
        
        Args:
            force_refresh (bool): Force refresh data even if recently updated
            
        Returns:
            List[Dict]: List of top performing coins with RSI data
        """
        # Check if we should use cached results (update every 15 minutes)
        if not force_refresh and self.cached_results and self.last_update:
            time_since_update = datetime.now() - self.last_update
            if time_since_update < timedelta(minutes=15):
                logger.info("Using cached results (updated recently)")
                return self.cached_results
        
        try:
            logger.info("Fetching fresh data for RSI screening...")
            
            # Get top 50 coins by volume for initial screening
            volume_coins = self.binance_service.get_top_coins_by_volume(limit=50)
            
            if not volume_coins:
                logger.warning("No coins found for screening")
                return []
            
            # Analyze each coin and calculate RSI
            analyzed_coins = []
            
            for coin in volume_coins:
                symbol = coin['symbol']
                
                # Fetch OHLCV data for RSI calculation
                ohlcv_data = self.binance_service.get_ohlcv(symbol, '1h', limit=100)
                
                if ohlcv_data:
                    # Calculate RSI and analyze market data
                    analysis = self.rsi_calculator.analyze_market_data(ohlcv_data)
                    
                    if analysis['rsi'] is not None:
                        # Create comprehensive coin data
                        coin_data = {
                            'symbol': symbol,
                            'base': coin['base'],
                            'price': analysis['last_price'] or coin['price'],
                            'rsi': analysis['rsi'],
                            'signal': analysis['signal'],
                            'price_change_24h': coin['change_24h'],
                            'volume_24h': coin['volume_24h'],
                            'price_change_period': analysis['price_change'],
                            'data_points': analysis['data_points'],
                            'binance_link': f"https://www.binance.com/en/trade/{symbol.replace('/', '_')}",
                            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        analyzed_coins.append(coin_data)
                        
                        logger.debug(f"Analyzed {symbol}: RSI={analysis['rsi']:.2f}, Signal={analysis['signal']}")
                
                # Add small delay to respect rate limits
                import time
                time.sleep(0.1)
            
            # Rank coins by RSI performance (higher RSI = better performance)
            # We want coins that are showing strength (RSI > 50) but not overbought (RSI < 70)
            ranked_coins = self._rank_coins_by_performance(analyzed_coins)
            
            # Take top N coins
            top_coins = ranked_coins[:self.top_coins_limit]
            
            # Cache results
            self.cached_results = top_coins
            self.last_update = datetime.now()
            
            logger.info(f"Successfully analyzed {len(analyzed_coins)} coins, returning top {len(top_coins)}")
            return top_coins
            
        except Exception as e:
            logger.error(f"Error in get_top_performing_coins: {e}")
            # Return cached results if available, otherwise empty list
            return self.cached_results if self.cached_results else []
    
    def _rank_coins_by_performance(self, coins: List[Dict]) -> List[Dict]:
        """
        Rank coins by RSI performance using a scoring system
        
        Args:
            coins (List[Dict]): List of analyzed coins
            
        Returns:
            List[Dict]: Ranked coins by performance score
        """
        def calculate_performance_score(coin: Dict) -> float:
            """Calculate performance score based on RSI and other factors"""
            rsi = coin['rsi']
            
            # Base score from RSI (0-100)
            # We want coins with RSI between 50-70 (showing strength but not overbought)
            if rsi >= 50 and rsi < 70:
                base_score = rsi * 1.5  # Bonus for optimal range
            elif rsi >= 40 and rsi < 50:
                base_score = rsi * 1.2  # Good potential
            elif rsi >= 70:
                base_score = rsi * 0.7  # Penalty for overbought
            else:
                base_score = rsi * 0.5  # Penalty for oversold
            
            # Volume bonus (higher volume = more interest)
            volume_bonus = min(coin['volume_24h'] / 1000000, 10)  # Cap at 10 points
            
            # Price change bonus (positive changes are good)
            price_bonus = max(coin['price_change_24h'], 0) * 0.1
            
            total_score = base_score + volume_bonus + price_bonus
            return total_score
        
        # Sort by performance score (highest first)
        ranked_coins = sorted(coins, key=calculate_performance_score, reverse=True)
        
        # Add rank to each coin
        for i, coin in enumerate(ranked_coins):
            coin['rank'] = i + 1
            coin['performance_score'] = round(calculate_performance_score(coin), 2)
        
        return ranked_coins
    
    def get_screening_stats(self) -> Dict:
        """
        Get statistics about the current screening
        
        Returns:
            Dict: Screening statistics
        """
        if not self.cached_results:
            return {
                'total_coins_analyzed': 0,
                'last_update': None,
                'next_update': None,
                'top_performer': None
            }
        
        next_update = self.last_update + timedelta(minutes=15) if self.last_update else None
        
        return {
            'total_coins_analyzed': len(self.cached_results),
            'last_update': self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else None,
            'next_update': next_update.strftime('%Y-%m-%d %H:%M:%S') if next_update else None,
            'top_performer': {
                'symbol': self.cached_results[0]['symbol'],
                'rsi': self.cached_results[0]['rsi'],
                'signal': self.cached_results[0]['signal']
            } if self.cached_results else None
        }
