from app import create_app, db

'''
Importing:
- create_app: A function to initialize and configure the Flask application.
- db: The database instance used for managing database operations.
'''

app = create_app()

'''
Creating the Flask application instance using the create_app function.
'''

with app.app_context():
    db.create_all()

'''
Using the application context to create all database tables.
This ensures that the database schema is set up before running the app.
'''

if __name__ == '__main__':
    app.run(debug=True)

'''
Running the Flask application in debug mode when the script is executed directly.
Debug mode enables detailed error messages and live reloading during development.
'''