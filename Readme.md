# Vivaldi20-Backend

This is the backend API built using Django for the **Vivaldi20** project. It provides a RESTful API for managing the application's functionality.

## Features

- Django REST Framework for API endpoints
- JWT Authentication for secure access
- User management

## Getting Started

Follow these instructions to set up the **Vivaldi20-Backend** project on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or higher
- Git
- Virtual environment package (`python3 -m venv`)

### Installation

#### 1. Clone the repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/ngetichnicholas/Vivaldi20-Backend.git
cd Vivaldi20-Backend
```

#### 2. Set up the virtual environment

Create a virtual environment in the project folder and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```
or this in windows
```bash
python -m venv venv
```

#### 3. Install the dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables

Create a `.env` file in the root directory of the project and add the necessary environment variables, such as database credentials and secret keys.

Example `.env` file:

```bash
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=my-secret-key
```

#### 5. Set up the database

Apply the database migrations:

```bash
python3 manage.py migrate
```
For windows 
```bash
python manage.py migrate
```

#### 6. Create a superuser (optional)

To create a superuser for accessing the Django admin panel, run:

```bash
python3 manage.py createsuperuser
```

#### 7. Run the development server

Now, you can run the Django development server:

```bash
python3 manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

### Running Tests

To run the test suite, execute:

```bash
python3 manage.py test
```

### Deployment

For deploying this Django app, you can use services like Heroku, AWS, or a VPS. Ensure that all environment variables are set correctly in the production environment and that static files are properly configured.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.
