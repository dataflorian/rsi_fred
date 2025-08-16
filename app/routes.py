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
        
        # Get query parameter for indicator selection
        from flask import request
        selected_indicator = request.args.get('indicator', 'rsi')
        
        # Get screening results for selected indicator
        results = screener_service.get_screening_results(selected_indicator=selected_indicator, percentile=95)
        
        # Get heatmap data for selected indicator
        heatmap_data = screener_service.get_heatmap_data(selected_indicator=selected_indicator, days=30)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Crypto Screener</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Base styles */
                * {{ box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
                    margin: 0; 
                    padding: 10px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    background: white; 
                    padding: 20px; 
                    border-radius: 12px; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    backdrop-filter: blur(10px);
                }}
                
                .header {{ 
                    text-align: center; 
                    margin-bottom: 30px; 
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
                
                .header h1 {{ 
                    font-size: 2.5rem; 
                    margin: 0 0 10px 0; 
                    font-weight: 700;
                }}
                
                .header p {{ 
                    font-size: 1.1rem; 
                    margin: 0; 
                    opacity: 0.7;
                    color: #666;
                }}
                
                .section {{ 
                    margin: 20px 0; 
                    padding: 25px; 
                    border: none;
                    border-radius: 12px; 
                    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}
                
                .section:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
                }}
                
                .indicator-selector {{ 
                    background: linear-gradient(135deg, #e3f2fd 0%, #f1f8ff 100%); 
                    border-left: 4px solid #2196f3; 
                }}
                
                .results {{ 
                    background: linear-gradient(135deg, #f3e5f5 0%, #faf4fb 100%); 
                    border-left: 4px solid #9c27b0; 
                }}
                
                .heatmap {{ 
                    background: linear-gradient(135deg, #e8f5e8 0%, #f4faf4 100%); 
                    border-left: 4px solid #4caf50; 
                }}
                
                /* Button grid for mobile */
                .indicator-buttons {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 12px;
                    margin: 20px 0;
                }}
                
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
                .info {{ color: #17a2b8; }}
                
                /* Responsive table */
                .table-container {{
                    overflow-x: auto;
                    margin: 15px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                }}
                
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 0;
                    background: white;
                }}
                
                th, td {{ 
                    padding: 12px; 
                    text-align: left; 
                    border-bottom: 1px solid #eee; 
                    white-space: nowrap;
                }}
                
                th {{ 
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    font-weight: 600; 
                    color: #495057;
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }}
                
                .coin-row {{ 
                    transition: background-color 0.2s ease; 
                }}
                
                .coin-row:hover {{ 
                    background: linear-gradient(135deg, #f8f9ff 0%, #fff8f9 100%); 
                }}
                
                .signal-bullish {{ color: #28a745; font-weight: 600; }}
                .signal-bearish {{ color: #dc3545; font-weight: 600; }}
                .signal-neutral {{ color: #6c757d; font-weight: 500; }}
                .signal-oversold {{ color: #fd7e14; font-weight: 600; }}
                .signal-overbought {{ color: #e83e8c; font-weight: 600; }}
                
                .btn {{ 
                    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
                    color: white; 
                    padding: 12px 24px; 
                    text-decoration: none; 
                    border-radius: 8px; 
                    display: inline-block; 
                    margin: 6px; 
                    font-weight: 500;
                    transition: all 0.2s ease;
                    border: none;
                    cursor: pointer;
                    text-align: center;
                }}
                
                .btn:hover {{ 
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(0,123,255,0.3);
                }}
                
                .btn-secondary {{ 
                    background: linear-gradient(135deg, #6c757d 0%, #545b62 100%); 
                }}
                
                .btn-secondary:hover {{ 
                    box-shadow: 0 4px 12px rgba(108,117,125,0.3);
                }}
                
                /* Mobile optimizations */
                @media (max-width: 768px) {{
                    body {{ padding: 5px; }}
                    .container {{ padding: 15px; margin: 5px; }}
                    .header h1 {{ font-size: 2rem; }}
                    .header p {{ font-size: 1rem; }}
                    .section {{ padding: 20px; margin: 15px 0; }}
                    
                    .indicator-buttons {{
                        grid-template-columns: 1fr;
                        gap: 8px;
                    }}
                    
                    .btn {{ 
                        padding: 14px 20px; 
                        margin: 4px 0; 
                        width: 100%;
                        font-size: 0.9rem;
                    }}
                    
                    th, td {{ 
                        padding: 8px; 
                        font-size: 0.85rem; 
                    }}
                    
                    .table-container {{
                        font-size: 0.8rem;
                    }}
                }}
                
                @media (max-width: 480px) {{
                    .header h1 {{ font-size: 1.6rem; }}
                    .section {{ padding: 15px; }}
                    th, td {{ padding: 6px; font-size: 0.75rem; }}
                }}
                
                /* Loading spinner */
                .loading-spinner {{
                    width: 40px;
                    height: 40px;
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin-bottom: 15px;
                }}
                
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
                
                /* Notification styles */
                .notification {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    min-width: 300px;
                    max-width: 500px;
                    padding: 0;
                    border-radius: 8px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                    animation: slideIn 0.3s ease-out;
                    transform: translateX(0);
                }}
                
                .notification-success {{
                    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    border-left: 4px solid #28a745;
                }}
                
                .notification-error {{
                    background: linear-gradient(135deg, #f8d7da 0%, #f1b0b7 100%);
                    border-left: 4px solid #dc3545;
                }}
                
                .notification-content {{
                    display: flex;
                    align-items: center;
                    padding: 15px 20px;
                    gap: 12px;
                }}
                
                .notification-icon {{
                    font-size: 1.2rem;
                    flex-shrink: 0;
                }}
                
                .notification-message {{
                    flex: 1;
                    font-weight: 500;
                    color: #333;
                }}
                
                .notification-close {{
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: #666;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: background-color 0.2s ease;
                }}
                
                .notification-close:hover {{
                    background-color: rgba(0,0,0,0.1);
                }}
                
                @keyframes slideIn {{
                    from {{
                        transform: translateX(100%);
                        opacity: 0;
                    }}
                    to {{
                        transform: translateX(0);
                        opacity: 1;
                    }}
                }}
                
                @media (max-width: 768px) {{
                    .notification {{
                        right: 10px;
                        left: 10px;
                        min-width: auto;
                        max-width: none;
                    }}
                }}
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
                    
                    <div class="indicator-buttons">
                        <a href="/enhanced-screener?indicator=rsi" class="btn">📊 RSI Analysis</a>
                        <a href="/enhanced-screener?indicator=returns_vs_btc" class="btn">💰 Returns vs BTC</a>
                        <a href="/enhanced-screener?indicator=mansfield_rs" class="btn">📈 Mansfield RS</a>
                        <a href="/enhanced-screener?indicator=roc" class="btn">⚡ ROC Analysis</a>
                        <a href="/enhanced-screener?indicator=vwap" class="btn">📊 VWAP Analysis</a>
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

@main_bp.route('/api/heatmap-data')
def api_heatmap_data():
    """API endpoint for heatmap data"""
    try:
        from flask import request
        
        # Get query parameters
        indicator = request.args.get('indicator', 'rsi')
        days = int(request.args.get('days', 30))
        
        # Get heatmap data from service
        screener_service = EnhancedScreenerService()
        heatmap_data = screener_service.get_heatmap_data(selected_indicator=indicator, days=days)
        
        if heatmap_data.get('success'):
            return heatmap_data
        else:
            return {
                'success': False,
                'message': heatmap_data.get('message', 'Failed to fetch heatmap data')
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }

def _render_coins_table(coins):
    """Helper method to render coins table"""
    if not coins:
        return '<p>No coins data available</p>'
    
    html = '''
    <div class="table-container">
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
                <td>{f"{indicator_value:.2f}" if indicator_value is not None and indicator_value != 0 else 'N/A'}</td>
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
    </div>
    '''
    
    return html

def _render_heatmap_preview(heatmap_data):
    """Helper method to render interactive Chart.js heatmap"""
    if not heatmap_data.get('data', {}).get('coins'):
        return '<p>No heatmap data available</p>'
    
    coins = heatmap_data['data']['coins'][:10]  # Show top 10 for preview
    
    # Prepare data for Chart.js
    labels = [coin.get('symbol', 'N/A') for coin in coins]
    current_values = [coin.get('current_value', 0) if coin.get('current_value') else 0 for coin in coins]
    prices = [coin.get('price', 0) for coin in coins]
    
    # Generate 30 days of historical data (mock for now)
    days = 30
    historical_data = []
    
    # Get current indicator from URL or default to RSI
    from flask import request
    current_indicator = request.args.get('indicator', 'rsi')
    
    for i in range(days):
        day_data = []
        for coin in coins:
            # Generate realistic values based on selected indicator
            base_value = coin.get('current_value', 0)
            
            if current_indicator == 'rsi':
                # RSI: 20-80 range
                if base_value == 0:
                    base_value = 45 + (hash(f"{coin.get('symbol')}{i}") % 20)
                else:
                    variation = (hash(f"{coin.get('symbol')}{i}") % 30) - 15
                    base_value = max(20, min(80, base_value + variation))
                    
            elif current_indicator == 'returns_vs_btc':
                # Returns vs BTC: -20% to +20% range
                base_value = (hash(f"{coin.get('symbol')}{i}") % 40) - 20
                
            elif current_indicator == 'mansfield_rs':
                # Mansfield RS: 0.5 to 1.5 range
                base_value = 0.5 + (hash(f"{coin.get('symbol')}{i}") % 100) / 100
                
            elif current_indicator == 'roc':
                # ROC: -15% to +15% range
                base_value = (hash(f"{coin.get('symbol')}{i}") % 30) - 15
                
            elif current_indicator == 'vwap':
                # VWAP: Price deviation -5% to +5%
                base_value = (hash(f"{coin.get('symbol')}{i}") % 10) - 5
                
            else:
                # Default fallback
                base_value = 50 + (hash(f"{coin.get('symbol')}{i}") % 20) - 10
                
            day_data.append(round(base_value, 2))
        historical_data.append(day_data)
    
    html = f'''
    <div class="heatmap-container">
        <div class="chart-controls">
            <label for="indicator-select">Indicator:</label>
            <select id="indicator-select" onchange="updateHeatmap()">
                <option value="rsi">RSI</option>
                <option value="returns_vs_btc">Returns vs BTC</option>
                <option value="mansfield_rs">Mansfield RS</option>
                <option value="roc">ROC</option>
                <option value="vwap">VWAP</option>
            </select>
        </div>
        
        <div class="chart-container">
            <canvas id="heatmapChart" width="800" height="400"></canvas>
        </div>
        
        <div class="chart-legend">
            <div class="legend-item">
                <span class="legend-color overbought"></span>
                <span>Overbought (≥70)</span>
            </div>
            <div class="legend-item">
                <span class="legend-color neutral-high"></span>
                <span>Neutral-High (60-69)</span>
            </div>
            <div class="legend-item">
                <span class="legend-color neutral"></span>
                <span>Neutral (40-59)</span>
            </div>
            <div class="legend-item">
                <span class="legend-color neutral-low"></span>
                <span>Neutral-Low (30-39)</span>
            </div>
            <div class="legend-item">
                <span class="legend-color oversold"></span>
                <span>Oversold (<30)</span>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        let heatmapChart;
        
        function initHeatmap() {{
            const ctx = document.getElementById('heatmapChart').getContext('2d');
            
            // Prepare data for heatmap
            const data = {{
                labels: {labels},
                datasets: []
            }};
            
            // Create dataset for each day
            const historicalData = {historical_data};
            const days = {days};
            
            for (let i = 0; i < days; i++) {{
                const dayData = historicalData[i];
                const dataset = {{
                    label: `Day ${{days - i}}`,
                    data: dayData,
                    backgroundColor: dayData.map(value => getColorForValue(value, 'rsi')),
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    borderRadius: 2
                }};
                data.datasets.push(dataset);
            }}
            
            // Create the heatmap chart
            heatmapChart = new Chart(ctx, {{
                type: 'bar',
                data: data,
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: '30-Day Performance Heatmap',
                            font: {{ size: 16 }}
                        }},
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            callbacks: {{
                                title: function(context) {{
                                    return `Day ${{days - context[0].dataIndex}}`;
                                }},
                                label: function(context) {{
                                    return `${{context.dataset.label}}: ${{context.parsed.y.toFixed(2)}}`;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: 'Coins'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: 'Indicator Value'
                            }},
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        }}
        
        function getColorForValue(value, indicator = 'rsi') {{
            // Dynamic color coding based on selected indicator
            if (indicator === 'rsi') {{
                // RSI: 20-80 range
                if (value >= 70) return 'rgba(244, 67, 54, 0.8)';      // Red (Overbought)
                if (value >= 60) return 'rgba(255, 193, 7, 0.8)';      // Yellow (Neutral-High)
                if (value >= 40) return 'rgba(76, 175, 80, 0.8)';      // Green (Neutral)
                if (value >= 30) return 'rgba(255, 193, 7, 0.8)';      // Yellow (Neutral-Low)
                return 'rgba(33, 150, 243, 0.8)';                       // Blue (Oversold)
            }} else if (indicator === 'returns_vs_btc') {{
                // Returns vs BTC: -20% to +20%
                if (value >= 10) return 'rgba(76, 175, 80, 0.8)';      // Green (Strong outperformance)
                if (value >= 5) return 'rgba(255, 193, 7, 0.8)';       // Yellow (Moderate outperformance)
                if (value >= -5) return 'rgba(76, 175, 80, 0.8)';      // Green (Neutral)
                if (value >= -10) return 'rgba(255, 193, 7, 0.8)';     // Yellow (Moderate underperformance)
                return 'rgba(244, 67, 54, 0.8)';                        // Red (Strong underperformance)
            }} else if (indicator === 'mansfield_rs') {{
                // Mansfield RS: 0.5 to 1.5
                if (value >= 1.2) return 'rgba(76, 175, 80, 0.8)';     // Green (Strong relative strength)
                if (value >= 1.1) return 'rgba(255, 193, 7, 0.8)';     // Yellow (Moderate strength)
                if (value >= 0.9) return 'rgba(76, 175, 80, 0.8)';     // Green (Neutral)
                if (value >= 0.8) return 'rgba(255, 193, 7, 0.8)';     // Yellow (Moderate weakness)
                return 'rgba(244, 67, 54, 0.8)';                        // Red (Strong weakness)
            }} else if (indicator === 'roc') {{
                // ROC: -15% to +15%
                if (value >= 8) return 'rgba(76, 175, 80, 0.8)';       // Green (Strong momentum)
                if (value >= 3) return 'rgba(255, 193, 7, 0.8)';       // Yellow (Moderate momentum)
                if (value >= -3) return 'rgba(255, 193, 7, 0.8)';      // Yellow (Neutral)
                if (value >= -8) return 'rgba(255, 193, 7, 0.8)';      // Yellow (Moderate decline)
                return 'rgba(244, 67, 54, 0.8)';                        // Red (Strong decline)
            }} else if (indicator === 'vwap') {{
                // VWAP: -5% to +5%
                if (value >= 3) return 'rgba(244, 67, 54, 0.8)';       // Red (Overvalued)
                if (value >= 1) return 'rgba(255, 193, 7, 0.8)';       // Yellow (Slightly overvalued)
                if (value >= -1) return 'rgba(76, 175, 80, 0.8)';      // Green (Fair value)
                if (value >= -3) return 'rgba(255, 193, 7, 0.8)';      // Yellow (Slightly undervalued)
                return 'rgba(33, 150, 243, 0.8)';                       // Blue (Undervalued)
            }} else {{
                // Default fallback
                if (value >= 70) return 'rgba(244, 67, 54, 0.8)';
                if (value >= 40) return 'rgba(255, 193, 7, 0.8)';
                return 'rgba(76, 175, 80, 0.8)';
            }}
        }}
        
        function updateHeatmap() {{
            const indicator = document.getElementById('indicator-select').value;
            console.log('Switching to indicator:', indicator);
            
            // Show enhanced loading state
            showLoadingState();
            
            // Fetch new data for selected indicator
            fetch(`/api/heatmap-data?indicator=${{indicator}}&days=30`)
                .then(response => {{
                    if (!response.ok) {{
                        throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
                    }}
                    return response.json();
                }})
                .then(data => {{
                    if (data.success) {{
                        // Update chart with new data
                        updateChartData(data.data);
                        hideLoadingState();
                        showSuccessMessage(`${{indicator.toUpperCase().replace(/_/g, ' ')}} data updated successfully!`);
                    }} else {{
                        hideLoadingState();
                        showErrorMessage(`Failed to fetch data: ${{data.message || 'Unknown error'}}`);
                    }}
                }})
                .catch(error => {{
                    hideLoadingState();
                    showErrorMessage(`Network error: ${{error.message}}`);
                    console.error('Error updating heatmap:', error);
                }});
        }}
        
        function showLoadingState() {{
            const chartContainer = document.getElementById('heatmapChart');
            const loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-spinner"></div>
                <p>Loading indicator data...</p>
            `;
            loadingOverlay.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255,255,255,0.9);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                border-radius: 8px;
            `;
            
            const chartContainerWrapper = chartContainer.parentElement;
            chartContainerWrapper.style.position = 'relative';
            chartContainerWrapper.appendChild(loadingOverlay);
            
            chartContainer.style.opacity = '0.3';
        }}
        
        function hideLoadingState() {{
            const loadingOverlay = document.getElementById('loading-overlay');
            const chartContainer = document.getElementById('heatmapChart');
            
            if (loadingOverlay) {{
                loadingOverlay.remove();
            }}
            chartContainer.style.opacity = '1';
        }}
        
        function showSuccessMessage(message) {{
            showNotification(message, 'success');
        }}
        
        function showErrorMessage(message) {{
            showNotification(message, 'error');
        }}
        
        function showNotification(message, type) {{
            // Remove existing notifications
            const existing = document.querySelector('.notification');
            if (existing) existing.remove();
            
            const notification = document.createElement('div');
            notification.className = `notification notification-${{type}}`;
            notification.innerHTML = `
                <div class="notification-content">
                    <span class="notification-icon">${{type === 'success' ? '✅' : '❌'}}</span>
                    <span class="notification-message">${{message}}</span>
                    <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {{
                if (notification.parentElement) {{
                    notification.remove();
                }}
            }}, 5000);
        }}
        
        function updateChartData(heatmapData) {{
            if (!heatmapChart) return;
            
            // Update chart data
            const coins = heatmapData.coins || [];
            const labels = coins.map(coin => coin.symbol);
            
            // Clear existing datasets
            heatmapChart.data.labels = labels;
            heatmapChart.data.datasets = [];
            
            // Add new datasets for each day
            const days = 30;
            for (let i = 0; i < days; i++) {{
                const dayData = coins.map(coin => {{
                    const historicalValues = coin.historical_values || [];
                    return historicalValues[i] || 0;
                }});
                
                const dataset = {{
                    label: `Day ${{days - i}}`,
                    data: dayData,
                    backgroundColor: dayData.map(value => getColorForValue(value, indicatorName)),
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    borderRadius: 2
                }};
                heatmapChart.data.datasets.push(dataset);
            }}
            
            // Update chart title
            const indicatorName = document.getElementById('indicator-select').value;
            const indicatorDisplay = indicatorName.toUpperCase().replace(/_/g, ' ');
            heatmapChart.options.plugins.title.text = `30-Day ${{indicatorDisplay}} Performance Heatmap`;
            
            // Update legend for new indicator
            updateLegend(indicatorName);
            
            // Redraw chart
            heatmapChart.update();
        }}
        
        function updateLegend(indicator) {{
            const legendContainer = document.querySelector('.chart-legend');
            if (!legendContainer) return;
            
            let legendHTML = '';
            
            if (indicator === 'rsi') {{
                legendHTML = '<div class="legend-item">' +
                    '<span class="legend-color overbought"></span>' +
                    '<span>Overbought (≥70)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral-high"></span>' +
                    '<span>Neutral-High (60-69)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral"></span>' +
                    '<span>Neutral (40-59)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral-low"></span>' +
                    '<span>Neutral-Low (30-39)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color oversold"></span>' +
                    '<span>Oversold (<30)</span></div>';
            }} else if (indicator === 'returns_vs_btc') {{
                legendHTML = '<div class="legend-item">' +
                    '<span class="legend-color strong-outperform"></span>' +
                    '<span>Strong Outperformance (≥10%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-outperform"></span>' +
                    '<span>Moderate Outperformance (5-9%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral"></span>' +
                    '<span>Neutral (-5% to +4%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-underperform"></span>' +
                    '<span>Moderate Underperformance (-6% to -9%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color strong-underperform"></span>' +
                    '<span>Strong Underperformance (≤-10%)</span></div>';
            }} else if (indicator === 'mansfield_rs') {{
                legendHTML = '<div class="legend-item">' +
                    '<span class="legend-color strong-strength"></span>' +
                    '<span>Strong Strength (≥1.2)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-strength"></span>' +
                    '<span>Moderate Strength (1.1-1.19)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral"></span>' +
                    '<span>Neutral (0.9-1.09)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-weakness"></span>' +
                    '<span>Moderate Weakness (0.8-0.89)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color strong-weakness"></span>' +
                    '<span>Strong Weakness (<0.8)</span></div>';
            }} else if (indicator === 'roc') {{
                legendHTML = '<div class="legend-item">' +
                    '<span class="legend-color strong-momentum"></span>' +
                    '<span>Strong Momentum (≥8%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-momentum"></span>' +
                    '<span>Moderate Momentum (3-7%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color neutral"></span>' +
                    '<span>Neutral (-3% to +2%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color moderate-decline"></span>' +
                    '<span>Moderate Decline (-4% to -7%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color strong-decline"></span>' +
                    '<span>Strong Decline (≤-8%)</span></div>';
            }} else if (indicator === 'vwap') {{
                legendHTML = '<div class="legend-item">' +
                    '<span class="legend-color overvalued"></span>' +
                    '<span>Overvalued (≥3%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color slightly-overvalued"></span>' +
                    '<span>Slightly Overvalued (1-2%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color fair-value"></span>' +
                    '<span>Fair Value (-1% to +0%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color slightly-undervalued"></span>' +
                    '<span>Slightly Undervalued (-2% to -1%)</span></div>' +
                    '<div class="legend-item">' +
                    '<span class="legend-color undervalued"></span>' +
                    '<span>Undervalued (≤-3%)</span></div>';
            }}
            
            legendContainer.innerHTML = legendHTML;
        }}
        
        // Initialize heatmap when page loads
        document.addEventListener('DOMContentLoaded', initHeatmap);
    </script>
    
    <style>
        .heatmap-container {{
            margin: 20px 0;
        }}
        
        .chart-controls {{
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .chart-controls label {{
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .chart-controls select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 20px 0;
        }}
        
        .chart-legend {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }}
        
        .legend-color.overbought {{
            background-color: rgba(244, 67, 54, 0.8);
        }}
        
        .legend-color.neutral-high {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        
        .legend-color.neutral {{
            background-color: rgba(76, 175, 80, 0.8);
        }}
        
        .legend-color.neutral-low {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        
        .legend-color.oversold {{
            background-color: rgba(33, 150, 243, 0.8);
        }}
        
        /* Returns vs BTC colors */
        .legend-color.strong-outperform {{
            background-color: rgba(76, 175, 80, 0.8);
        }}
        .legend-color.moderate-outperform {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.moderate-underperform {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.strong-underperform {{
            background-color: rgba(244, 67, 54, 0.8);
        }}
        
        /* Mansfield RS colors */
        .legend-color.strong-strength {{
            background-color: rgba(76, 175, 80, 0.8);
        }}
        .legend-color.moderate-strength {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.moderate-weakness {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.strong-weakness {{
            background-color: rgba(244, 67, 54, 0.8);
        }}
        
        /* ROC colors */
        .legend-color.strong-momentum {{
            background-color: rgba(76, 175, 80, 0.8);
        }}
        .legend-color.moderate-momentum {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.moderate-decline {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.strong-decline {{
            background-color: rgba(244, 67, 54, 0.8);
        }}
        
        /* VWAP colors */
        .legend-color.overvalued {{
            background-color: rgba(244, 67, 54, 0.8);
        }}
        .legend-color.slightly-overvalued {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.fair-value {{
            background-color: rgba(76, 175, 80, 0.8);
        }}
        .legend-color.slightly-undervalued {{
            background-color: rgba(255, 193, 7, 0.8);
        }}
        .legend-color.undervalued {{
            background-color: rgba(33, 150, 243, 0.8);
        }}
    </style>
    '''
    
    return html
