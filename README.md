# Journal Api
This is a RESTful API for managing journal entries.

# Features
Create, read, update, and delete (CRUD) operations for users and journal entries.
Retrieve entries by date.
User authentication.
Error handling for invalid requests.

# Technologies Used 
Flask: A lightweight web application framework for Python.
SQLAlchemy: An Object-Relational Mapping (ORM) library for Python.
PostgreSQL: A powerful open-source relational database management system.
Python: A high-level programming language.

# Getting Started
To get started with this project, follow these steps:
## Clone this repository to your local machine:
'git clone https://github.com/akosuaeffa/journal_api.git'

### Install the required dependencies:
'pip install -r requirements.txt'

### Set up your database:
Create a PostgreSQL database.
Update the database URI in the .env file.

### Run the application:
'python journal_api.py'

### Access the API endpoints using a tool like Postman or cURL.

# API Endpoints
- '/user': CRUD operations for users.
- '/entries': CRUD operations for journal entries.
- '/user/<user_id>/entries': Retrieve entries for a specific user.
- '/entries/<date>': Retrieve entries for a specific date.

# Contributing
Contributions are welcome! Please follow these guidelines when contributing:

1.Fork the repository.
2.Create a new branch for your feature or bug fix.
3.Make your changes and commit them.
4.Push your changes to your fork.
5.Submit a pull request.
