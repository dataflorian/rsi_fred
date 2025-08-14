from flask import Blueprint, render_template_string
from app.services.binance_service import BinanceService
from app.services.rsi_calculator import RSICalculator

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
    </body>
    </html>
    """
    return html

@main_bp.route('/test-api')
def test_api():
    """Test route to verify Binance API connection"""
    try:
        binance_service = BinanceService()
        connection_status = binance_service.test_connection()
        
        if connection_status['status'] == 'connected':
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Test - RSI Crypto Screener</title>
            </head>
            <body>
                <h1>Binance API Connection Test</h1>
                <p style="color: green;">✅ {connection_status['message']}</p>
                <h3>Sample Trading Pairs:</h3>
                <ul>
            """
            
            for pair in connection_status['sample_pairs']:
                html += f"<li><strong>{pair['symbol']}</strong> ({pair['base']}/{pair['quote']})</li>"
            
            html += """
                </ul>
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        else:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Test - RSI Crypto Screener</title>
            </head>
            <body>
                <h1>Binance API Connection Test</h1>
                <p style="color: red;">❌ {connection_status['message']}</p>
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
            <title>API Test - RSI Crypto Screener</title>
        </head>
        <body>
            <h1>Binance API Connection Test</h1>
            <p style="color: red;">❌ Service initialization failed: {str(e)}</p>
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
                    <td>${analysis['last_price']:.4f if analysis['last_price'] else 'N/A'}</td>
                    <td class="{rsi_class}">{analysis['rsi'] if analysis['rsi'] else 'N/A'}</td>
                    <td>{analysis['signal']}</td>
                    <td>{analysis['price_change']}% if analysis['price_change'] is not None else 'N/A'}</td>
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
