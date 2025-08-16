import sqlite3
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json
import threading
import time

logger = logging.getLogger(__name__)

class HistoricalDataService:
    """Service for managing historical price data"""
    
    def __init__(self, db_path: str = "historical_data.db"):
        logger.info(f"Initializing Historical Data Service with database: {db_path}")
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
        logger.info("Historical Data Service initialized successfully")
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            logger.info("Initializing database tables...")
            
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Create coins table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS coins (
                            symbol TEXT PRIMARY KEY,
                            name TEXT,
                            first_seen TIMESTAMP,
                            last_updated TIMESTAMP
                        )
                    """)
                    logger.debug("Coins table created/verified")
                    
                    # Create price history table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS price_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            symbol TEXT,
                            timestamp TIMESTAMP,
                            price REAL,
                            volume_24h REAL,
                            price_change_24h REAL,
                            rsi REAL,
                            FOREIGN KEY (symbol) REFERENCES coins (symbol)
                        )
                    """)
                    logger.debug("Price history table created/verified")
                    
                    # Create indicators table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS indicators (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            symbol TEXT,
                            timestamp TIMESTAMP,
                            indicator_name TEXT,
                            value REAL,
                            signal TEXT,
                            FOREIGN KEY (symbol) REFERENCES coins (symbol)
                        )
                    """)
                    logger.debug("Indicators table created/verified")
                    
                    # Create indexes for better performance
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_history_symbol_timestamp ON price_history(symbol, timestamp)")
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicators_symbol_timestamp ON indicators(symbol, timestamp)")
                    logger.debug("Database indexes created/verified")
                    
                    conn.commit()
                    logger.info("Database initialization completed successfully")
                    
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def add_coin(self, symbol: str, name: str = None):
        """Add or update a coin in the database"""
        try:
            logger.debug(f"Adding/updating coin: {symbol} ({name})")
            
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Check if coin already exists
                    cursor.execute("SELECT name FROM coins WHERE symbol = ?", (symbol,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        logger.debug(f"Coin {symbol} already exists, updating...")
                        cursor.execute("""
                            UPDATE coins SET name = ?, last_updated = ?
                            WHERE symbol = ?
                        """, (name or symbol, datetime.now(), symbol))
                    else:
                        logger.debug(f"Adding new coin: {symbol}")
                        cursor.execute("""
                            INSERT OR REPLACE INTO coins (symbol, name, first_seen, last_updated)
                            VALUES (?, ?, ?, ?)
                        """, (symbol, name, datetime.now(), datetime.now()))
                    
                    conn.commit()
                    logger.info(f"Added/updated coin: {symbol}")
                    
        except Exception as e:
            logger.error(f"Error adding coin {symbol}: {e}")
    
    def update_price_data(self, symbol: str, price_data: Dict):
        """Update price data for a specific coin"""
        try:
            logger.debug(f"Updating price data for {symbol}: {price_data}")
            
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Update or insert price data
                    cursor.execute("""
                        INSERT OR REPLACE INTO price_history 
                        (symbol, timestamp, price, volume_24h, price_change_24h, rsi)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        symbol,
                        datetime.now(),
                        price_data.get('price', 0),
                        price_data.get('volume_24h', 0),
                        price_data.get('price_change_24h', 0),
                        price_data.get('rsi', 0)
                    ))
                    
                    # Update last_updated in coins table
                    cursor.execute("""
                        UPDATE coins SET last_updated = ? WHERE symbol = ?
                    """, (datetime.now(), symbol))
                    
                    conn.commit()
                    logger.debug(f"Price data updated for {symbol}")
                    
        except Exception as e:
            logger.error(f"Error updating price data for {symbol}: {e}")
    
    def update_indicators(self, symbol: str, indicators: Dict):
        """Update technical indicators for a specific coin"""
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    timestamp = datetime.now()
                    
                    for indicator_name, value in indicators.items():
                        if isinstance(value, dict) and 'value' in value:
                            indicator_value = value['value']
                            signal = value.get('signal', 'Unknown')
                        else:
                            indicator_value = value
                            signal = 'Unknown'
                        
                        cursor.execute("""
                            INSERT OR REPLACE INTO indicators 
                            (symbol, timestamp, indicator_name, value, signal)
                            VALUES (?, ?, ?, ?, ?)
                        """, (symbol, timestamp, indicator_name, indicator_value, signal))
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error updating indicators for {symbol}: {e}")
    
    def get_historical_data(self, symbol: str, days: int = 30, interval: str = '1d') -> pd.DataFrame:
        """Get historical data for a specific coin"""
        try:
            logger.debug(f"Getting historical data for {symbol}, last {days} days")
            
            with sqlite3.connect(self.db_path) as conn:
                # Calculate start date
                start_date = datetime.now() - timedelta(days=days)
                
                query = """
                    SELECT timestamp, price, volume_24h, price_change_24h, rsi
                    FROM price_history
                    WHERE symbol = ? AND timestamp >= ?
                    ORDER BY timestamp ASC
                """
                
                df = pd.read_sql_query(query, conn, params=(symbol, start_date))
                
                if not df.empty:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df.set_index('timestamp', inplace=True)
                    logger.debug(f"Retrieved {len(df)} historical records for {symbol}")
                else:
                    logger.warning(f"No historical data found for {symbol}")
                
                return df
                
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_top_coins_by_volume(self, limit: int = 100) -> List[str]:
        """Get top coins by 24h volume"""
        try:
            logger.debug(f"Getting top {limit} coins by volume from historical data")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT symbol FROM price_history 
                    WHERE timestamp >= datetime('now', '-1 hour')
                    GROUP BY symbol
                    ORDER BY MAX(volume_24h) DESC
                    LIMIT ?
                """, (limit,))
                
                coins = [row[0] for row in cursor.fetchall()]
                logger.debug(f"Historical data returned {len(coins)} coins: {coins[:5]}")
                return coins
                
        except Exception as e:
            logger.error(f"Error getting top coins by volume: {e}")
            return []
    
    def get_coins_with_data(self) -> List[str]:
        """Get list of coins that have recent data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT symbol FROM price_history 
                    WHERE timestamp >= datetime('now', '-2 hours')
                """)
                
                return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting coins with data: {e}")
            return []
    
    def get_latest_indicators(self, symbol: str) -> Dict:
        """Get latest technical indicators for a coin"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT indicator_name, value, signal, timestamp
                    FROM indicators
                    WHERE symbol = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, (symbol,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'indicator_name': result[0],
                        'value': result[1],
                        'signal': result[2],
                        'timestamp': result[3]
                    }
                return {}
                
        except Exception as e:
            logger.error(f"Error getting latest indicators for {symbol}: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to keep database size manageable"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cutoff_date = datetime.now() - timedelta(days=days_to_keep)
                
                # Clean up old price history
                cursor.execute("""
                    DELETE FROM price_history 
                    WHERE timestamp < ?
                """, (cutoff_date,))
                
                # Clean up old indicators
                cursor.execute("""
                    DELETE FROM indicators 
                    WHERE timestamp < ?
                """, (cutoff_date,))
                
                conn.commit()
                logger.info(f"Cleaned up data older than {days_to_keep} days")
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            logger.debug("Getting database statistics")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count coins
                cursor.execute("SELECT COUNT(*) FROM coins")
                total_coins = cursor.fetchone()[0]
                
                # Count price records
                cursor.execute("SELECT COUNT(*) FROM price_history")
                total_price_records = cursor.fetchone()[0]
                
                # Count indicator records
                cursor.execute("SELECT COUNT(*) FROM indicators")
                total_indicator_records = cursor.fetchone()[0]
                
                # Get oldest and newest data
                cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM price_history")
                time_range = cursor.fetchone()
                oldest_data = time_range[0] if time_range[0] else 'None'
                newest_data = time_range[1] if time_range[1] else 'None'
                
                stats = {
                    'total_coins': total_coins,
                    'total_price_records': total_price_records,
                    'total_indicator_records': total_indicator_records,
                    'oldest_data': oldest_data,
                    'newest_data': newest_data
                }
                
                logger.debug(f"Database stats: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
