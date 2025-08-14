from flask import Blueprint, render_template_string
from app.services.binance_service import BinanceService

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
