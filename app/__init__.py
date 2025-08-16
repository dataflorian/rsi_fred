from flask import Flask, request, Response
import os

def create_app():
    app = Flask(__name__)
    
    # Import and register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    @app.after_request
    def after_request(response):
        """Capture HTML responses and write to latest_output.html"""
        if response.status_code == 200 and 'text/html' in response.content_type:
            try:
                # Write the latest HTML output to file
                with open('latest_output.html', 'w', encoding='utf-8') as f:
                    f.write(response.get_data(as_text=True))
            except Exception as e:
                # Silently fail to avoid interfering with app behavior
                pass
        return response
    
    return app
