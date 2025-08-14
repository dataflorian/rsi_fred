import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # RSI Configuration
    RSI_PERIOD = int(os.environ.get('RSI_PERIOD', 14))
    TOP_COINS_LIMIT = int(os.environ.get('TOP_COINS_LIMIT', 10))
    REFRESH_INTERVAL_MINUTES = int(os.environ.get('REFRESH_INTERVAL_MINUTES', 15))
    
    # API Configuration
    BINANCE_RATE_LIMIT = True
    OHLCV_LIMIT = int(os.environ.get('OHLCV_LIMIT', 100))
    SCREENING_COINS_LIMIT = int(os.environ.get('SCREENING_COINS_LIMIT', 50))
    
    # Cache Configuration
    CACHE_DURATION = timedelta(minutes=REFRESH_INTERVAL_MINUTES)
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Production overrides
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
