# Django E-commerce App 🛒

Welcome to the Django E-commerce App repository! This project is an E-commerce API built using the Django REST Framework (DRF). It provides a robust backend solution for managing online stores, supporting user authentication through Google OAuth and JWT. You can explore endpoints for managing products, categories, orders, and user profiles. The API documentation is generated using DRF Spectacular, making it easy to understand and use.

[![Releases](https://img.shields.io/badge/Releases-Check%20Here-brightgreen)](https://github.com/JobValdez/django-ecommerce-app/releases)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication**: Supports Google OAuth and JWT for secure user login.
- **Product Management**: Create, read, update, and delete products easily.
- **Category Management**: Organize products into categories for better navigation.
- **Order Management**: Handle customer orders efficiently.
- **User Profiles**: Manage user information and preferences.
- **API Documentation**: Automatically generated documentation for easy reference.

## Technologies Used

This project leverages a variety of technologies to provide a seamless e-commerce experience:

- **Django**: A high-level Python web framework that encourages rapid development.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **Celery**: Asynchronous task queue/job queue based on distributed message passing.
- **Redis**: In-memory data structure store used as a database, cache, and message broker.
- **Django Allauth**: Integrated set of Django applications addressing authentication, registration, account management, and more.
- **Simple JWT**: JSON Web Token authentication for Django REST Framework.
- **SQL**: Structured Query Language for managing and querying relational databases.

## Installation

To get started with the Django E-commerce App, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JobValdez/django-ecommerce-app.git
   cd django-ecommerce-app
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your environment variables, such as database credentials and secret keys.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

Your API should now be running at `http://127.0.0.1:8000/`.

## Usage

Once your server is up and running, you can interact with the API using tools like Postman or curl. Below are some examples of how to use the endpoints.

### Authentication

To authenticate users, you can use the Google OAuth flow or JWT tokens. After logging in, you will receive a token that you can use for subsequent requests.

### Managing Products

- **Create a Product**:
  ```http
  POST /api/products/
  Content-Type: application/json

  {
      "name": "Product Name",
      "price": 29.99,
      "category": "Category ID",
      "description": "Product Description"
  }
  ```

- **Get All Products**:
  ```http
  GET /api/products/
  ```

### Managing Orders

- **Create an Order**:
  ```http
  POST /api/orders/
  Content-Type: application/json

  {
      "user": "User ID",
      "products": [
          {
              "product": "Product ID",
              "quantity": 2
          }
      ]
  }
  ```

- **Get All Orders**:
  ```http
  GET /api/orders/
  ```

## API Documentation

For detailed API documentation, visit the [Releases](https://github.com/JobValdez/django-ecommerce-app/releases) section. Here, you will find all the necessary information about endpoints, request formats, and response structures.

## Contributing

We welcome contributions to improve the Django E-commerce App. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

Please ensure your code adheres to the project's coding standards and is well-documented.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please reach out:

- **Email**: jobvaldez@example.com
- **GitHub**: [JobValdez](https://github.com/JobValdez)

Thank you for checking out the Django E-commerce App! We hope it serves as a useful resource for your projects.