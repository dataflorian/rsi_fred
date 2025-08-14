import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RSICalculator:
    def __init__(self, period: int = 14):
        """
        Initialize RSI Calculator
        
        Args:
            period (int): RSI calculation period (default: 14)
        """
        self.period = period
        logger.info(f"RSI Calculator initialized with period {period}")
    
    def calculate_rsi(self, prices: List[float]) -> Optional[float]:
        """
        Calculate RSI for a list of prices
        
        Args:
            prices (List[float]): List of closing prices
            
        Returns:
            Optional[float]: RSI value or None if insufficient data
        """
        if len(prices) < self.period + 1:
            logger.warning(f"Insufficient data for RSI calculation. Need {self.period + 1}, got {len(prices)}")
            return None
        
        try:
            # Convert to numpy array for efficient calculation
            prices_array = np.array(prices)
            
            # Calculate price changes
            deltas = np.diff(prices_array)
            
            # Separate gains and losses
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # Calculate average gains and losses using exponential moving average
            avg_gains = self._exponential_moving_average(gains, self.period)
            avg_losses = self._exponential_moving_average(losses, self.period)
            
            # Calculate RS and RSI
            rs = avg_gains / avg_losses if avg_losses != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            
            # Ensure RSI is within valid range [0, 100]
            rsi = max(0, min(100, rsi))
            
            logger.debug(f"RSI calculated: {rsi:.2f} for {len(prices)} price points")
            return round(rsi, 2)
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return None
    
    def _exponential_moving_average(self, data: np.ndarray, period: int) -> float:
        """
        Calculate exponential moving average
        
        Args:
            data (np.ndarray): Input data
            period (int): EMA period
            
        Returns:
            float: EMA value
        """
        if len(data) == 0:
            return 0.0
        
        # Use simple moving average for the first period
        if len(data) <= period:
            return np.mean(data)
        
        # Calculate EMA
        alpha = 2.0 / (period + 1)
        ema = data[0]  # Start with first value
        
        for i in range(1, len(data)):
            ema = alpha * data[i] + (1 - alpha) * ema
        
        return ema
    
    def get_rsi_signal(self, rsi: float) -> str:
        """
        Get trading signal based on RSI value
        
        Args:
            rsi (float): RSI value
            
        Returns:
            str: Trading signal
        """
        if rsi is None:
            return "Unknown"
        elif rsi >= 70:
            return "Overbought"
        elif rsi <= 30:
            return "Oversold"
        elif rsi >= 60:
            return "Bullish"
        elif rsi <= 40:
            return "Bearish"
        else:
            return "Neutral"
    
    def analyze_market_data(self, ohlcv_data: List[List]) -> Dict:
        """
        Analyze OHLCV data and return RSI analysis
        
        Args:
            ohlcv_data (List[List]): OHLCV data from exchange
            
        Returns:
            Dict: Analysis results
        """
        try:
            if not ohlcv_data or len(ohlcv_data) < self.period + 1:
                return {
                    'rsi': None,
                    'signal': 'Unknown',
                    'price_change': None,
                    'volume_change': None,
                    'data_points': len(ohlcv_data) if ohlcv_data else 0
                }
            
            # Extract closing prices (index 4 in OHLCV)
            closing_prices = [float(candle[4]) for candle in ohlcv_data]
            
            # Calculate RSI
            rsi = self.calculate_rsi(closing_prices)
            signal = self.get_rsi_signal(rsi)
            
            # Calculate price change
            if len(closing_prices) >= 2:
                price_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
            else:
                price_change = None
            
            # Calculate volume change (index 5 in OHLCV)
            if len(ohlcv_data) >= 2:
                volumes = [float(candle[5]) for candle in ohlcv_data]
                volume_change = ((volumes[-1] - volumes[0]) / volumes[0]) * 100 if volumes[0] != 0 else None
            else:
                volume_change = None
            
            return {
                'rsi': rsi,
                'signal': signal,
                'price_change': round(price_change, 2) if price_change is not None else None,
                'volume_change': round(volume_change, 2) if volume_change is not None else None,
                'data_points': len(ohlcv_data),
                'last_price': closing_prices[-1] if closing_prices else None
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market data: {e}")
            return {
                'rsi': None,
                'signal': 'Error',
                'price_change': None,
                'volume_change': None,
                'data_points': 0,
                'last_price': None
            }
