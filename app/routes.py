from flask import Blueprint, render_template_string
from app.services.binance_service import BinanceService
from app.services.rsi_calculator import RSICalculator
from app.services.data_updater import DataUpdater
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
