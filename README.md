# E-commerce API

This is an E-commerce API built using Django REST Framework (DRF). It supports user authentication via **Google OAuth** and **JWT**, and provides endpoints for managing products, categories, orders, and user profiles. The API documentation is generated using **DRF Spectacular**.

---

## Features

- **User Authentication**:
  - Google OAuth (using `django-allauth`).
  - JWT Authentication (using `django-rest-framework-simplejwt`).
- **Product Management**:
  - Create, read, update, and delete products.
  - Filter and search products by name, category, or price.
- **Order Management**:
  - Place, view, and cancel orders.
- **User Profiles**:
  - View and update user profiles.
- **API Documentation**:
  - Auto-generated API documentation using **DRF Spectacular**.

- **Asynchronous Task Management & Caching**:
  - **Celery** for background task execution (e.g., sending emails, processing orders).
  - **Redis** as:
    - A message broker for Celery to handle asynchronous tasks.
    - A caching layer to improve performance and reduce database queries.

---

## Technologies Used

- **Backend**:
  - Django
  - Django REST Framework (DRF)
  - Django Allauth (Google OAuth)
  - Simple JWT (JWT Authentication)
  - DRF Spectacular (API Documentation)
- **Database**:
  - PostgreSQL (or SQLite for development)
- **Other Tools**:
  - Docker (for containerization)
  - Swagger UI (for API documentation)

---

## Contact
If you have any questions or feedback, feel free to reach out:
<p align="left">
<a href="https://wa.me/919373961764" target="blank"><img align="center" src="https://img.icons8.com/color/48/000000/whatsapp.png" alt="WhatsApp" height="30" width="40" /></a>
<a href="https://www.linkedin.com/in/ganeshborkar31/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="sohail-ahmad342" height="30" width="40" /></a>
<a href="https://instagram.com/ganeshborkar31" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="sohail_ahmed113" height="30" width="40" /></a>
<a href="mailto:ganeshborkar31@gmail.com" target="blank"><img align="center" src="https://img.icons8.com/ios-filled/50/000000/email-open.png" alt="Email" height="30" width="40" /></a>
</p>
