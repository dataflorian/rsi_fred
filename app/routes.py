from flask import Blueprint, render_template_string
from app.services.binance_service import BinanceService
from app.services.rsi_calculator import RSICalculator
from app.services.data_updater import DataUpdater

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
    """Main RSI screener showing top 10 performing coins"""
    try:
        data_updater = DataUpdater(rsi_period=14, top_coins_limit=10)
        top_coins = data_updater.get_top_performing_coins()
        stats = data_updater.get_screening_stats()
        
        if not top_coins:
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>RSI Screener - RSI Crypto Screener</title>
            </head>
            <body>
                <h1>RSI Crypto Screener</h1>
                <p style="color: orange;">⏳ No data available yet. Please wait for initial analysis...</p>
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSI Screener - RSI Crypto Screener</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #1a365d; text-align: center; margin-bottom: 30px; }}
                .stats {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #3182ce; }}
                .stats p {{ margin: 5px 0; color: #2d3748; }}
                .refresh-controls {{ text-align: center; margin: 20px 0; }}
                .refresh-btn {{ background: #3182ce; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                .refresh-btn:hover {{ background: #2c5aa0; }}
                .refresh-btn:disabled {{ background: #a0aec0; cursor: not-allowed; }}
                .loading {{ display: none; color: #3182ce; font-style: italic; }}
                .countdown {{ color: #718096; font-size: 14px; margin-top: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; overflow-x: auto; }}
                th, td {{ border: 1px solid #e2e8f0; padding: 12px; text-align: left; }}
                th {{ background-color: #1a365d; color: white; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: #f8f9fa; }}
                tr:hover {{ background-color: #e6fffa; }}
                .rsi-high {{ color: #e74c3c; font-weight: bold; }}
                .rsi-low {{ color: #27ae60; font-weight: bold; }}
                .rsi-neutral {{ color: #f39c12; font-weight: bold; }}
                .rsi-optimal {{ color: #2ecc71; font-weight: bold; }}
                .rank {{ font-weight: bold; color: #1a365d; }}
                .binance-link {{ color: #3182ce; text-decoration: none; }}
                .binance-link:hover {{ text-decoration: underline; }}
                .refresh-info {{ text-align: center; margin-top: 20px; color: #718096; }}
                .back-link {{ margin-top: 20px; }}
                .back-link a {{ color: #3182ce; text-decoration: none; }}
                .back-link a:hover {{ text-decoration: underline; }}
                @media (max-width: 768px) {{
                    .container {{ padding: 15px; margin: 10px; }}
                    table {{ font-size: 14px; }}
                    th, td {{ padding: 8px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 RSI Crypto Screener</h1>
                
                <div class="stats">
                    <p><strong>📊 Screening Statistics:</strong></p>
                    <p>📈 Total Coins Analyzed: {stats['total_coins_analyzed']}</p>
                    <p>🕒 Last Update: {stats['last_update'] or 'Never'}</p>
                    <p>⏰ Next Update: {stats['next_update'] or 'Unknown'}</p>
                    {f"<p>🏆 Top Performer: {stats['top_performer']['symbol']} (RSI: {stats['top_performer']['rsi']}, Signal: {stats['top_performer']['signal']})</p>" if stats['top_performer'] else ""}
                </div>
                
                <div class="refresh-controls">
                    <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
                    <div class="loading" id="loading">⏳ Refreshing data...</div>
                    <div class="countdown" id="countdown">Next auto-refresh in: <span id="timer">15:00</span></div>
                </div>
                
                <h2>🏅 Top 10 Performing Coins by RSI</h2>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Symbol</th>
                        <th>Price</th>
                        <th>RSI (14)</th>
                        <th>Signal</th>
                        <th>24h Change</th>
                        <th>Volume (24h)</th>
                        <th>Performance Score</th>
                        <th>Binance</th>
                    </tr>
        """
        
        for coin in top_coins:
            # Style RSI values
            rsi_class = ""
            if coin['rsi'] >= 70:
                rsi_class = "rsi-high"
            elif coin['rsi'] <= 30:
                rsi_class = "rsi-low"
            elif coin['rsi'] >= 50 and coin['rsi'] < 70:
                rsi_class = "rsi-optimal"
            else:
                rsi_class = "rsi-neutral"
            
            # Format volume
            volume_formatted = f"{coin['volume_24h']:,.0f}" if coin['volume_24h'] else 'N/A'
            
            html += f"""
            <tr>
                <td class="rank">#{coin['rank']}</td>
                <td><strong>{coin['symbol']}</strong></td>
                <td>${f"{coin['price']:.6f}" if coin['price'] else 'N/A'}</td>
                <td class="{rsi_class}">{coin['rsi']}</td>
                <td>{coin['signal']}</td>
                <td style="color: {'green' if coin['price_change_24h'] >= 0 else 'red'}">{coin['price_change_24h']:.2f}%</td>
                <td>{volume_formatted}</td>
                <td>{coin['performance_score']}</td>
                <td><a href="{coin['binance_link']}" target="_blank" class="binance-link">📈 Trade</a></td>
            </tr>
            """
        
        html += """
                </table>
                
                <div class="refresh-info">
                    <p>🔄 Data refreshes automatically every 15 minutes</p>
                    <p>📊 RSI values above 50 indicate strength, below 30 indicate oversold conditions</p>
                    <p>💡 Click "Refresh Data" to force an immediate update</p>
                </div>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
            
            <script>
                let countdown = 15 * 60; // 15 minutes in seconds
                let timerInterval;
                
                function startTimer() {{
                    timerInterval = setInterval(() => {{
                        countdown--;
                        const minutes = Math.floor(countdown / 60);
                        const seconds = countdown % 60;
                        document.getElementById('timer').textContent = 
                            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                        
                        if (countdown <= 0) {{
                            countdown = 15 * 60;
                            refreshData();
                        }}
                    }}, 1000);
                }}
                
                function refreshData() {{
                    const btn = document.querySelector('.refresh-btn');
                    const loading = document.getElementById('loading');
                    const countdownDiv = document.getElementById('countdown');
                    
                    btn.disabled = true;
                    loading.style.display = 'block';
                    countdownDiv.style.display = 'none';
                    
                    // Reload the page to get fresh data
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 1000);
                }}
                
                // Start the countdown timer when page loads
                document.addEventListener('DOMContentLoaded', startTimer);
            </script>
        </body>
        </html>
        """
        
        return html
        
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
