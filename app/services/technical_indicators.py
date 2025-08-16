import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Service for calculating various technical indicators"""
    
    def __init__(self):
        logger.info("Initializing Technical Indicators service")
        self.indicators = {
            'rsi': 'Relative Strength Index',
            'returns_vs_btc': '24h Returns vs Bitcoin',
            'mansfield_rs': 'Mansfield Relative Strength',
            'roc': 'Rate of Change',
            'vwap': 'Volume Weighted Average Price'
        }
        logger.info(f"Available indicators: {list(self.indicators.keys())}")
    
    def calculate_all_indicators(self, coin_data: Dict, btc_data: Dict) -> Dict:
        """Calculate all technical indicators for a coin"""
        try:
            logger.debug(f"Calculating indicators for coin: {coin_data.get('symbol', 'Unknown')}")
            logger.debug(f"Coin data: {coin_data}")
            logger.debug(f"BTC data: {btc_data}")
            
            indicators = {}
            
            # RSI (14-period)
            if 'rsi' in coin_data:
                indicators['rsi'] = coin_data['rsi']
                logger.debug(f"RSI: {indicators['rsi']}")
            
            # 24h Returns vs BTC
            if 'price_change_24h' in coin_data and 'price_change_24h' in btc_data:
                coin_change = coin_data['price_change_24h'] or 0
                btc_change = btc_data['price_change_24h'] or 0
                indicators['returns_vs_btc'] = coin_change - btc_change
                logger.debug(f"Returns vs BTC: {indicators['returns_vs_btc']}")
            
            # Mansfield Relative Strength
            if 'price_change_24h' in coin_data and 'price_change_24h' in btc_data:
                indicators['mansfield_rs'] = self._calculate_mansfield_rs(
                    coin_data.get('price_change_24h', 0),
                    btc_data.get('price_change_24h', 0)
                )
                logger.debug(f"Mansfield RS: {indicators['mansfield_rs']}")
            
            # ROC (Rate of Change)
            if 'price_change_24h' in coin_data:
                indicators['roc'] = coin_data['price_change_24h'] or 0
                logger.debug(f"ROC: {indicators['roc']}")
            
            # VWAP (simplified - using 24h average price)
            if 'price' in coin_data and 'volume_24h' in coin_data:
                indicators['vwap'] = coin_data['price']  # Simplified for now
                logger.debug(f"VWAP: {indicators['vwap']}")
            
            logger.debug(f"Calculated indicators: {indicators}")
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
    
    def _calculate_mansfield_rs(self, coin_change: float, btc_change: float) -> float:
        """Calculate Mansfield Relative Strength"""
        try:
            logger.debug(f"Calculating Mansfield RS: coin_change={coin_change}, btc_change={btc_change}")
            
            if btc_change == 0:
                logger.debug("BTC change is 0, returning 0")
                return 0.0
            
            # Mansfield RS = (1 + coin_change) / (1 + btc_change) - 1
            mansfield_rs = ((1 + coin_change/100) / (1 + btc_change/100)) - 1
            result = mansfield_rs * 100  # Convert to percentage
            
            logger.debug(f"Mansfield RS calculated: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating Mansfield RS: {e}")
            return 0.0
    
    def get_indicator_description(self, indicator: str) -> str:
        """Get description for an indicator"""
        description = self.indicators.get(indicator, 'Unknown indicator')
        logger.debug(f"Description for {indicator}: {description}")
        return description
    
    def get_indicator_signal(self, indicator: str, value: float) -> str:
        """Get trading signal based on indicator value"""
        try:
            logger.debug(f"Getting signal for {indicator}={value}")
            
            if indicator == 'rsi':
                if value >= 70:
                    signal = 'Overbought'
                elif value <= 30:
                    signal = 'Oversold'
                elif value >= 50:
                    signal = 'Bullish'
                else:
                    signal = 'Bearish'
                
            elif indicator == 'returns_vs_btc':
                if value > 5:
                    signal = 'Strong Outperformance'
                elif value > 0:
                    signal = 'Outperforming'
                elif value > -5:
                    signal = 'Underperforming'
                else:
                    signal = 'Weak Underperformance'
                
            elif indicator == 'mansfield_rs':
                if value > 10:
                    signal = 'Very Strong'
                elif value > 5:
                    signal = 'Strong'
                elif value > 0:
                    signal = 'Positive'
                elif value > -5:
                    signal = 'Weak'
                else:
                    signal = 'Very Weak'
                
            elif indicator == 'roc':
                if value > 20:
                    signal = 'Very Strong Momentum'
                elif value > 10:
                    signal = 'Strong Momentum'
                elif value > 0:
                    signal = 'Positive Momentum'
                elif value > -10:
                    signal = 'Weak Momentum'
                else:
                    signal = 'Very Weak Momentum'
                
            else:
                signal = 'Neutral'
            
            logger.debug(f"Signal for {indicator}={value}: {signal}")
            return signal
                
        except Exception as e:
            logger.error(f"Error getting indicator signal: {e}")
            return 'Unknown'
    
    def rank_coins_by_indicator(self, coins_data: List[Dict], indicator: str, btc_data: Dict) -> List[Dict]:
        """Rank coins by a specific indicator"""
        try:
            logger.info(f"Ranking {len(coins_data)} coins by indicator: {indicator}")
            
            ranked_coins = []
            
            for coin in coins_data:
                logger.debug(f"Processing coin: {coin.get('symbol', 'Unknown')}")
                indicators = self.calculate_all_indicators(coin, btc_data)
                if indicator in indicators:
                    coin_copy = coin.copy()
                    coin_copy['indicator_value'] = indicators[indicator]
                    coin_copy['indicator_signal'] = self.get_indicator_signal(indicator, indicators[indicator])
                    ranked_coins.append(coin_copy)
                    logger.debug(f"Added {coin.get('symbol', 'Unknown')} with {indicator}={indicators[indicator]}")
                else:
                    logger.warning(f"Indicator {indicator} not found for {coin.get('symbol', 'Unknown')}")
            
            # Sort by indicator value (descending for most indicators)
            if indicator in ['rsi', 'returns_vs_btc', 'mansfield_rs', 'roc']:
                ranked_coins.sort(key=lambda x: x['indicator_value'], reverse=True)
                logger.debug(f"Sorted {len(ranked_coins)} coins by {indicator} (descending)")
            else:
                ranked_coins.sort(key=lambda x: x['indicator_value'])
                logger.debug(f"Sorted {len(ranked_coins)} coins by {indicator} (ascending)")
            
            logger.info(f"Ranked {len(ranked_coins)} coins by {indicator}")
            return ranked_coins
            
        except Exception as e:
            logger.error(f"Error ranking coins by indicator: {e}")
            return []
    
    def get_top_percentile_coins(self, ranked_coins: List[Dict], percentile: float = 95) -> List[Dict]:
        """Get top percentile coins based on ranking"""
        try:
            logger.info(f"Getting top {100-percentile}% coins from {len(ranked_coins)} ranked coins")
            
            if not ranked_coins:
                logger.warning("No ranked coins provided")
                return []
            
            # Calculate how many coins represent the top percentile
            top_count = max(1, int(len(ranked_coins) * (100 - percentile) / 100))
            logger.info(f"Top {100-percentile}% represents {top_count} coins")
            
            top_coins = ranked_coins[:top_count]
            logger.info(f"Selected top {len(top_coins)} coins: {[c.get('symbol', 'Unknown') for c in top_coins]}")
            
            return top_coins
            
        except Exception as e:
            logger.error(f"Error getting top percentile coins: {e}")
            return ranked_coins[:10]  # Fallback to top 10
