# HBnB Application 🏠 🔑

Welcome to the HBnB Application project! This application is designed to provide a platform for managing users, places, reviews, and amenities, similar to a simplified Airbnb.

## Project Structure 📂

The project is structured into several key directories, each serving a specific purpose:

*   `app/`: Contains the core application code. 🚀
    *   `__init__.py`: Initializes the Flask application and API.
    *   `api/`: Houses the API endpoints, organized by version. 🌐
        *   `v1/`: Contains the version 1 API endpoints.
            *   `__init__.py`: Initializes the v1 API package.
            *   `users.py`: API endpoints for user management. 🧑‍💼
            *   `places.py`: API endpoints for place management. 🏢
            *   `reviews.py`: API endpoints for review management. 📝
            *   `amenities.py`: API endpoints for amenity management. 🏊‍♀️
    *   `models/`: Contains the business logic classes (data models). 🗄️
        *   `__init__.py`: Initializes the models package.
        *   `user.py`: Defines the User model.
        *   `place.py`: Defines the Place model.
        *   `review.py`: Defines the Review model.
        *   `amenity.py`: Defines the Amenity model.
    *   `services/`: Implements the Facade pattern to manage interactions between layers. 🛠️
        *   `__init__.py`: Initializes the services package and creates a Facade instance.
        *   `facade.py`: Defines the `HBnBFacade` class.
    *   `persistence/`: Implements the in-memory repository for data storage. 💾
        *   `__init__.py`: Initializes the persistence package.
        *   `repository.py`: Defines the repository interface and the `InMemoryRepository` class.
*   `run.py`: The entry point for running the Flask application. 🏃
*   `config.py`: Defines environment-specific settings and configurations. ⚙️
*   `requirements.txt`: Lists all the Python packages required for the project. 📦
*   `README.md`: Provides an overview of the project setup and instructions. ℹ️

## Getting Started 🚀

Follow these instructions to get the application up and running on your local machine.

### Prerequisites ⚙️

*   Python 3.6+
*   pip (Python package installer)

### Installation 🛠️

1.  Clone the repository:

    ```
    git clone <repository_url>
    cd hbnb
    ```

2.  Create a virtual environment (recommended):

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

### Configuration ⚙️

1.  Set environment variables in `config.py` as needed.  A default secret key is provided, but it's recommended to set your own `SECRET_KEY` environment variable.

### Running the Application 🏃

1.  Run the application:

    ```
    python run.py
    ```

2.  Open your web browser and go to `http://127.0.0.1:5000/api/v1/` to view the API documentation.  (Note: the port may be different depending on your configuration)

## Dependencies 📦

*   `flask`: A micro web framework for Python.
*   `flask-restx`: An extension for Flask that adds support for quickly building REST APIs.

## Business Logic Layer (Models) 🏢

The `models/` directory contains the core business logic of the application.  It defines the data models (entities) that represent users, places, reviews, and amenities.  These models encapsulate the data and behavior related to these entities.

### Models Overview

*   **User:** Represents a user of the HBnB platform.  It stores information such as the user's ID, name, email, and password.
*   **Place:** Represents a place available for rent on the HBnB platform.  It stores information such as the place's ID, owner, location, price, and amenities.
*   **Review:** Represents a review of a place by a user.  It stores information such as the review's ID, the place being reviewed, the user who wrote the review, and the review text.
*   **Amenity:** Represents an amenity offered at a place (e.g., Wi-Fi, a swimming pool). It stores information such as the amenity's ID and name.

### Example Usage

While the exact implementation of the models (attributes and methods) is not provided in the current setup, here's an example of how you might use the `User` model *once it is fully implemented*:

## Resources 📚

*   [Flask Documentation](https://flask.palletsprojects.com/)
*   [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
*   [Python Project Structure Best Practices](https://realpython.com/python-application-layouts/)
*   [Facade Design Pattern in Python](https://www.tutorialspoint.com/design_pattern/facade_pattern.htm)
*   [Python OOP Basics](https://realpython.com/python3-object-oriented-programming/)
*   [Designing Classes and Relationships](https://docs.python.org/3/tutorial/classes.html)
*   [Why You Should Use UUIDs](https://docs.python.org/3/tutorial/classes.html)

## Authors