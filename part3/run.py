from app import create_app

"""Entry point for running the Flask application.
This module creates and configures the Flask application instance using
the create_app factory function. When run directly.
"""

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)