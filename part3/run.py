import pymysql
pymysql.install_as_MySQLdb()

from app import create_app
from app.extensions import db
from config import DevelopmentConfig

"""Entry point for running the Flask application."""

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    try:
        print("🔵 Starting Flask application on http://127.0.0.1:5000/")

        with app.app_context():
            db.create_all()  # Ensure all tables exist

        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Error starting the application: {e}")
