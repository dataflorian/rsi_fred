from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
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
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True)
