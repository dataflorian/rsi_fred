from flask import Blueprint, render_template_string
from app.services.binance_service import BinanceService
from app.services.rsi_calculator import RSICalculator
from app.services.data_updater import DataUpdater
from app.services.enhanced_screener_service import EnhancedScreenerService
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RSI Crypto Screener</title>
    </head>
    <body>
        <h1>RSI Crypto Screener</h1>
        <p>Application is running successfully!</p>
        <p>Project structure is now organized!</p>
        <p><a href="/test-api">Test Binance API Connection</a></p>
        <p><a href="/test-rsi">Test RSI Calculations</a></p>
        <p><a href="/screener">🚀 Main RSI Screener</a></p>
        <p><a href="/enhanced-screener">🚀 Enhanced Multi-Indicator Screener</a></p>
        <p><a href="/debug">🐛 Debug Configuration</a></p>
    </body>
    </html>
    """
    return html

@main_bp.route('/debug')
def debug():
    """Debug route to check configuration and environment"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug Configuration</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .error {{ color: red; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            pre {{ background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>🐛 Debug Configuration</h1>
        
        <div class="section">
            <h2>Environment Variables</h2>
            <p><strong>FLASK_ENV:</strong> <span class="{'success' if os.environ.get('FLASK_ENV') == 'production' else 'warning'}">{os.environ.get('FLASK_ENV', 'NOT SET')}</span></p>
            <p><strong>SECRET_KEY:</strong> <span class="{'success' if os.environ.get('SECRET_KEY') else 'error'}">{'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}</span></p>
            <p><strong>RSI_PERIOD:</strong> {os.environ.get('RSI_PERIOD', '14 (default)')}</p>
            <p><strong>TOP_COINS_LIMIT:</strong> {os.environ.get('TOP_COINS_LIMIT', '10 (default)')}</p>
        </div>
        
        <div class="section">
            <h2>Configuration Status</h2>
            <p><strong>Debug Mode:</strong> <span class="{'warning' if os.environ.get('FLASK_ENV') == 'development' else 'success'}">{'ON' if os.environ.get('FLASK_ENV') == 'development' else 'OFF'}</span></p>
            <p><strong>Production Mode:</strong> <span class="{'success' if os.environ.get('FLASK_ENV') == 'production' else 'warning'}">{'ON' if os.environ.get('FLASK_ENV') == 'production' else 'OFF'}</span></p>
        </div>
        
        <div class="section">
            <h2>All Environment Variables</h2>
            <pre>{chr(10).join([f"{k}={v}" for k, v in sorted(os.environ.items())])}</pre>
        </div>
        
        <p><a href="/">← Back to Home</a></p>
    </body>
    </html>
    """
    return html

@main_bp.route('/test-api')
def test_api():
    """Test Binance WebSocket connection"""
    try:
        from app.services.websocket_service import BinanceWebSocketService
        
        websocket_service = BinanceWebSocketService()
        result = websocket_service.test_connection()
        
        if result['success']:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Binance WebSocket Test</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .success {{ color: green; }}
                    .error {{ color: red; }}
                    .info {{ color: blue; }}
                    .section {{ margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                    .websocket {{ background: #e8f5e8; border-left: 4px solid #4caf50; }}
                </style>
            </head>
            <body>
                <h1>🔌 Binance WebSocket Connection Test</h1>
                <div class="section websocket">
                    <p class="success">✅ {result['message']}</p>
                    <p><strong>Total Streams:</strong> {result['total_streams']}</p>
                </div>
                
                <div class="section">
                    <h3>📊 Sample Real-time Data:</h3>
                    <ul>
                        {chr(10).join([f'<li><strong>{symbol}:</strong> {price}</li>' for symbol, price in result['sample_data'].items()])}
                    </ul>
                </div>
                
                <div class="section">
                    <h3>🚀 WebSocket Benefits:</h3>
                    <ul>
                        <li>✅ No rate limiting</li>
                        <li>✅ Real-time data updates</li>
                        <li>✅ Efficient single connection</li>
                        <li>✅ Handles hundreds of symbols</li>
                    </ul>
                </div>
                
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        else:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Binance WebSocket Test</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .error {{ color: red; }}
                    .section {{ margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>🔌 Binance WebSocket Connection Test</h1>
                <div class="section">
                    <p class="error">❌ {result['message']}</p>
                    <p><strong>Error Details:</strong> {result.get('error', 'Unknown error')}</p>
                </div>
                
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        
        return html
        
    except Exception as e:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Binance WebSocket Test</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>🔌 Binance WebSocket Connection Test</h1>
            <p class="error">❌ Failed to initialize WebSocket service: {str(e)}</p>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        return html

@main_bp.route('/test-rsi')
def test_rsi():
    """Test route to verify RSI calculations"""
    try:
        binance_service = BinanceService()
        rsi_calculator = RSICalculator(period=14)
        
        # Get top 5 coins by volume for testing
        top_coins = binance_service.get_top_coins_by_volume(limit=5)
        
        if not top_coins:
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>RSI Test - RSI Crypto Screener</title>
            </head>
            <body>
                <h1>RSI Calculation Test</h1>
                <p style="color: red;">❌ Failed to fetch top coins</p>
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSI Test - RSI Crypto Screener</title>
            <style>
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .rsi-high { color: #e74c3c; }
                .rsi-low { color: #27ae60; }
                .rsi-neutral { color: #f39c12; }
            </style>
        </head>
        <body>
            <h1>RSI Calculation Test</h1>
            <p>Testing RSI calculations with top 5 coins by volume:</p>
            <table>
                <tr>
                    <th>Symbol</th>
                    <th>Price</th>
                    <th>RSI (14)</th>
                    <th>Signal</th>
                    <th>Price Change %</th>
                    <th>Data Points</th>
                </tr>
        """
        
        for coin in top_coins:
            symbol = coin['symbol']
            
            # Fetch OHLCV data for RSI calculation
            ohlcv_data = binance_service.get_ohlcv(symbol, '1h', limit=100)
            
            if ohlcv_data:
                # Calculate RSI
                analysis = rsi_calculator.analyze_market_data(ohlcv_data)
                
                # Style RSI values
                rsi_class = ""
                if analysis['rsi']:
                    if analysis['rsi'] >= 70:
                        rsi_class = "rsi-high"
                    elif analysis['rsi'] <= 30:
                        rsi_class = "rsi-low"
                    else:
                        rsi_class = "rsi-neutral"
                
                html += f"""
                <tr>
                    <td><strong>{symbol}</strong></td>
                    <td>${f"{analysis['last_price']:.4f}" if analysis['last_price'] else 'N/A'}</td>
                    <td class="{rsi_class}">{analysis['rsi'] if analysis['rsi'] else 'N/A'}</td>
                    <td>{analysis['signal']}</td>
                    <td>{f"{analysis['price_change']}%" if analysis['price_change'] is not None else 'N/A'}</td>
                    <td>{analysis['data_points']}</td>
                </tr>
                """
            else:
                html += f"""
                <tr>
                    <td><strong>{symbol}</strong></td>
                    <td>${coin['price']:.4f}</td>
                    <td colspan="4" style="color: red;">Failed to fetch data</td>
                </tr>
                """
        
        html += """
            </table>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSI Test - RSI Crypto Screener</title>
        </head>
        <body>
            <h1>RSI Calculation Test</h1>
            <p style="color: red;">❌ RSI test failed: {str(e)}</p>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        return html

@main_bp.route('/screener')
def screener():
    """Main RSI screener showing top 10 performing coins using WebSocket data"""
    try:
        print("DEBUG: Starting WebSocket screener route")  # Debug log
        
        # Test WebSocket connection first
        try:
            from app.services.websocket_service import BinanceWebSocketService
            
            websocket_service = BinanceWebSocketService()
            print("DEBUG: WebSocket service created successfully")  # Debug log
            
            # Test basic connection
            connection_test = websocket_service.test_connection()
            print(f"DEBUG: WebSocket connection test result: {connection_test}")  # Debug log
            
            if not connection_test['success']:
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>RSI Screener - RSI Crypto Screener</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .error {{ color: red; }}
                        .debug {{ background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                        .websocket {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
                    </style>
                </head>
                <body>
                    <h1>🚀 RSI Crypto Screener (WebSocket)</h1>
                    <div class="websocket">
                        <p class="error">❌ WebSocket Connection Failed</p>
                        <p><strong>Error:</strong> {connection_test.get('error', 'Unknown error')}</p>
                    </div>
                    
                    <div class="debug">
                        <h3>🔍 Debug Information:</h3>
                        <p><strong>Connection Status:</strong> {connection_test.get('message', 'No message')}</p>
                        <p><strong>Service Type:</strong> WebSocket (Real-time)</p>
                        <p><strong>Rate Limiting:</strong> None (WebSocket streams)</p>
                    </div>
                    
                    <p><a href="/test-api">🔧 Test WebSocket Connection</a></p>
                    <p><a href="/debug">🐛 Debug Configuration</a></p>
                    <p><a href="/">← Back to Home</a></p>
                </body>
                </html>
                """
            
        except Exception as e:
            print(f"DEBUG: WebSocket service creation failed: {e}")  # Debug log
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>RSI Screener - RSI Crypto Screener</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .error {{ color: red; }}
                </style>
            </body>
            <body>
                <h1>🚀 RSI Crypto Screener (WebSocket)</h1>
                <p class="error">❌ Failed to create WebSocket service</p>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><a href="/debug">🐛 Debug Configuration</a></p>
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        
        # For now, show WebSocket connection success
        # In the next step, we'll integrate the actual data processing
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSI Screener - RSI Crypto Screener</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .success {{ color: #28a745; }}
                .info {{ background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .websocket {{ background: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .next-steps {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 RSI Crypto Screener (WebSocket)</h1>
                
                <div class="websocket">
                    <h2>✅ WebSocket Connection Successful!</h2>
                    <p><strong>Status:</strong> {connection_test.get('message', 'Connected')}</p>
                    <p><strong>Total Streams:</strong> {connection_test.get('total_streams', 'N/A')}</p>
                    <p><strong>Sample Data:</strong> {connection_test.get('sample_data', {})}</p>
                </div>
                
                <div class="info">
                    <h3>🔌 WebSocket Benefits Achieved:</h3>
                    <ul>
                        <li>✅ <strong>No Rate Limiting:</strong> WebSocket streams have much higher limits</li>
                        <li>✅ <strong>Real-time Updates:</strong> Live price data instead of polling</li>
                        <li>✅ <strong>Efficient:</strong> Single connection for multiple data streams</li>
                        <li>✅ <strong>Scalable:</strong> Can handle hundreds of symbols simultaneously</li>
                    </ul>
                </div>
                
                <div class="next-steps">
                    <h3>🔄 Next Steps:</h3>
                    <p><strong>Current Status:</strong> WebSocket connection working ✅</p>
                    <p><strong>Next:</strong> Integrating data processing and RSI calculations</p>
                    <p><strong>ETA:</strong> 1-2 more iterations to complete</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p><a href="/test-api">🔧 Test WebSocket Connection</a></p>
                    <p><a href="/debug">🐛 Debug Configuration</a></p>
                    <p><a href="/">← Back to Home</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSI Screener - RSI Crypto Screener</title>
        </head>
        <body>
            <h1>RSI Crypto Screener</h1>
            <p style="color: red;">❌ Screener failed: {str(e)}</p>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        return html

@main_bp.route('/enhanced-screener')
def enhanced_screener():
    """Enhanced screener with multiple indicators and heatmap"""
    try:
        screener_service = EnhancedScreenerService()
        
        # Get available indicators
        available_indicators = screener_service.available_indicators
        
        # Get screening results (default to RSI)
        results = screener_service.get_screening_results(selected_indicator='rsi', percentile=95)
        
        # Get heatmap data
        heatmap_data = screener_service.get_heatmap_data(selected_indicator='rsi', days=30)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Crypto Screener</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                .indicator-selector {{ background: #e3f2fd; border-left: 4px solid #2196f3; }}
                .results {{ background: #f3e5f5; border-left: 4px solid #9c27b0; }}
                .heatmap {{ background: #e8f5e8; border-left: 4px solid #4caf50; }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
                .info {{ color: #17a2b8; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .coin-row:hover {{ background-color: #f5f5f5; }}
                .signal-bullish {{ color: #28a745; font-weight: bold; }}
                .signal-bearish {{ color: #dc3545; font-weight: bold; }}
                .signal-neutral {{ color: #6c757d; }}
                .signal-oversold {{ color: #fd7e14; }}
                .signal-overbought {{ color: #e83e8c; }}
                .btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }}
                .btn:hover {{ background: #0056b3; }}
                .btn-secondary {{ background: #6c757d; }}
                .btn-secondary:hover {{ background: #545b62; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Enhanced Crypto Screener</h1>
                    <p>Multi-indicator analysis with 95th percentile filtering</p>
                </div>
                
                <div class="section indicator-selector">
                    <h2>📊 Indicator Selection</h2>
                    <p><strong>Available Indicators:</strong></p>
                    <ul>
                        <li><strong>RSI:</strong> Relative Strength Index - Momentum oscillator</li>
                        <li><strong>Returns vs BTC:</strong> 24h performance relative to Bitcoin</li>
                        <li><strong>Mansfield RS:</strong> Mansfield Relative Strength ratio</li>
                        <li><strong>ROC:</strong> Rate of Change - Price momentum</li>
                        <li><strong>VWAP:</strong> Volume Weighted Average Price</li>
                    </ul>
                    
                    <div style="margin: 20px 0;">
                        <a href="/enhanced-screener?indicator=rsi" class="btn">RSI Analysis</a>
                        <a href="/enhanced-screener?indicator=returns_vs_btc" class="btn">Returns vs BTC</a>
                        <a href="/enhanced-screener?indicator=mansfield_rs" class="btn">Mansfield RS</a>
                        <a href="/enhanced-screener?indicator=roc" class="btn">ROC Analysis</a>
                        <a href="/enhanced-screener?indicator=vwap" class="btn">VWAP Analysis</a>
                    </div>
                </div>
                
                <div class="section results">
                    <h2>🏆 Top 5th Percentile Results</h2>
                    <p><strong>Current Indicator:</strong> {results.get('selected_indicator', 'rsi').upper()}</p>
                    <p><strong>Description:</strong> {results.get('indicator_description', 'N/A')}</p>
                    <p><strong>Total Coins Analyzed:</strong> {results.get('total_coins_analyzed', 0)}</p>
                    <p><strong>Top Percentile Count:</strong> {results.get('top_percentile_count', 0)}</p>
                    <p><strong>Last Updated:</strong> {results.get('timestamp', 'N/A')}</p>
                    
                    {_render_coins_table(results.get('coins', [])) if results.get('success') else f'<p class="error">❌ {results.get("message", "No data available")}</p>'}
                </div>
                
                <div class="section heatmap">
                    <h2>📈 Historical Data Heatmap</h2>
                    <p><strong>Data Period:</strong> Last 30 days</p>
                    <p><strong>Update Frequency:</strong> Hourly</p>
                    <p><strong>Total Coins:</strong> {heatmap_data.get('data', {}).get('metadata', {}).get('total_coins', 0)}</p>
                    
                    {_render_heatmap_preview(heatmap_data) if heatmap_data.get('success') else f'<p class="error">❌ {heatmap_data.get("message", "No heatmap data available")}</p>'}
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="/" class="btn btn-secondary">← Back to Home</a>
                    <a href="/test-api" class="btn">🔧 Test WebSocket</a>
                    <a href="/debug" class="btn">🐛 Debug</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Screener - Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>🚀 Enhanced Crypto Screener</h1>
            <p class="error">❌ Enhanced screener failed: {str(e)}</p>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        return html

def _render_coins_table(coins):
    """Helper method to render coins table"""
    if not coins:
        return '<p>No coins data available</p>'
    
    html = '''
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Symbol</th>
                <th>Price</th>
                <th>Indicator Value</th>
                <th>Signal</th>
                <th>24h Change</th>
                <th>Volume (24h)</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    for i, coin in enumerate(coins, 1):
        symbol = coin.get('symbol', 'N/A')
        price = coin.get('price', 0)
        indicator_value = coin.get('indicator_value', 0)
        signal = coin.get('indicator_signal', 'Unknown')
        price_change = coin.get('price_change_24h', 0)
        volume = coin.get('volume_24h', 0)
        
        # Format signal class
        signal_class = 'signal-neutral'
        if 'bullish' in signal.lower() or 'strong' in signal.lower() or 'positive' in signal.lower():
            signal_class = 'signal-bullish'
        elif 'bearish' in signal.lower() or 'weak' in signal.lower() or 'negative' in signal.lower():
            signal_class = 'signal-bearish'
        elif 'oversold' in signal.lower():
            signal_class = 'signal-oversold'
        elif 'overbought' in signal.lower():
            signal_class = 'signal-overbought'
        
        html += f'''
            <tr class="coin-row">
                <td>{i}</td>
                <td><strong>{symbol}</strong></td>
                <td>${f"{price:.6f}" if price else 'N/A'}</td>
                <td>{f"{indicator_value:.2f}" if indicator_value else 'N/A'}</td>
                <td class="{signal_class}">{signal}</td>
                <td class="{'signal-bullish' if price_change > 0 else 'signal-bearish' if price_change < 0 else 'signal-neutral'}">
                    {f"{price_change:+.2f}%" if price_change is not None else 'N/A'}
                </td>
                <td>{f"{volume:,.0f}" if volume else 'N/A'}</td>
                <td><a href="https://www.binance.com/en/trade/{symbol.replace('/', '_')}" target="_blank" class="btn">Trade</a></td>
            </tr>
        '''
    
    html += '''
        </tbody>
    </table>
    '''
    
    return html

def _render_heatmap_preview(heatmap_data):
    """Helper method to render heatmap preview"""
    if not heatmap_data.get('data', {}).get('coins'):
        return '<p>No heatmap data available</p>'
    
    coins = heatmap_data['data']['coins'][:10]  # Show top 10 for preview
    
    html = '''
    <div style="overflow-x: auto;">
        <table style="font-size: 12px;">
            <thead>
                <tr>
                    <th>Coin</th>
                    <th>Current Value</th>
                    <th>Signal</th>
                    <th>Price</th>
                    <th>Volume</th>
                </tr>
            </thead>
            <tbody>
    '''
    
    for coin in coins:
        symbol = coin.get('symbol', 'N/A')
        current_value = coin.get('current_value', 0)
        signal = coin.get('signal', 'Unknown')
        price = coin.get('price', 0)
        volume = coin.get('volume_24h', 0)
        
        html += f'''
            <tr>
                <td><strong>{symbol}</strong></td>
                <td>{f"{current_value:.2f}" if current_value else 'N/A'}</td>
                <td>{signal}</td>
                <td>${f"{price:.6f}" if price else 'N/A'}</td>
                <td>{f"{volume:,.0f}" if volume else 'N/A'}</td>
            </tr>
        '''
    
    html += '''
            </tbody>
        </table>
    </div>
    <p><em>Note: Full interactive heatmap with 30-day historical data will be implemented in the next phase.</em></p>
    '''
    
    return html
